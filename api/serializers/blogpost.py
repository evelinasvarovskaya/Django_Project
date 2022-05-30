from rest_framework.serializers import ModelSerializer
from .company import CompanySerializer
from ..models import BlogPost

class BlogPostSerializer(ModelSerializer):
    company_data = CompanySerializer(source='company')
    class Meta:
        model = BlogPost
        exclude = ['company']
