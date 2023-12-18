from rest_framework.routers import DefaultRouter
from accounts.api import views

router = DefaultRouter()
router.register(r'accounts/token-user',views.TokenUser,basename='token-user')