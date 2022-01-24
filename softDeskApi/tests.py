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
from softDeskApi.models import Project, Issue, Comment, Contributor
from softDeskApi.serializers import ProjectSerializerDetails
from softDeskApi.views import ProjectView


class Test_A_Users(TestCase):

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


class Test_B_Projects(TestCase):
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
        user3 = User.objects.create(email="motdepasse2022@djangotest3.fr",
                                    first_name="Django3",
                                    last_name="Test3")
        user3.set_password("motdepasse2022")
        user3.save()

    def integrations_projects(self):
        project1 = Project.objects.create(title="Test_project Mobile API",
                                          description="Mise en évidence d'une serie de tests pour l'application Mobile",
                                          type="IOS")
        project1.save()
        author_p1 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest1.fr"), project=Project.objects.filter(id=1).first(), role="AUTHOR")
        author_p1.save()
        contrib_p1 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest2.fr"), project=Project.objects.filter(id=1).first(), role="CONTRIBUTOR")
        contrib_p1.save()
        project2 = Project.objects.create(title="Test_project Fonted",
                                          description="Mise en évidence une faille identification partie Panier",
                                          type="FRONTED")
        project2.save()
        author_p2 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest2.fr"), project=Project.objects.filter(id=2).first(), role="AUTHOR")
        author_p2.save()

    def test_POST_projects(self):
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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"POST_Projects_Without_TOKEN_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token = 'Bearer ' + request.get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.get().title,
                         "Test_project Mobile API")
        p1 = Project.objects.get(id=1)
        p1.delete()
        print(self.OKGREEN+"POST_Projects_200 OK"+self.ENDC)
        print(json.loads(response.content))

    def test_GET_projects(self):
        """
        Test GET Method for LIST PROJECTS ASSIGNED 
        """
        self.integration_users()
        self.integrations_projects()
        # without login
        url = reverse("projects")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"GET_Projects_Without_LOGIN_401 OK"+self.ENDC)
        print(json.loads(response.content))

        # login user 3 without Project
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        url = reverse("projects")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"GET_Projects_Without_Project_assigned_200 OK"+self.ENDC)
        print(json.loads(response.content))

        # login user1 with Project 1 only
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        url = reverse("projects")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"GET_Projects_200 OK"+self.ENDC)
        print(json.loads(response.content))


