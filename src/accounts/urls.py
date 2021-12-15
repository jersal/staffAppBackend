
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from src.accounts import views
from src.accounts.views import CustomAuthToken

router = routers.SimpleRouter()
router.register('users', views.AuthUserViewSet)


urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api-token-auth/', CustomAuthToken.as_view())
]

