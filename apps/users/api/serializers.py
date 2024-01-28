from rest_framework import serializers
from apps.users.models import User
from apps.users.use_cases import UserExistsUseCase, UserCreateUseCase, UserUpdateUseCase, UserPasswordSetUseCase


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'email', 'name', "password", "password2"]

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        request = self.context.get('request')
        company_id = request.META.get('HTTP_COMPANY')

        if password != password2:
            raise serializers.ValidationError({'password': ['two password are not same']})

        if UserExistsUseCase({'company_id': company_id, 'email': self.validated_data['email']}).execute():
            raise serializers.ValidationError({'email': ['user with this email already exits']})

        account = UserCreateUseCase(
            {
                'email': validated_data['email'],
                'name': validated_data['name'],
                'phone': request.data.get('phone', None),
                'company_id': company_id,
            }
        ).execute()

        # account.set_password(password)
        UserPasswordSetUseCase(account, password).execute()

        return account

    def update(self, instance, validated_data):
        UserUpdateUseCase(instance, {
            'name': validated_data.get('name', instance.name),
        }).execute()
        return instance


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
