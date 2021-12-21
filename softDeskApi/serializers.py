from rest_framework.serializers import ModelSerializer

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

    class Meta:
        model = Project
