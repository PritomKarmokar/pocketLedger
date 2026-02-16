from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from accounts.models import User

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)

    def validate_email(self, value):
        if User.objects.email_exists(value):
            raise serializers.ValidationError(
                detail="An User With This Email Address Already Exists.",
                code="UAE_400"
            )
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            errors = e.messages
            raise serializers.ValidationError(
                detail=errors,
                code="INVP_400"
            )

        return value