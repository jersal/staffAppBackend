from datetime import datetime

from django.db import models


class StaffEmployeeQuerySet(models.QuerySet):

    def filter_query_params(self, request):
        items = self
        query_str = request.GET.get('query', None)
        branch_str = request.GET.get('branch', None)
        status_str = request.GET.get('status', None)

        if query_str:
            items = items.filter(name__icontains=query_str.strip())
        if status_str:
            items = items.filter(status=status_str.upper().strip())
        if branch_str:
            items = items.filter(staff_union__icontains=branch_str.strip())
        return items


class StaffEmployeeSubscriptionQuerySet(models.QuerySet):

    def filter_query_params(self, request):
        items = self
        staff_name_str = request.GET.get('staff_name', None)
        staff_status_str = request.GET.get('staff_status', None)
        valid_from_str = request.GET.get('valid_from', None)
        valid_to_str = request.GET.get('valid_to', None)
        staff_employee_str = request.GET.get('staff_employee', None)
        # staff_name_str = request.GET.get('staff_name', None)
        payment_status_str = request.GET.get('payment_status', None)

        # ---ID FILTERS---
        if staff_employee_str:
            items = items.filter(staff_employee__pk=int(staff_employee_str.strip()))

        # ---String search---
        if staff_name_str:
            items = items.filter(staff_employee__name__icontains=staff_name_str.strip())
        if staff_status_str:
            items = items.filter(staff_employee__status=staff_status_str.upper().strip())

        # ---DATE FILTERS---
        if valid_from_str and valid_to_str:
            valid_from = datetime.strptime(valid_from_str, "%Y-%m-%d")
            valid_to = datetime.strptime(valid_to_str, "%Y-%m-%d")
            items = items.filter(valid_from__gte=valid_from, valid_to__lte=valid_to)

        if valid_from_str and not valid_to_str:
            valid_from = datetime.strptime(valid_from_str, "%Y-%m-%d")
            items = items.filter(valid_from__gte=valid_from)

        # ---PAYMENT STATUS---
        if payment_status_str:
            payment_status = payment_status_str.strip().upper()
            items = items.filter(subscription_payment_status=payment_status)

        return items