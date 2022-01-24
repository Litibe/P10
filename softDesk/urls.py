from django.urls import path
from rest_framework_simplejwt import views as DRF_jwt_views
from authentication.views import UserSignUpView
from softDeskApi import views as sdApi_views

urlpatterns = [
    path('', sdApi_views.main_page, name='homepage'),
    path('login/', DRF_jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', DRF_jwt_views.TokenRefreshView.as_view(),
         name='login_refresh'),

    path('projects/',
         sdApi_views.ProjectsListView.as_view(
             {"get": "list_projects",
              "post": "create_project"}), name='projects'),
    path('projects/<id_project>/',
         sdApi_views.ProjectView.as_view(
             {"get": "details_project",
              "put": "update_project",
              "delete": "delete_project"}), name='project'),

    path('projects/<id_project>/issues/',
         sdApi_views.IssuesIntoProjectView.as_view(
             {"get": "list_issues",
              "post": "create_issue"}), name='issues'),
    path('projects/<id_project>/issues/<id_issue>/',
         sdApi_views.IssuesIntoProjectView.as_view(
             {"put": "modify_issues",
              "delete": "delete_issue"}), name='issue'),

    path('projects/<id_project>/issues/<id_issue>/comments/',
         sdApi_views.CommentIntoProjectView.as_view(
             {"get": "list_comments",
              "post": "create_comment"}),
         name='comments'),
    path('projects/<id_project>/issues/<id_issue>/comments/<id_comment>/',
         sdApi_views.CommentIntoProjectView.as_view(
             {'get': 'details_comment',
              "put": "modify_comment",
              "delete": "delete_comment"}), name="comment"),

    path('projects/<id_project>/users/',
         sdApi_views.UserIntoProjectView.as_view(
             {"get": "list_users_project",
              "post": "add_user_into_project"}), name='contributors'),
    path('projects/<id_project>/users/<id_user>/',
         sdApi_views.UserIntoProjectView.as_view(
             {"delete": "del_user"}), name='del_contributor'),

    path('signup/',
         UserSignUpView.as_view(
             {'post': "create_a_new_user"}), name='sign_up'),
]
