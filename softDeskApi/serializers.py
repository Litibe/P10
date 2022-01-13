from django.db.models.fields import CharField
from rest_framework import fields, status
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault
from authentication.serializers import UserSerializer
from authentication.models import User

from softDeskApi.models import Comment, Contributor, Issue, Project


class ContributorSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['role',  'user']


class ProjectSerializerCreate(ModelSerializer):

    title = fields.CharField(required=True)
    description = fields.CharField(required=True)
    type = fields.ChoiceField(choices=Project.Type_project.choices)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']

    def create(self, validated_data):
        project = Project.objects.create(title=validated_data['title'],
                                         description=validated_data['description'],
                                         type=validated_data['type'])
        project.save()
        return project


class ProjectSerializer(ProjectSerializerCreate):
    contributor_project = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', "contributor_project"]


class ProjectSerializerDetails(ModelSerializer):
    title = fields.CharField(required=True)
    description = fields.CharField(required=True)
    type = fields.ChoiceField(choices=Project.Type_project.choices)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']

    def put(self, validated_data, pk):
        project = Project.objects.filter(id=pk)
        project.update(
            title=validated_data['title'], description=validated_data['description'], type=validated_data['type'])
        return project


class IssueSerializer(ModelSerializer):
    project = ProjectSerializer()
    author_user = UserSerializer()
    assignee_user = UserSerializer()

    title = fields.CharField(required=True)
    description = fields.CharField(required=True)
    tag = fields.ChoiceField(choices=Issue.Tag_issue.choices)
    priority = fields.ChoiceField(choices=Issue.Priority_issue.choices)
    status = fields.ChoiceField(choices=Issue.Status_issue.choices)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status',
                  "author_user", 'assignee_user', 'project', "created_time"]

    def create(self, validated_data, project_object, author):
        if validated_data.get('assignee_user', '') != '':
            assignee = User.objects.filter(
                email=validated_data.get('assignee_user', '')).first()
        else:
            assignee = author
        new_issue = Issue.objects.create(title=validated_data['title'],
                                         description=validated_data['description'],
                                         tag=validated_data['tag'],
                                         priority=validated_data['priority'],
                                         status=validated_data["status"],
                                         project=project_object,
                                         author_user=author,
                                         assignee_user=assignee
                                         )
        new_issue.save()
        return new_issue

    def put(self, validated_data, pk):
        issue = Issue.objects.filter(id=pk)
        if validated_data.get('assignee_user', '') != "":
            issue.update(
                title=validated_data['title'],
                description=validated_data['description'],
                tag=validated_data['tag'],
                priority=validated_data['priority'],
                status=validated_data['status'],
                assignee_user=validated_data['assignee_user']
            )
        else:
            issue.update(
                title=validated_data['title'],
                description=validated_data['description'],
                tag=validated_data['tag'],
                priority=validated_data['priority'],
                status=validated_data['status'],
            )
        return issue


class IssueDetailsSerializer(ModelSerializer):
    author_user = UserSerializer()
    assignee_user = UserSerializer()

    title = fields.CharField(required=True)
    description = fields.CharField(required=True)
    tag = fields.ChoiceField(choices=Issue.Tag_issue.choices)
    priority = fields.ChoiceField(choices=Issue.Priority_issue.choices)
    status = fields.ChoiceField(choices=Issue.Status_issue.choices)

    class Meta:
        model = Issue
        fields = ['id', "created_time", 'title', 'description', 'tag', 'priority', 'status',
                  "author_user", 'assignee_user']


class IssueSerializerCreate(ModelSerializer):
    title = fields.CharField(required=True)
    description = fields.CharField(required=True)
    tag = fields.ChoiceField(choices=Issue.Tag_issue.choices)
    priority = fields.ChoiceField(choices=Issue.Priority_issue.choices)
    status = fields.ChoiceField(choices=Issue.Status_issue.choices)

    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority', 'status']


class CommentSerializer(ModelSerializer):
    description = fields.CharField(required=True)
    author_user = UserSerializer()
    issue = IssueDetailsSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_time', 'author_user', 'issue']

    def create(self, validated_data, author_user, issue):
        comment = Comment.objects.create(description=validated_data['description'],
                                         author_user=author_user,
                                         issue=issue)
        comment.save()
        return comment


class CommentSerializerCreate(ModelSerializer):
    description = fields.CharField(required=True)

    class Meta:
        model = Comment
        fields = ['description']

    def put(self, validated_data, pk):
        comment = Comment.objects.filter(id=pk)
        comment.update(
            description=validated_data['description'])
        return comment
