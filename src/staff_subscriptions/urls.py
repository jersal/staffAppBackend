
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from src.staff_subscriptions import views

router = routers.SimpleRouter()
router.register('staff-employees', views.StaffEmployeeViewSet)
router.register('staff-subscriptions', views.StaffEmployeeSubscriptionViewSet)

urlpatterns = [
    path(r'api/', include(router.urls))
]