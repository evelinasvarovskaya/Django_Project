from rest_framework.viewsets import ModelViewSet
import django_filters.rest_framework as filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ..models import Company
from ..serializers.company import CompanySerializer

class CompanyViewSet(ModelViewSet):
    model = Company
    queryset = model.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['company_name']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            data = self.serializer_class(self.queryset.get(pk=pk)).data
            return Response(data)
        except self.model.DoesNotExist:
            raise NotFound({'message': 'Album was not found'})