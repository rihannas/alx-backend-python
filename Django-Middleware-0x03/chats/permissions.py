from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipant(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view or send messages, with explicit checks for PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Allow safe methods (GET, HEAD, OPTIONS) if user is participant
        if request.method in SAFE_METHODS:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
            return False

        # Explicitly check for write methods PUT, PATCH, DELETE
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
            return False

        # For other methods (POST etc.), also require participant status
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        return False
