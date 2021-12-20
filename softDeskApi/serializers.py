from rest_framework.serializers import ModelSerializer

from models import Comment, Contributor, Issue, Project


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Comment
