import django_filters
from django_filters.rest_framework import FilterSet, filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(FilterSet):
    # Filter messages by conversation participants (filter conversations having a specific user)
    participant = filters.ModelChoiceFilter(
        field_name='conversation__participants',
        queryset=User.objects.all(),
        label='Conversation Participant'
    )
    # Filter messages by sent_at datetime range
    sent_at__gte = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at__lte = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant', 'sent_at__gte', 'sent_at__lte']
