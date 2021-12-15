from src.accounts.models import AuthUser
from src.utils.serializers import DynamicFieldsModelSerializer


class AuthUserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = AuthUser
        fields = '__all__'

