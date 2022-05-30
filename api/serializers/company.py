from rest_framework.serializers import ModelSerializer
from .user import UserSerializer
from ..models import Company

class CompanySerializer(ModelSerializer):
    user_data = UserSerializer(source='user')
    class Meta:
        model = Company
        exclude = ['user']
