from django.db import transaction

from src.staff_subscriptions.models import StaffEmployee, StaffEmployeeSubscription
from src.utils.serializers import DynamicFieldsModelSerializer


class StaffEmployeeSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = StaffEmployee
        fields = '__all__'


class StaffEmployeeSubscriptionSerializer(DynamicFieldsModelSerializer):
    staff_employee_details = StaffEmployeeSerializer(source='staff_employee', read_only=True)

    class Meta:
        model = StaffEmployeeSubscription
        read_only_fields = ('subscription_payment_status', 'subsciption_last_paid_date',
                            'subscription_paid_amount', 'subscription_balance_amount')
        fields = [f.name for f in model._meta.fields] + [
            'subscription_payment_status', 'subsciption_last_paid_date',
             'subscription_paid_amount', 'subscription_balance_amount', 'staff_employee_details']

    # @transaction.atomic
    # def create(self, validated_data):
    #     staff_employee = validated_data['staff_employee']
    #     request = self.context.get('request')
    #     from src.staff_subscriptions.custom_mails import new_subscription_with_template
    #     new_subscription_with_template(staff_employee, request_headers=request.META)
    #     return super(StaffEmployeeSubscriptionSerializer, self).create(validated_data)
    #
    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     from src.staff_subscriptions.custom_mails import new_subscription_with_template
    #     new_subscription_with_template(instance.staff_employee, request_headers=request.META)
    #     return super(StaffEmployeeSubscriptionSerializer, self).update(instance, validated_data)


