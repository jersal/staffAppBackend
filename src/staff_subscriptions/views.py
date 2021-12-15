from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from src.staff_subscriptions.models import StaffEmployee, StaffEmployeeSubscription
from src.staff_subscriptions.serializers import StaffEmployeeSerializer, StaffEmployeeSubscriptionSerializer


class StaffEmployeeViewSet(viewsets.ModelViewSet):
    queryset = StaffEmployee.objects.all()
    serializer_class = StaffEmployeeSerializer

    def list(self, request):
        self.queryset = self.queryset.filter_query_params(request)
        return super(StaffEmployeeViewSet, self).list(request)


class StaffEmployeeSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = StaffEmployeeSubscription.objects.all()
    serializer_class = StaffEmployeeSubscriptionSerializer

    def list(self, request):
        self.queryset = self.queryset.filter_query_params(request)
        return super(StaffEmployeeSubscriptionViewSet, self).list(request)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    @action(methods=['post'], detail=False)
    def bulk_upsert(self, request):
        """
        Insert or create multiple data at once
        """
        # TODO: check whether audit log is working or not
        if type(request.data) != list:
            raise Exception("Expected list for the bulk upsert")

        success_data = {
            'total_count': 0,
            'updated': 0,
            'inserted': 0
        }
        for item in request.data:
            id_ = item.get('id', None)
            if not id_:
                serializer = self.get_serializer(data=item)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                success_data['inserted'] += 1
            if id_:
                partial = True
                pk = int(id_)
                lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
                if pk:
                    self.kwargs['pk'] = pk
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=item, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                success_data['updated'] += 1

        success_data['total_count'] = success_data['updated'] + success_data['inserted']
        return Response(success_data, status=status.HTTP_201_CREATED)
