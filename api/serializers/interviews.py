from rest_framework.serializers import ModelSerializer
from .vacancy import VacancySerializer
from .candidate import CandidateSerializer
from ..models import Interview

class InterviewSerializer(ModelSerializer):
    vacancy_data = VacancySerializer(source='vacancy')
    candidate_data = CandidateSerializer(source='candidate')
    class Meta:
        model = Interview
        exclude = ['vacancy', 'candidate']
