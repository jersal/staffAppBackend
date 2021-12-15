from django.db import models


class SubscriptionPaymentQuerySet(models.QuerySet):

    def filter_query_params(self, request):
        items = self
        return items


class SubscriptionPaymentHistoryQuerySet(models.QuerySet):

    def filter_query_params(self, request):
        items = self
        return items
