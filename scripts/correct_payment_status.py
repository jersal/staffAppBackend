from django.db.models import Sum

from src.staff_subscriptions.models import StaffEmployeeSubscription


def run():
    staff_subscriptions_qs = StaffEmployeeSubscription.objects.all()
    for item in staff_subscriptions_qs:
        paid_amount = item.staff_subscription_payment.all().aggregate(Sum('payment_amount'))['payment_amount__sum']
        if paid_amount and paid_amount == item.subscription_amount:
            item.subscription_payment_status = 'COMPLETED'
            item.save(update_fields=['subscription_payment_status'])
