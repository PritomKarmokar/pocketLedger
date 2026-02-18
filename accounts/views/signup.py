from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from applibs.logger import get_logger
from applibs.response import format_output_error
from applibs.status import USER_SIGNUP_SUCCESS, USER_CREATION_FAILED, VALID_DATA_NOT_FOUND

from accounts.models import User
from accounts.serializers import SignUpSerializer

logger = get_logger(__name__)

class SignUpAPIView(APIView):
    permission_classes = []
    serializer_class = SignUpSerializer

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("SignUp Serializer Errors: %s", errors)
            return Response(
                format_output_error(VALID_DATA_NOT_FOUND, error=errors), status=status.HTTP_400_BAD_REQUEST
            )

        serializer_data = serializer.validated_data
        user = User.objects.create_user(**serializer_data)
        if not user:
            logger.error("Error Occurred While Creating A New User")
            return Response(
                USER_CREATION_FAILED, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            USER_SIGNUP_SUCCESS, status=status.HTTP_201_CREATED
        )