from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show conversations where the user is a participant
        return self.queryset.filter(participants__in=[self.request.user])

    def perform_create(self, serializer):
        # Automatically add the current user as a participant
        participants = self.request.data.get('participants', [])
        if str(self.request.user.id) not in participants:
            participants.append(str(self.request.user.id))
        serializer.save(participants=participants)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show messages from conversations the user is part of
        return self.queryset.filter(conversation__participants__in=[self.request.user])

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise ValidationError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
