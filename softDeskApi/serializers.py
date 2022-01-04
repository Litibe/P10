from django.db.models.fields import CharField
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault
from authentication.serializers import UserSerializer

from softDeskApi.models import Comment, Contributor, Issue, Project


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment


class ContributorSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['role',  'user']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue


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
