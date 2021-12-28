from django.db.models.fields import CharField
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

from softDeskApi.models import Comment, Contributor, Issue, Project


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issue


class ProjectSerializer(ModelSerializer):
    title = fields.CharField(required=True)
    description = fields.CharField(required=True)
    type = fields.ChoiceField(choices=Project.Type_project.choices)
    author_user_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def create(self, validated_data):
        project = Project.objects.create(title=validated_data['title'],
                                         description=validated_data['description'],
                                         type=validated_data['type'],
                                         author_user_id=self.context.get(
                                             "request").user.id,
                                         )
        project.save()
        return project


class ProjectSerializerDetails(ModelSerializer):
    title = fields.CharField(required=True)
    description = fields.CharField(required=True)
    type = fields.ChoiceField(choices=Project.Type_project.choices)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def put(self, validated_data, pk):
        project = Project.objects.filter(id=pk)
        project.update(
            title=validated_data['title'], description=validated_data['description'], type=validated_data['type'])
        return project

    def delete(self, validated_data, pk):
        project = Project.objects.filter(id=pk)
        project.delete()
        return True
