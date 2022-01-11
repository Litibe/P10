from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.urls import router as authentication_router
from softDeskApi.urls import router as softDeskApi_router
from softDeskApi.views import CommentIntoProjectView, IssuesIntoProjectView, UserIntoProjectView

router = routers.DefaultRouter()
router.registry.extend(authentication_router.registry)
router.registry.extend(softDeskApi_router.registry)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('projects/<id_project>/issues/',
         IssuesIntoProjectView.as_view({"get": "list_issues", "post": "create_issue"})),
    path('projects/<id_project>/issues/<id_issue>/',
         IssuesIntoProjectView.as_view({"put": "modify_issues", "delete": "delete_issue"})),

    path('projects/<id_project>/issues/<id_issue>/comments/',
         CommentIntoProjectView.as_view({"get": "list_comments", "post": "create_comment"})),

    path('projects/<id_project>/users/',
         UserIntoProjectView.as_view({"get": "list_users_project", "post": "add_user_into_project"})),
    path('projects/<id_project>/users/<id_user>/',
         UserIntoProjectView.as_view({"delete": "del_user"})),
]
