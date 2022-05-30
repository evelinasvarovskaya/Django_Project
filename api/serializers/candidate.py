from rest_framework.serializers import ModelSerializer
from .user import UserSerializer
from ..models import Candidate

class CandidateSerializer(ModelSerializer):
    user_data = UserSerializer(source='user')
    class Meta:
        model = Candidate
        exclude = ['user']
