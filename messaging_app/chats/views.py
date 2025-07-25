from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant



class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['conversation_id']
    ordering = ['-conversation_id']

    def get_queryset(self):
        return self.queryset.filter(participants__in=[self.request.user])

    def perform_create(self, serializer):
        participant_ids = self.request.data.get('participants', [])
        if str(self.request.user.id) not in participant_ids:
            participant_ids.append(str(self.request.user.id))

        participants = User.objects.filter(id__in=participant_ids)
        serializer.save()
        serializer.instance.participants.set(participants)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']


    def get_queryset(self):
        return self.queryset.filter(conversation__participants__in=[self.request.user])

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise ValidationError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
