from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserSignUpView
from softDeskApi.views import CommentIntoProjectView, IssuesIntoProjectView, ProjectView, ProjectsListView, UserIntoProjectView, main_page

urlpatterns = [
    path('', main_page, name='homepage'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),

    path('projects/',
         ProjectsListView.as_view({"get": "list_projects",
                                  "post": "create_project"}), name='projects'),
    path('projects/<id_project>/',
         ProjectView.as_view({"get": "details_project",
                              "put": "update_project",
                              "delete": "delete_project"}), name='project'),

    path('projects/<id_project>/issues/',
         IssuesIntoProjectView.as_view({"get": "list_issues", "post": "create_issue"}), name='issues'),
    path('projects/<id_project>/issues/<id_issue>/',
         IssuesIntoProjectView.as_view({"put": "modify_issues", "delete": "delete_issue"}), name='issue'),

    path('projects/<id_project>/issues/<id_issue>/comments/',
         CommentIntoProjectView.as_view({"get": "list_comments", "post": "create_comment"}), name='comments'),
    path('projects/<id_project>/issues/<id_issue>/comments/<id_comment>/',
         CommentIntoProjectView.as_view({'get': 'details_comment', "put": "modify_comment", "delete": "delete_comment"}), name="comment"),

    path('projects/<id_project>/users/',
         UserIntoProjectView.as_view({"get": "list_users_project", "post": "add_user_into_project"}), name='contributors'),
    path('projects/<id_project>/users/<id_user>/',
         UserIntoProjectView.as_view({"delete": "del_user"}), name='del_contributor'),

    path('signup/',
         UserSignUpView.as_view({'post': "create_a_new_user"}), name='sign_up'),
]
