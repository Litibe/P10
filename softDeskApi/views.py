from django.conf import settings
from rest_framework import serializers
from rest_framework import generics, permissions, response, status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from softDeskApi.models import Comment, Contributor, Issue, Project
from authentication.serializers import UserSerializer
from softDeskApi.serializers import CommentSerializer, ContributorSerializer, IssueSerializer, ProjectSerializer, ProjectSerializerDetails


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
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def create(self, request, format=None):
        """
        POST Method
        Return : 
            - a new project created
        """
        serializer_project = ProjectSerializer(
            data=request.data)
        if serializer_project.is_valid():
            serializer_project.create(self, request.data, request.user.id)
            return Response(serializer_project.data, status=status.HTTP_201_CREATED)
        return Response(serializer_project.data)

    def retrieve(self, request, pk):
        """
        GET Method for details project
        Return : 
            - details projects created by user_logged
        """
        projects = Project.objects.filter(id=pk)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        PUT Method for details project
        Return : 
            - updated projects 
        """
        serializer = ProjectSerializerDetails(
            data=request.data)
        if serializer.is_valid():
            serializer.put(serializer.data, pk)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """
        DELETE Method for details project
        Return : 
            - delete projects created by user_logged
        """
        serializer = ProjectSerializerDetails(
            data=request.data)
        if serializer.is_valid():
            serializer.delete(serializer.data, pk)
        return Response(serializer.data)
