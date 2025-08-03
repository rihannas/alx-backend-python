from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

        print(f"📢 Notification for {instance.receiver.username}")


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Message.objects.get(pk=instance.pk)
        if old_instance.content != instance.content:
            MessageHistory.objects.create(
                message=old_instance,
                old_content=old_instance.content
            )
            instance.edited = True

        print(f"📢{instance.sender.username} edited message")

@receiver(post_delete, sender=User)
def delete_related_histories(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(user=instance).delete()
    # to clean up histories where user was editor
    MessageHistory.objects.filter(edited_by=instance).delete()
    print('editer deleted')
