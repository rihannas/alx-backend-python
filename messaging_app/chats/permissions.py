from rest_framework import permissions, SAFE_METHODS

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view or send messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users allowed globally
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Check if user is participant of the conversation

        # For Conversation instances
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message instances (or others) with conversation foreign key
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # Default deny
        return False
