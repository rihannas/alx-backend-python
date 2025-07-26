from django.urls import path, include

from rest_framework_nested.routers import NestedDefaultRouter, DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Main router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router: messages under conversations
convo_messages_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_messages_router.urls)),

]
