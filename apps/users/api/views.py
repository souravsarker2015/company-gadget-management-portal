import requests
from rest_framework import status
from .serializers import RegistrationSerializer, CustomLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.views import TokenView
from django.contrib.auth import get_user_model
import dotenv
import os
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from ..use_cases import TokenDeleteUseCase, UserDetailsUseCase

from ...company.utils import company_id_header_params

dotenv.load_dotenv()


class CustomTokenView(TokenView):
    def validate_user(self, email, password, company_id):

        User = get_user_model()

        try:
            user = UserDetailsUseCase({'email': email, 'company_id': company_id}).execute()
        except User.DoesNotExist:
            return False

        if not user.check_password(password):
            return False

        if not user.is_active:
            return False
        return True

    def create_token_response(self, request):
        email = request.POST.get('username')
        password = request.POST.get('password')
        company_id = request.POST.get('company_id')

        if not self.validate_user(email, password, company_id):
            return self.error_response('Invalid user credentials')

        return super().create_token_response(request)


def get_access_token_from_refresh_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'client_id': os.environ.get('OAUTH2_PROVIDER_CLIENT_ID'),
        'client_secret': os.environ.get('OAUTH2_PROVIDER_CLIENT_SECRET'),
        'refresh_token': refresh_token
    }
    auth_service_url = os.environ.get('CUSTOM_AUTH_BACKEND_URL')
    auth_verify_url = f'{auth_service_url}o/token/'
    response = requests.post(auth_verify_url, data=data)
    response_data = response.json()
    return response_data


class RegistrationView(APIView):
    @swagger_auto_schema(
        tags=["Login, Registration"],
        manual_parameters=company_id_header_params(),
        request_body=RegistrationSerializer
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data, context={'request': request})
        req_data = self.request.data
        try:
            if serializer.is_valid():
                user = serializer.save()
                company_id = request.META.get('HTTP_COMPANY', None)
                if company_id:
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'company': company_id,
                    }
                    data = {
                        'grant_type': 'password',
                        'username': req_data.get('email'),
                        'password': req_data.get('password'),
                        'company_id': company_id,
                        'client_id': os.environ.get('OAUTH2_PROVIDER_CLIENT_ID'),
                        'client_secret': os.environ.get('OAUTH2_PROVIDER_CLIENT_SECRET')
                    }
                    auth_service_url = os.environ.get('CUSTOM_AUTH_BACKEND_URL')
                    auth_verify_url = f'{auth_service_url}/token2/'

                    response = requests.post(auth_verify_url, data=data, headers=headers)

                    data = {
                        'message': 'User registered successfully.',
                        'access_response': response.json(),
                        'status': status.HTTP_201_CREATED,
                        'id': user.id,
                        'email': user.email,
                        'name': user.name,
                    }
                    return Response(data)
                return Response({
                    "error": "Company Id is required for registration",
                    "status": 401
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "error": str(e),
                "status": 500
            })


class CustomLoginView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=["Login, Registration"],
        manual_parameters=company_id_header_params(),
        request_body=CustomLoginSerializer
    )
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            serializer = CustomLoginSerializer(data=request.data)
            if serializer.is_valid():
                company_id = request.META.get('HTTP_COMPANY')
                user = UserDetailsUseCase({
                    'email': username,
                    'company_id': company_id,
                }).execute()

                if user:
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'company': None if user.is_superuser else company_id,
                    }
                    data = {
                        'grant_type': 'password',
                        'username': username,
                        'password': password,
                        'company_id': None if user.is_superuser else company_id,
                        'client_id': os.environ.get('OAUTH2_PROVIDER_CLIENT_ID'),
                        'client_secret': os.environ.get('OAUTH2_PROVIDER_CLIENT_SECRET')
                    }
                    auth_service_url = os.environ.get('CUSTOM_AUTH_BACKEND_URL')
                    auth_verify_url = f'{auth_service_url}/token2/'

                    response = requests.post(auth_verify_url, data=data, headers=headers)

                    if 200 <= response.status_code < 300:
                        res = response.json()
                        serializer = RegistrationSerializer(user)
                        serialized_data = serializer.data

                        combined_dict = {}

                        user_details_info = {
                            "email": user.email,
                            "name": user.name,
                        }

                        combined_dict.update(user_details_info)

                        data = {
                            'status': status.HTTP_200_OK,
                            'access_response': res,
                            'user_info': combined_dict,
                            'app': request.META.get('HTTP_APP')
                        }

                    else:
                        data = {
                            'error': 'Invalid credentials!',
                            'status': status.HTTP_401_UNAUTHORIZED
                        }
                    return Response(data)

                else:
                    data = {
                        'error': 'Invalid credentials!!!',
                        'status': status.HTTP_401_UNAUTHORIZED
                    }
                    return Response(data)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'error': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            })


class CustomLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["Login, Registration"],
    )
    def post(self, request):
        try:
            token = request.auth
            if token:
                TokenDeleteUseCase(token).execute()
            return Response({
                'message': 'Logged out successfully',
                'status': status.HTTP_200_OK
            })

        except Exception as e:
            return Response({
                'error': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            })



