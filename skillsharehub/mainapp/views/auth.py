from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

import logging

from ..serializers import UserRegistrySerializer, UserSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrySerializer

    def post(self, request):
        serializer = UserRegistrySerializer(data=request.data)
        logger.info("RegisterView POST request data: %s", request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = RefreshToken.for_user(user)
            logger.info("Token generated for user: %s", user.id)

            user_data = UserSerializer(user).data
            logger.info("User data serialized for user: %s", user.id)

            return Response(data={
                "user": user_data,
                "token": str(token.access_token),
                "refresh": str(token)
            }, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
