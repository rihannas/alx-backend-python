from rest_framework import permissions, SAFE_METHODS
from .models import Conversation


class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to view or send messages.
    """

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return True
        return False


    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS (read-only)
        if request.method in SAFE_METHODS:
            return request.user in obj.conversation.participants.all()
        
        # Explicitly check for PUT, PATCH, DELETE
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()

        # POST or other methods can also be restricted if needed
        return request.user in obj.conversation.participants.all()
    
class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False