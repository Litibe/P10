from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.serializers import UserSerializer


class UserSignUpView(ViewSet):
    serializer_class = UserSerializer

    def create(self, request, format=None):
        """
        POST Method
        Return :
            - user created informations
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
