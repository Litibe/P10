from rest_framework import serializers
from rest_framework import generics, permissions, response, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from rest_framework.response import Response

from authentication.models import User
from softDeskApi.models import Comment, Contributor, Issue, Project
from authentication.serializers import UserSerializer
from softDeskApi.serializers import CommentSerializer, ContributorSerializer, IssueSerializer, ProjectSerializer

# Endpoint1


class UserSignUpView(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Endpoint3


class ProjectAllView(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
