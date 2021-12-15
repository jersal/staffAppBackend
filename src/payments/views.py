from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from src.payments.models import SubscriptionPayment
from src.payments.serializers import SubscriptionPaymentSerializer


class SubscriptionPaymentViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPayment.objects.all()
    serializer_class = SubscriptionPaymentSerializer

    def list(self, request):
        self.queryset = self.queryset.filter_query_params(request)
        return super(SubscriptionPaymentViewSet, self).list(request)


