from rest_framework import serializers

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
