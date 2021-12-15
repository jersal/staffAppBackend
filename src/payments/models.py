from decimal import Decimal

from django.db import models, transaction

# Create your models here.
from django.db.models import Sum

from src.payments.managers import SubscriptionPaymentQuerySet, SubscriptionPaymentHistoryQuerySet
from src.staff_subscriptions.models import StaffEmployee, StaffEmployeeSubscription
from src.utils.models import AbstractTimeStampModel


class SubscriptionPayment(AbstractTimeStampModel):
    PAYMENT_STATUSES = (('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'))

    # staff_employee = models.ForeignKey(StaffEmployee, on_delete=models.CASCADE)
    staff_subscription = models.ForeignKey(StaffEmployeeSubscription, on_delete=models.CASCADE,
                                           related_name='staff_subscription_payment')
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.0)
    status = models.CharField(max_length=32, choices=PAYMENT_STATUSES, null=True, blank=True)

    objects = SubscriptionPaymentQuerySet.as_manager()

    def __str__(self):
        return '{}'.format(self.payment_amount)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:
            previous_paid = self.__class__.objects.filter(staff_subscription=self.staff_subscription).aggregate(
                previous_paid=Sum('payment_amount'))['previous_paid']
            if not previous_paid:
                previous_paid = Decimal(0.0)
            if (previous_paid + self.payment_amount) == self.staff_subscription.subscription_amount:
                self.status = 'COMPLETED'
                self.staff_subscription.subscription_payment_status = 'COMPLETED'
                self.staff_subscription.save(update_fields=['subscription_payment_status'])
            else:
                self.status = 'PENDING'

        return super(SubscriptionPayment, self).save(*args, **kwargs)


class SubscriptionPaymentHistory(AbstractTimeStampModel):
    PAYMENT_STATUSES = (('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'))

    staff_subscription = models.ForeignKey(StaffEmployeeSubscription, on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.0)
    status = models.CharField(max_length=32, choices=PAYMENT_STATUSES)

    objects = SubscriptionPaymentHistoryQuerySet.as_manager()

    def __str__(self):
        return self.payment_amount

