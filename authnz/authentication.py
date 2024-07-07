from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        # Check if header has the right format
        header_parts = auth_header.split()
        if len(header_parts) != 2:
            raise AuthenticationFailed()

        # Get token type and value
        token_type, token_value = header_parts
        if token_type.lower() != "bearer":
            raise AuthenticationFailed()

        # Get user from token
        try:
            user = User.objects.get(api_token=token_value)
        except User.DoesNotExist:
            raise AuthenticationFailed()

        return user, None
