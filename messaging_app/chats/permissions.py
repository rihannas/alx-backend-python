from rest_framework import permissions
from .models import Conversation


class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to view or send messages.
    """

    def has_object_permission(self, request, view, obj):
        # For Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        # For Conversation objects
        return request.user in obj.participants.all()
