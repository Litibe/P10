import json
import time
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from rest_framework.authtoken.models import Token


from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.views import UserSignUpView
from softDeskApi.models import Project, Issue, Comment
from softDeskApi.views import ProjectView


class TestUsers(TestCase):

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    print(OKBLUE+"SECTION TEST USER"+ENDC)

    def integration_users(self):
        user1 = User.objects.create(email="motdepasse2022@djangotest1.fr",
                                    first_name="Django1",
                                    last_name="Test1")
        user1.set_password("motdepasse2022")
        user1.save()
        user2 = User.objects.create(email="motdepasse2022@djangotest2.fr",
                                    first_name="Django2",
                                    last_name="Test2")
        user2.set_password("motdepasse2022")
        user2.save()

    def test_create_new_user_406(self):
        """
        POST Method to create a new user with bad data
        """
        url = reverse("sign_up")
        data = {
            "email": "motdepasse2022@djangotest.fr",
            "password": "motdepasse2022",
            "fist_name": "Djando",
            'lest_name': "Test"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        print(self.FAIL+"new_user_406" + self.ENDC)
        print(json.loads(response.content))

    def test_create_new_user_201(self):
        """
        POST Method to create a new user with correct data
        """
        url = reverse("sign_up")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
            "first_name": "Django1",
            'last_name': "Test1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {
            "email": "motdepasse2022@djangotest1.fr",
            "first_name": "Django1",
            'last_name': "Test1"
        })
        print(self.OKGREEN + "create_new_user_201 OK" + self.ENDC)
        print(json.loads(response.content))

    def test_login_user_401(self):
        self.integration_users()
        """
        POST Method to log an user with bad data
        """
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"login_user_401"+self.ENDC)
        print(json.loads(response.content))

    def test_login_user_200(self):
        self.integration_users()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(self.OKGREEN+"login_user_200 OK"+self.ENDC)
        print(json.loads(response.content))


class TestProjects(TestCase):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def integration_users(self):
        user1 = User.objects.create(email="motdepasse2022@djangotest1.fr",
                                    first_name="Django1",
                                    last_name="Test1")
        user1.set_password("motdepasse2022")
        user1.save()
        user2 = User.objects.create(email="motdepasse2022@djangotest2.fr",
                                    first_name="Django2",
                                    last_name="Test2")
        user2.set_password("motdepasse2022")
        user2.save()

    def test_post_projects(self):
        print(self.OKBLUE+"SECTION TEST PROJECTS"+self.ENDC)
        """
        Test POST Method for create a Project
        """
        self.integration_users()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        request = json.loads(response.content)

        url = reverse("projects")
        data = {'title': "Test_project Mobile API",
                "description": "Mise en évidence d'une serie de tests pour l'application Mobile",
                "type": "IOS"
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"GET_Projects_Without_TOKEN_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token = 'Bearer ' + request.get('access')
        headers = {'HTTP_AUTHORIZATION': access_token}
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.get().title,
                         "Test_project Mobile API")
        print(self.OKGREEN+"GET_Projects_200 OK"+self.ENDC)
        print(json.loads(response.content))
