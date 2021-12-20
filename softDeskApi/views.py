from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.models import User
from models import Comment, Contributor, Issue, Project
from authentication.serializers import UserSerializer
from serializers import CommentSerializer, ContributorSerializer, IssueSerializer, ProjectSerializer


class UserAPIView(APIView):

    def get(self, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
