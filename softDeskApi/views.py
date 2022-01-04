from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import generics, permissions, response, status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from authentication.models import User
from softDeskApi.models import Comment, Contributor, Issue, Project
from authentication.serializers import UserSerializer
from softDeskApi.serializers import CommentSerializer, ContributorSerializer, IssueSerializer, ProjectSerializerCreate, ProjectSerializer, ProjectSerializerDetails


class ProjectListView(ViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    serializer_details_for_project = ProjectSerializerDetails

    def list(self, request):
        """
        GET Method
        Return :
            - All projects created by user_logged
        """

        projects = Project.objects.filter(contributor=request.user.id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        POST Method
        Return :
            - a new project created
            - integration link Contributors-Projects
        """
        serializer_project = ProjectSerializerCreate(
            data=request.data)
        if serializer_project.is_valid():
            project_created = serializer_project.create(request.data)
            contributor = Contributor.objects.create(
                user=request.user, project=Project.objects.filter(id=project_created.id).first(), role="AUTHOR")
            contributor.save()
            projects = Project.objects.filter(id=project_created.id)
            serializer = ProjectSerializerCreate(projects, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("ERROR TO CREATE PROJECT", status=status.HTTP_406_NOT_ACCEPTABLE)

    def retrieve(self, request, pk):
        """
        GET Method for details project
        Return :
            - details projects created by user_logged
        """
        project = get_object_or_404(Project, id=pk)
        projects = Project.objects.filter(contributor=request.user.id, id=pk)
        if projects.exists():
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !", status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk):
        """
        PUT Method for details project
        Return :
            - updated projects
        """

        project = get_object_or_404(Project, id=pk)
        projects = Project.objects.filter(contributor=request.user.id, id=pk)
        if projects.exists():
            serializer = ProjectSerializerDetails(
                data=request.data)
            if serializer.is_valid():
                serializer.put(serializer.data, pk)
                return Response(serializer.data)
            return Response("INPUT ERROR", status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !", status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        """
        DELETE Method for details project
        Return :
            - delete projects created by user_logged
        """
        project = get_object_or_404(
            Project, id=pk)
        project = Project.objects.filter(contributor=request.user.id, id=pk)
        if project.exists():
            project.delete()
            return Response("SUCCESSFULLY", status=status.HTTP_202_ACCEPTED)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !", status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """
        GET Method for users details into project
        Return :
            - list of users into project
        """
        project = get_object_or_404(
            Project, id=pk)
        projects = Project.objects.filter(contributor=request.user.id, id=pk)
        if projects.exists():
            contributors = Contributor.objects.filter(
                project_id=pk)
            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !", status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['post'])
    def users(self, request, pk=None):
        """
        POST Method to add Contributor into project
        Return :
            - list of users into project
        """
        project = get_object_or_404(
            Project, id=pk)
        projects = Project.objects.filter(contributor=request.user.id, id=pk)

        if projects.exists():
            new_contributor = User.objects.filter(
                email=request.data.get('email', '')).first()
            if not new_contributor:
                return Response("INPUT ERROR", status=status.HTTP_406_NOT_ACCEPTABLE)
            contributor_not_in_projects = Project.objects.filter(
                contributor=new_contributor.id, id=pk)
            if contributor_not_in_projects:
                return Response("User Already into current project", status=status.HTTP_409_CONFLICT)

            if new_contributor and not contributor_not_in_projects:
                contributor = Contributor.objects.create(
                    user=new_contributor, project=projects.first(), role="CONTRIBUTOR")
                contributor.save()
                projects = Project.objects.filter(
                    contributor=request.user.id, id=pk)
                if projects.exists():
                    contributors = Contributor.objects.filter(
                        project_id=pk)
                    serializer = ContributorSerializer(contributors, many=True)
                    return Response(serializer.data)
            return Response("INPUT ERROR", status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !", status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['delete'])
    def users(self, request, pk=None):
        """
        DEL Method to del Contributor into project
        Return :
            - list of users into project
        """
        project = get_object_or_404(
            Project, id=pk)
        projects = Project.objects.filter(contributor=request.user.id, id=pk)

        if projects.exists():
            new_contributor = User.objects.filter(
                email=request.data.get('email', '')).first()
            if not new_contributor:
                return Response("INPUT ERROR", status=status.HTTP_406_NOT_ACCEPTABLE)
            contributor_in_projects = Project.objects.filter(
                contributor=new_contributor.id, id=pk)
            if not contributor_in_projects:
                return Response("User isn't into current project", status=status.HTTP_409_CONFLICT)

            if new_contributor and contributor_in_projects:
                contributor = Contributor.objects.filter(
                    user=new_contributor, project=projects.first()).first()
                contributor.delete()
                projects = Project.objects.filter(
                    contributor=request.user.id, id=pk)
                if projects.exists():
                    contributors = Contributor.objects.filter(
                        project_id=pk)
                    serializer = ContributorSerializer(contributors, many=True)
                    return Response(serializer.data)
            return Response("INPUT ERROR", status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT IN CONTRIBUTOR_PROJECT !", status=status.HTTP_401_UNAUTHORIZED)
