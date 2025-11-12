from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from skillsharehub.mainapp.models import CustomUser
from ..models import CustomUser


class UserRegistrySerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=18, allow_blank=False, write_only=True, required=True)
    password2 = serializers.CharField(max_length=18 , allow_blank=False, write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
        
    def create(self, validated_data):
        # Remove password2 and use the manager's create_user which will
        # properly set and hash the password via set_password().
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(
            email=validated_data.get('email'),
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

    class Meta:
        model = CustomUser
        fields = ("email", "password", "password2", "first_name", "last_name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "date_joined")