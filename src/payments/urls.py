from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from src.payments import views

router = routers.SimpleRouter()
router.register('subscription-payments', views.SubscriptionPaymentViewSet)


urlpatterns = [
    path(r'api/', include(router.urls))
]