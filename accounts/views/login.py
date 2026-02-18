from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from applibs.logger import get_logger
from applibs.status import VALID_DATA_NOT_FOUND, INVALID_CREDENTIALS
from applibs.response import format_output_error, format_output_success

from accounts.models import User
from accounts.serializers import LoginSerializer

logger = get_logger(__name__)

class LoginAPIView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Login API Serializer Errors: %s", errors)
            return Response(
                format_output_error(VALID_DATA_NOT_FOUND, error=errors), status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = User.objects.email_exists(email)
        if not user:
            logger.error("User with the Following Email Does Not Exist: %s", email)
            return Response(
                format_output_error(INVALID_CREDENTIALS), status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data="New User Created Successfully", status=status.HTTP_201_CREATED
        )