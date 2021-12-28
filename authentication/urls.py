from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import UserSignUpView

router = routers.SimpleRouter()
router.register('signup', UserSignUpView, basename="signup")
