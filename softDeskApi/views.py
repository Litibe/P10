from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from softDeskApi.models import Comment, Contributor, Issue, Project
from softDeskApi import serializers


def main_page(request):
    return render(request, "softDeskApi/index.html")


class ProjectsListView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list_projects(self, request):
        """
        GET Method
        Return :
            - A list where user_logged is an \
                Author or a contributor of projects
        """
        projects = Project.objects.filter(
            contributor=request.user.id)
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def create_project(self, request):
        """
        POST Method
        Return :
            - a new project created
            - integration link Contributors-Projects
        """
        serializer_project = serializers.ProjectSerializerCreate(
            data=request.data)
        if serializer_project.is_valid():
            project_created = serializer_project.create(request.data)
            author_project = Contributor.objects.create(
                user=request.user, project=Project.objects.filter(
                    id=project_created.id).first(), role="AUTHOR")
            author_project.save()
            projects = Project.objects.filter(id=project_created.id).first()
            serializer = serializers.ProjectSerializerCreate(
                projects, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("ERROR TO CREATE PROJECT",
                        status=status.HTTP_406_NOT_ACCEPTABLE)


class ProjectView(ViewSet):
    permission_classes = [IsAuthenticated]

    def details_project(self, request, id_project):
        """
        GET Method for details project
        Return :
            - details projects where user_logged is in \
                list contributor/author of project
        """
        get_object_or_404(Project, id=id_project)
        project = Project.objects.filter(
            contributor=request.user.id, id=id_project)
        if project.exists():
            serializer = serializers.ProjectSerializer(
                project.first(), many=False)
            return Response(serializer.data)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !",
                        status=status.HTTP_401_UNAUTHORIZED)

    def update_project(self, request, id_project):
        """
        PUT Method for details project
        Return :
            - updated projects only by this author
        """
        get_object_or_404(Project, id=id_project)
        author = Contributor.objects.filter(
            project=id_project, role="AUTHOR").first()
        if author.user.id == request.user.id:
            serializer = serializers.ProjectSerializerDetails(
                data=request.data)
            if serializer.is_valid():
                serializer.put(serializer.data, id_project)
                return Response(serializer.data)
            return Response("INPUT ERROR",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT THE AUTHOR OF THIS PROJECT !\
             Update Unauthorized",
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete_project(self, request, id_project):
        """
        DELETE Method for details project
        Return :
            - SUCCESSFULL - HTTP_202_ACCEPTED
        """
        project = get_object_or_404(
            Project, id=id_project)
        author = Contributor.objects.filter(
            project=id_project, role="AUTHOR").first()
        if author.user.id == request.user.id:
            project.delete()
            return Response("SUCCESSFULLY",
                            status=status.HTTP_202_ACCEPTED)
        return Response("YOU ARE NOT THE AUTHOR OF THIS PROJECT ! \
            DELETE Unauthorized",
                        status=status.HTTP_401_UNAUTHORIZED)


class UserIntoProjectView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list_users_project(self, request, id_project):
        """
        GET Method for users details into project
        Return :
            - list of users into project
        """
        project = get_object_or_404(
            Project, id=id_project)
        if_user_into_project = Contributor.objects.filter(
            project_id=id_project, user=request.user.id)
        if project and if_user_into_project:
            contributors = Contributor.objects.filter(
                project_id=id_project)
            serializer = serializers.ContributorSerializer(
                contributors, many=True)
            return Response(serializer.data)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !\
             Unauthorized",
                        status=status.HTTP_401_UNAUTHORIZED)

    def add_user_into_project(self, request, id_project):
        """
        POST Method for users details into project
        Return :
            - create a new contributor into project\
                and return list of all users into project
        """
        project = get_object_or_404(
            Project, id=id_project)
        author = Contributor.objects.filter(
            project=id_project, role="AUTHOR").first()
        if author.user.id == request.user.id:
            new_contributor = User.objects.filter(
                email=request.data.get('email', '')).first()
            if not new_contributor:
                return Response("INPUT ERROR",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            contributor_in_projects = Project.objects.filter(
                contributor=new_contributor.id, id=id_project)
            if contributor_in_projects:
                return Response("User Already into current project",
                                status=status.HTTP_409_CONFLICT)

            if new_contributor and not contributor_in_projects:
                contributor = Contributor.objects.create(
                    user=new_contributor,
                    project=project,
                    role="CONTRIBUTOR")
                contributor.save()
                projects = Project.objects.filter(
                    contributor=request.user.id, id=id_project)
                if projects.exists():
                    contributors = Contributor.objects.filter(
                        project_id=id_project)
                    serializer = serializers.ContributorSerializer(
                        contributors, many=True)
                    return Response(serializer.data)
                return Response("INPUT ERROR",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT THE AUTHOR OF THIS PROJECT !",
                        status=status.HTTP_401_UNAUTHORIZED)

    def del_user(self, request, id_project, id_user):
        """
        DEL Method for user
        Return :
            - HTTP_202 to successful delete
            - HTTP_404 if user_id not into contributor Project
            or not existing project
        """
        contributor = get_object_or_404(
            Contributor, user=id_user, project=id_project,
            role="CONTRIBUTOR")
        author = Contributor.objects.filter(
            project=id_project, role="AUTHOR").first()
        if author.user.id == request.user.id:
            contributor = Contributor.objects.filter(
                project=id_project, role="CONTRIBUTOR", user=id_user).first()
            if contributor:
                string_response = "SUCCESSFULLY Delete Contributor - "\
                    + "email : " + \
                    str(contributor.user) + " with user_id #" + \
                    str(contributor.user.id)
                contributor.delete()
                return Response(string_response,
                                status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                "YOU ARE NOT THE AUTHOR OF THIS PROJECT ! Unauthorized",
                status=status.HTTP_401_UNAUTHORIZED)


class IssuesIntoProjectView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list_issues(self, request, id_project=None):
        """
        GET Method for issues details into project
        Return :
            - list of issues into project
        """
        project = get_object_or_404(
            Project, id=id_project)
        users_access_ok = Contributor.objects.filter(
            project=id_project, user=request.user.id)
        if project and users_access_ok:
            issues = Issue.objects.filter(Q(project=id_project) & (
                Q(assignee_user=request.user.id) | Q(
                    author_user=request.user.id)))
            if not issues:
                return Response("Not Issues for you in this project",
                                status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = serializers.IssueDetailsSerializer(
                    issues, many=True)
                return Response(serializer.data)
        return Response(
            "YOU ARE NOT IN CONTRIBUTOR_PROJECT ! UNAUTHORIZED ACCESS",
            status=status.HTTP_401_UNAUTHORIZED)

    def create_issue(self, request, id_project):
        """
        POST Method for issues details into project
        Return :
            - create a new issue into project
        """
        projects = get_object_or_404(
            Project, id=id_project)
        users_access_ok = Contributor.objects.filter(
            project=id_project, user=request.user).first()
        if projects and users_access_ok:
            serializer_issue = serializers.IssueSerializer(
                data=request.data)
            if serializer_issue.is_valid():
                issue_created = serializer_issue.create(
                    request.data, projects, author=request.user)
                issue = Issue.objects.filter(id=issue_created.id)
                serializer = serializers.IssueSerializer(issue,
                                                         many=True)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response("INPUT ERROR",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !",
                        status=status.HTTP_401_UNAUTHORIZED)

    def modify_issues(self, request, id_project, id_issue):
        """
        PUT Method for details project
        Return :
            - updated issue only by this author
        """
        project = get_object_or_404(
            Project, id=id_project)
        issue = Issue.objects.filter(
            Q(id=id_issue) & Q(author_user=request.user.id))
        if project and issue:
            serializer_issue = serializers.IssueSerializer(
                data=request.data)
            if serializer_issue.is_valid():
                serializer_issue.put(request.data, id_issue)
                issue = Issue.objects.filter(id=id_issue)
                serializer = serializers.IssueDetailsSerializer(
                    issue, many=True)
                return Response(serializer.data,
                                status=status.HTTP_202_ACCEPTED)
            return Response("INPUT ERROR",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT THE AUTHOR OF THIS ISSUE! \
            Update Unauthorized",
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete_issue(self, request, id_project, id_issue):
        """
        DELETE Method for details project
        Return :
            - delete issue only by this author
        """
        issue = get_object_or_404(
            Issue, id=id_issue)
        issue = Issue.objects.filter(
            Q(id=id_issue) & Q(author_user=request.user.id))
        if issue:
            issue.delete()
            return Response("SUCCESSFULLY",
                            status=status.HTTP_202_ACCEPTED)
        return Response("YOU ARE NOT THE AUTHOR OF THIS ISSUE!\
             Update Unauthorized",
                        status=status.HTTP_401_UNAUTHORIZED)


class CommentIntoProjectView(ViewSet):
    permission_classes = [IsAuthenticated]

    def list_comments(self, request, id_project, id_issue):
        """
        GET Method for comments details for an issue into project
        Return :
            - list of comments for an issue into project
        """
        issue = get_object_or_404(
            Issue, Q(id=id_issue) & Q(project_id=id_project))
        issue_access = Issue.objects.filter(Q(id=id_issue) & (
            Q(assignee_user=request.user.id) | Q(
                author_user=request.user.id)) & Q(project_id=id_project))
        if issue_access and issue:
            comments = Comment.objects.filter(issue_id=id_issue)
            if not comments:
                return Response("Not Comments for you in this Issue",
                                status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = serializers.CommentSerializer(
                    comments, many=True)
                return Response(serializer.data)
        return Response(
            "YOU ARE NOT THE AUTHOR OR THE USER ASSIGNEE OF \
                THIS ISSUE/PROJECT! UNAUTHORIZED ACCESS",
            status=status.HTTP_401_UNAUTHORIZED)

    def create_comment(self, request, id_project, id_issue):
        """
        POST Method for add comment for an issue into project
        Return :
            - create a new comment into issue
        """
        issue = get_object_or_404(
            Issue, Q(id=id_issue) & Q(project_id=id_project))
        issue_access = Issue.objects.filter(Q(id=id_issue) & (
            Q(assignee_user=request.user.id) | Q(
                author_user=request.user.id)) & Q(project_id=id_project))
        if issue_access and issue:
            serializer_comment_create = serializers.CommentSerializerCreate(
                data=request.data)
            serializer_comment = serializers.CommentSerializer(
                data=request.data)
            if serializer_comment_create.is_valid():
                comment_created = serializer_comment.create(
                    request.data,
                    author_user=request.user, issue=issue)
                comment = Comment.objects.filter(
                    id=comment_created.id)
                serializer = serializers.CommentSerializer(
                    comment, many=True)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response("INPUT ERROR",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(
            "YOU ARE NOT THE AUTHOR OR THE USER ASSIGNEE OF THIS \
                ISSUE/PROJECT! UNAUTHORIZED ACCESS",
            status=status.HTTP_401_UNAUTHORIZED)

    def details_comment(self, request, id_project, id_issue, id_comment):
        """
        GET Method for comment details
        Return :
            - get a comment into issue
        """
        comment = get_object_or_404(Comment, id=id_comment)
        issue_access = Issue.objects.filter(Q(id=id_issue) & (
            Q(assignee_user=request.user.id) | Q(
                author_user=request.user.id)) & Q(
                    project_id=id_project))
        if issue_access:
            comment = Comment.objects.filter(Q(id=id_comment) & (
                Q(author_user=request.user.id)))
            serializer = serializers.CommentSerializer(
                comment.first(), many=False)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(
            "YOU ARE NOT THE AUTHOR OR USER ASSIGNEE OF \
                THIS ISSUE/PROJECT! UNAUTHORIZED ACCESS",
            status=status.HTTP_401_UNAUTHORIZED)

    def modify_comment(self, request, id_project, id_issue, id_comment):
        """
        PUT Method for comment
        Return :
            - modify a comment into project
        """
        comment = get_object_or_404(Comment, id=id_comment)
        issue_access = Issue.objects.filter(Q(id=id_issue) & (
            Q(assignee_user=request.user.id) | Q(
                author_user=request.user.id)) & Q(project_id=id_project))
        comment_access = Comment.objects.filter(Q(id=id_comment) & (
            Q(author_user=request.user.id)))
        if issue_access and comment_access:
            serializer_comment_create = serializers.CommentSerializerCreate(
                data=request.data)
            if serializer_comment_create.is_valid():
                serializer_comment_create.put(request.data, id_comment)
                comment = get_object_or_404(Comment, id=id_comment)
                serializer = serializers.CommentSerializer(
                    comment, many=False)
                return Response(serializer.data,
                                status=status.HTTP_202_ACCEPTED)
            return Response("INPUT ERROR",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(
            "YOU ARE NOT THE AUTHOR OF THIS COMMENT! UNAUTHORIZED ACCESS",
            status=status.HTTP_401_UNAUTHORIZED)

    def delete_comment(self, request, id_project, id_issue, id_comment):
        """
        DELETE Method to delete comment
        Return :
            - HTTP_202 to successful delete
            - HTTP_404 if user_id is NOT THE AUTHOR OR THE USER ASSIGNEE
             OF THIS ISSUE/PROJECT or not existing project
        """
        comment = get_object_or_404(Comment, id=id_comment)
        issue_access = Issue.objects.filter(Q(id=id_issue) & (
            Q(assignee_user=request.user.id) | Q(
                author_user=request.user.id)) & Q(
                    project_id=id_project))
        comment_access = Comment.objects.filter(Q(id=id_comment) & (
            Q(author_user=request.user.id)))
        if issue_access and comment_access:
            comment.delete()
            return Response("SUCCESSFULLY",
                            status=status.HTTP_202_ACCEPTED)
        return Response(
            "YOU ARE NOT THE AUTHOR OF THIS COMMENT! UNAUTHORIZED ACCESS",
            status=status.HTTP_401_UNAUTHORIZED)
