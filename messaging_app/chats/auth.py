from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend this class to customize token behavior if needed.
    """
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        # Add logging, activity tracking, role checks here if needed
        return user
