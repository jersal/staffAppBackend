from src.payments.models import SubscriptionPayment
from src.utils.serializers import DynamicFieldsModelSerializer


class SubscriptionPaymentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = SubscriptionPayment
        fields = '__all__'

