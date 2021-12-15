from django.db import models
from django.db.models import Sum

from src.staff_subscriptions.managers import StaffEmployeeQuerySet, StaffEmployeeSubscriptionQuerySet
from src.utils.models import AbstractTimeStampModel, AbstractValidityModel


class StaffEmployee(AbstractTimeStampModel):
    STAFF_STATUSES = (('ACTIVE', 'ACTIVE'), ('TRANSFERED', 'TRANSFERED'), ('REMOVED', 'REMOVED'))

    name = models.CharField(max_length=128)
    designation = models.CharField(max_length=256)
    department = models.CharField(max_length=256)
    staff_union = models.CharField(max_length=256, null=True, blank=True)
    nickname = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STAFF_STATUSES)
    email = models.EmailField(null=True, blank=True)

    objects = StaffEmployeeQuerySet.as_manager()

    def __str__(self):
        return self.name


class StaffEmployeeSubscription(AbstractTimeStampModel, AbstractValidityModel):
    PAYMENT_STATUSES = (('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'))

    staff_employee = models.ForeignKey(StaffEmployee, on_delete=models.CASCADE)
    category = models.CharField(max_length=128)
    subscription_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.0)
    subscription_payment_status = models.CharField(max_length=32, choices=PAYMENT_STATUSES, default='PENDING')

    objects = StaffEmployeeSubscriptionQuerySet.as_manager()

    def __str__(self):
        return '{}---{}---{}'.format(self.staff_employee.name, self.category, self.subscription_amount)

    # @property
    # def subscription_payment_status(self):
    #     subscription_status = 'PENDING'
    #     try:
    #         subscription_status = self.staff_subscription_payment.all().order_by(
    #             '-created_on').first().status
    #     except:
    #         pass
    #     return subscription_status

    @property
    def subsciption_last_paid_date(self):
        subscription_last_paid = None
        try:
            subscription_last_paid = self.staff_subscription_payment.all().order_by(
                '-created_on').first().payment_date
        except:
            pass
        return subscription_last_paid


    @property
    def subscription_paid_amount(self):
        subscription_paid_amount = 0.0
        try:
            subscription_paid_amount = self.staff_subscription_payment.all().aggregate(
                Sum('payment_amount'))['payment_amount__sum']
        except:
            pass
        return subscription_paid_amount

    @property
    def subscription_balance_amount(self):
        subscription_balance_amount = self.subscription_amount
        try:
            subscription_balance_amount = self.subscription_amount - self.staff_subscription_payment.all().aggregate(
                Sum('payment_amount'))['payment_amount__sum']
        except:
            pass
        return subscription_balance_amount

