 from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound, ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Candidate, Company, User
from ..serializers.user import UserSerializer
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from ..serializers.candidate import CandidateSerializer
from ..serializers.company import CompanySerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='register/candidate')
    def register_candidate(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        if len(password) < 8:
            raise ValidationError({'password': ['Password is too short']})

        serializer.save()

        if 'first_name' not in request.data:
            raise ParseError({'message': 'first name cannot be empty'})
        if 'middle_name' not in request.data:
            raise ParseError({'message': 'middle name cannot be empty'})
        if 'last_name' not in request.data:
            raise ParseError({'message': 'last name cannot be empty'})
        first_name = request.data['first_name']
        middle_name = request.data['middle_name']
        last_name = request.data['last_name']

        try:
            user=User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound({'message': 'User not found'})
        company = Candidate.objects.create(user=user, first_name=first_name, middle_name=middle_name, last_name=last_name)
        company.save()

        return Response({'message': 'success'}, status=HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, url_path='register/company')
    def register_company(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        if len(password) < 8:
            raise ValidationError({'password': ['Password is too short']})

        serializer.save()

        if 'company_name' not in request.data:
            raise ParseError({'message': 'company name cannot be empty'})
        print(request.data)
        company_name = request.data['company_name']
        print(company_name)
        try:
            user=User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound({'message': 'User not found'})
        company = Company.objects.create(user=user, company_name=company_name)
        company.save()

        return Response({'message': 'success'}, status=HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        if 'email' not in request.data:
            data = {'email': ['Email must be provided']}
            if 'password' not in request.data:
                data['password'] = ['Password must be provided']
            raise ValidationError(data)
        if 'password' not in request.data:
            raise ValidationError({'password': ['Password must be provided']})

        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            raise NotFound({'message': 'User with provided credentials does not exist'})

        if not user.check_password(request.data.get('password')):
            raise AuthenticationFailed({'message': 'Incorrect password'})

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie('refresh', str(refresh))
        response.data = {'access': str(refresh.access_token)}
        return response

    @action(methods=['POST'], detail=False,
            permission_classes=[IsAuthenticated])
    def logout(self, request):
        response = Response()
        response.delete_cookie('refresh')
        response.data = {'message': 'success'}
        return response

    @action(methods=['GET'], detail=False,
        permission_classes=[IsAuthenticated])
    def user(self, request):
        user = request.user
        data = {'user': UserSerializer(user).data}
        try:
            candidate = Candidate.objects.get(user=user)
            data['candidate'] = CandidateSerializer(candidate).data
        except Candidate.DoesNotExist:
            company = Company.objects.get(user=user)
            data['company'] = CompanySerializer(company).data
        return Response(data)
