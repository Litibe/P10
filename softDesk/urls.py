from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.urls import router as authentication_router
from softDeskApi.urls import router as softDeskApi_router

router = routers.DefaultRouter()
router.registry.extend(authentication_router.registry)
router.registry.extend(softDeskApi_router.registry)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
