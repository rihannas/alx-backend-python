# views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.db.models import Prefetch

from .models import Message

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    print('User deleted')
    return redirect('goodbye')  # Replace with your homepage or goodbye page

def user_sent_messages(request):
    messages = Message.objects.filter(sender=request.user) \
        .select_related('receiver', 'parent_message') \
        .prefetch_related('replies')

    context = {
        'messages': messages
    }
    return render(request, 'messaging/sent_messages.html', context)

def get_all_replies(message):
    replies = []

    def _fetch_replies(msg):
        children = msg.replies.all()
        for child in children:
            replies.append(child)
            _fetch_replies(child)

    _fetch_replies(message)
    return replies

def display_threaded_messages(messages, level=0):
    for msg in messages:
        print(" " * (level * 4) + f"{msg.sender}: {msg.content}")
        display_threaded_messages(msg.replies.all(), level + 1)

def unread_inbox(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})