class Test_C_ProjectDetails(TestCase):
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
        user3 = User.objects.create(email="motdepasse2022@djangotest3.fr",
                                    first_name="Django3",
                                    last_name="Test3")
        user3.set_password("motdepasse2022")
        user3.save()

    def integrations_projects(self):
        project1 = Project.objects.create(title="Test_project Mobile API",
                                          description="Mise en évidence d'une serie de tests pour l'application Mobile",
                                          type="IOS")
        project1.save()
        author_p1 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest1.fr"), project=Project.objects.filter(id=1).first(), role="AUTHOR")
        author_p1.save()
        contrib_p1 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest2.fr"), project=Project.objects.filter(id=1).first(), role="CONTRIBUTOR")
        contrib_p1.save()
        project2 = Project.objects.create(title="Test_project Fonted",
                                          description="Mise en évidence une faille identification partie Panier",
                                          type="FRONTED")
        project2.save()
        author_p2 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest2.fr"), project=Project.objects.filter(id=2).first(), role="AUTHOR")
        author_p2.save()

    def test_PUT_project(self):
        """
        Test PUT Method on project by author
        """
        self.integration_users()
        self.integrations_projects()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')

        url = reverse("project", kwargs={'id_project': 1})
        data = {'title': "Test_project Mobile API modified",
                "description": "Mise en évidence d'une serie de tests pour l'application Mobile modified",
                "type": "IOS"
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"PUT_Project_Without_TOKEN_401 OK"+self.ENDC)
        print(json.loads(response.content))

        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"PUT_Project_200 OK"+self.ENDC)
        print(json.loads(response.content))

    def test_GET_project(self):
        """
        Test GET Method on project by author
        """
        self.integration_users()
        self.integrations_projects()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')

        url = reverse("project", kwargs={'id_project': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"GET_Project_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        url = reverse("project", kwargs={'id_project': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"GET_Project_200 OK"+self.ENDC)
        print(json.loads(response.content))

    def test_DELETE_project(self):
        """
        Test DELETE Method on project by author
        """
        self.integration_users()
        self.integrations_projects()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')

        url = reverse("project", kwargs={'id_project': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"DELETE_Project_ARE_NOT_AUTHOR_401 OK"+self.ENDC)
        print(json.loads(response.content))

        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, format='json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')

        url = reverse("project", kwargs={'id_project': 1})
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        print(self.OKGREEN+"DELETE_Project_200 OK"+self.ENDC)
        print(json.loads(response.content))


class Test_D_ContributorProject(TestCase):
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
        user3 = User.objects.create(email="motdepasse2022@djangotest3.fr",
                                    first_name="Django3",
                                    last_name="Test3")
        user3.set_password("motdepasse2022")
        user3.save()

    def integrations_projects(self):
        project1 = Project.objects.create(title="Test_project Mobile API",
                                          description="Mise en évidence d'une serie de tests pour l'application Mobile",
                                          type="IOS")
        project1.save()
        author_p1 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest1.fr"), project=Project.objects.filter(id=1).first(), role="AUTHOR")
        author_p1.save()
        project2 = Project.objects.create(title="Test_project Fonted",
                                          description="Mise en évidence une faille identification partie Panier",
                                          type="FRONTED")
        project2.save()
        author_p2 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest2.fr"), project=Project.objects.filter(id=2).first(), role="AUTHOR")
        author_p2.save()

    def test_GET_contributor_of_project(self):
        """
        Test GET Method to list author and contributor of project
        """
        self.integration_users()
        self.integrations_projects()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')

        url = reverse("contributors", kwargs={'id_project': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"GET_ContributorProject_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        url = reverse("contributors", kwargs={'id_project': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"ContributorProject OK"+self.ENDC)
        print(json.loads(response.content))

    def test_POST_contributor_of_project(self):
        """
        Test POST Method to add contributor into project
        """
        self.integration_users()
        self.integrations_projects()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')

        url = reverse("contributors", kwargs={'id_project': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"POST_ContributorProject_Without_ACCESS_AUTHOR_401 OK"+self.ENDC)
        print(json.loads(response.content))

        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        url = reverse("contributors", kwargs={'id_project': 1})
        response = self.client.post(
            url, data={"email": "motdepasse2022@djangotest2.fr"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"POST ContributorProject OK"+self.ENDC)
        print(json.loads(response.content))

    def test_DELETE_contributor_of_project(self):
        """
        Test DELETE Method to add contributor into project
        """
        self.integration_users()
        self.integrations_projects()
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        url = reverse("del_contributor", kwargs={
                      'id_project': 1, 'id_user': 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"DELETE_ContributorProject_Without_ACCESS_AUTHOR_401 OK"+self.ENDC)
        print(json.loads(response.content))

        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token
        url = reverse("contributors", kwargs={'id_project': 1})
        response = self.client.post(
            url, data={"email": "motdepasse2022@djangotest2.fr"})
        url = reverse("del_contributor", kwargs={
                      'id_project': 1, 'id_user': 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        print(self.OKGREEN+"DELETE ContributorProject OK"+self.ENDC)
        print(json.loads(response.content))


class Test_E_IssuesProject(TestCase):
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
        user3 = User.objects.create(email="motdepasse2022@djangotest3.fr",
                                    first_name="Django3",
                                    last_name="Test3")
        user3.set_password("motdepasse2022")
        user3.save()

    def integrations_projects(self):
        project1 = Project.objects.create(title="Test_project Mobile API",
                                          description="Mise en évidence d'une serie de tests pour l'application Mobile",
                                          type="IOS")
        project1.save()
        author_p1 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest1.fr"), project=Project.objects.filter(id=1).first(), role="AUTHOR")
        author_p1.save()
        project2 = Project.objects.create(title="Test_project Fonted",
                                          description="Mise en évidence une faille identification partie Panier",
                                          type="FRONTED")
        project2.save()
        author_p2 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest2.fr"), project=Project.objects.filter(id=2).first(), role="AUTHOR")
        author_p2.save()

    def login_user_1(self):
        """
        login user_1 and return access token
        """
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        return access_token

    def login_user_3(self):
        """
        login user_3 without any project and return access token
        """
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        return access_token

    def test_POST_issue_of_project(self):
        """
        Test POST Method to add issue into project
        """
        self.integration_users()
        self.integrations_projects()

        access_token3 = self.login_user_3()
        url = reverse("issues", kwargs={'id_project': 1})
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"POST_Issue_Without_ACCESS_AUTHOR_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        data = {
            "title": "Error to log",
            "description": "Echec to connect, loading",
            "priority": 'HIGH',
            'status': 'TO_DO2'
        }
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        url = reverse("issues", kwargs={'id_project': 1})
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        print(self.FAIL+"POST ISSUE 406 NOT_ACCEPTABLE"+self.ENDC)
        print(json.loads(response.content))
        data = {
            "title": "Error to log",
            "description": "Echec to connect, loading",
            'tag': 'BUG',
            "priority": 'HIGH',
            'status': 'TO_DO'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(self.OKGREEN+"POST ISSUE OK without assigned user"+self.ENDC)
        print(json.loads(response.content))

        data = {
            "title": "FREEZE APP IOS",
            "description": "Echec to connect, loading",
            'tag': 'BUG',
            "priority": 'HIGH',
            'status': 'TO_DO',
            "assignee_user": "motdepasse2022@djangotest3.fr"
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(self.OKGREEN+"POST ISSUE OK With assignee user"+self.ENDC)
        print(json.loads(response.content))

    def test_GET_issue_of_project(self):
        """
        Test GET Method to add issue into project
        """
        self.integration_users()
        self.integrations_projects()
        access_token3 = self.login_user_3()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        url = reverse("issues", kwargs={'id_project': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"GET_Issue_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        url = reverse("issues", kwargs={'id_project': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(self.OKGREEN+"GET NO CONTENT ISSUE 204 OK"+self.ENDC)
        print(response.content)

        # create new issue to get after....
        data = {
            "title": "FREEZE APP IOS",
            "description": "Echec to connect, loading",
            'tag': 'BUG',
            "priority": 'HIGH',
            'status': 'TO_DO',
            "assignee_user": "motdepasse2022@djangotest3.fr"
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"GET ISSUE 200 OK"+self.ENDC)
        print(json.loads(response.content))

    def test_DEL_issue_of_project(self):
        """
        Test DEL Method to add issue into project
        """
        self.integration_users()
        self.integrations_projects()

        # create new issue to get after....
        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        url = reverse("issues", kwargs={'id_project': 1})
        data = {
            "title": "FREEZE APP IOS",
            "description": "Echec to connect, loading",
            'tag': 'BUG',
            "priority": 'HIGH',
            'status': 'TO_DO',
            "assignee_user": "motdepasse2022@djangotest3.fr"
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        access_token3 = self.login_user_3()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        url = reverse("issue", kwargs={'id_project': 1, 'id_issue': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"DEL_Issue_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        print(self.OKGREEN+"DELETE ISSUE 202 SUCCESS"+self.ENDC)
        print(json.loads(response.content))

    def test_PUT_issue_of_project(self):
        """
        Test PUT Method to add issue into project
        """
        self.integration_users()
        self.integrations_projects()

        # create new issue to get after....
        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        url = reverse("issues", kwargs={'id_project': 1})
        data = {
            "title": "FREEZE APP IOS",
            "description": "Echec to connect, loading",
            'tag': 'BUG',
            "priority": 'HIGH',
            'status': 'TO_DO',
            "assignee_user": "motdepasse2022@djangotest3.fr"
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        access_token3 = self.login_user_3()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        url = reverse("issue", kwargs={'id_project': 1, 'id_issue': 1})
        data = {
            "title": "FREEZE APP IOS modified",
            "description": "Echec to connect, loading, modified",
            'tag': 'BUG',
            "priority": 'HIGH',
            'status': 'TO_DO',
        }
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"PUT_Issue_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        print(self.OKGREEN+"PUT ISSUE 202 SUCCESS"+self.ENDC)
        print(json.loads(response.content))


class Test_F_CommentProject(TestCase):
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
        user3 = User.objects.create(email="motdepasse2022@djangotest3.fr",
                                    first_name="Django3",
                                    last_name="Test3")
        user3.set_password("motdepasse2022")
        user3.save()

    def integrations_projects(self):
        project1 = Project.objects.create(title="Test_project Mobile API",
                                          description="Mise en évidence d'une serie de tests pour l'application Mobile",
                                          type="IOS")
        project1.save()
        author_p1 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest1.fr"), project=Project.objects.filter(id=1).first(), role="AUTHOR")
        author_p1.save()
        project2 = Project.objects.create(title="Test_project Fonted",
                                          description="Mise en évidence une faille identification partie Panier",
                                          type="FRONTED")
        project2.save()
        author_p2 = Contributor.objects.create(user=User.objects.get(
            email="motdepasse2022@djangotest2.fr"), project=Project.objects.filter(id=2).first(), role="AUTHOR")
        author_p2.save()

    def login_user_1(self):
        """
        login user_1 and return access token
        """
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest1.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        return access_token

    def login_user_3(self):
        """
        login user_3 without any project and return access token
        """
        url = reverse("login")
        data = {
            "email": "motdepasse2022@djangotest3.fr",
            "password": "motdepasse2022",
        }
        response = self.client.post(url, data, content_type='application/json')
        request = json.loads(response.content)
        access_token = 'Bearer ' + request.get('access')
        return access_token

    def create_an_issue(self):
        self.integration_users()
        self.integrations_projects()
        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1

        data = {
            "title": "FREEZE APP IOS",
            "description": "Echec to connect, loading",
            'tag': 'BUG',
            "priority": 'HIGH',
            'status': 'TO_DO',
            "assignee_user": "motdepasse2022@djangotest2.fr"
        }
        url = reverse("issues", kwargs={'id_project': 1})
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_GET_comments_of_project(self):
        """
        TEST GET METHOD FOR COMMENTS ISSUE PROJECT
        """
        self.create_an_issue()

        access_token3 = self.login_user_3()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        url = reverse("comments", kwargs={'id_project': 1, 'id_issue': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"GET_comments_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        url = reverse("comments", kwargs={'id_project': 1, 'id_issue': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(self.OKGREEN+"GET NO CONTENT COMMENT of ISSUE 204 OK"+self.ENDC)
        print(response.content)

        data = {
            "description": "Example of comment for this issue"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(self.OKGREEN+"GET COMMENTS of ISSUE 200 OK"+self.ENDC)
        print(response.content)

    def test_POST_comment_of_project(self):
        """
        TEST POST METHOD FOR COMMENTS ISSUE PROJECT
        """
        self.create_an_issue()

        access_token3 = self.login_user_3()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        url = reverse("comments", kwargs={'id_project': 1, 'id_issue': 1})
        data = {
            "description": "Example of comment for this issue"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"POST_comment_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(self.OKGREEN+"POST COMMENT of ISSUE 201 CREATED OK"+self.ENDC)
        print(response.content)

    def test_PUT_comment_of_project(self):
        """
        TEST PUT METHOD FOR COMMENTS ISSUE PROJECT
        """
        self.create_an_issue()
        # create an issue into db
        data = {
            "description": "Example of comment for this issue "}
        url = reverse("comments", kwargs={'id_project': 1, 'id_issue': 1})
        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        response = self.client.post(url, data, content_type="application/json")

        access_token3 = self.login_user_3()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        url = reverse("comment", kwargs={
                      'id_project': 1, 'id_issue': 1, 'id_comment': 1})
        data = {
            "description": "Example of comment for this issue MODIFIED "}
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"PUT_comment_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        print(self.OKGREEN+"PUT COMMENT of ISSUE 202 ACCEPTED OK"+self.ENDC)
        print(response.content)

    def test_DELETE_comment_of_project(self):
        """
        TEST DELETE METHOD FOR COMMENTS ISSUE PROJECT
        """
        self.create_an_issue()
        # create an issue into db
        data = {
            "description": "Example of comment for this issue "}
        url = reverse("comments", kwargs={'id_project': 1, 'id_issue': 1})
        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        response = self.client.post(url, data, content_type="application/json")

        access_token3 = self.login_user_3()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token3
        url = reverse("comment", kwargs={
                      'id_project': 1, 'id_issue': 1, 'id_comment': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(self.FAIL+"DELETE_comment_Without_ACCESS_401 OK"+self.ENDC)
        print(json.loads(response.content))

        access_token1 = self.login_user_1()
        self.client.defaults['HTTP_AUTHORIZATION'] = access_token1
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        print(self.OKGREEN+"DELETE COMMENT of ISSUE 202 ACCEPTED OK"+self.ENDC)
        print(response.content)
