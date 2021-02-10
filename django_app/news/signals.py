from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User, Comment


@receiver(pre_save, sender=User)
def user_change_is_banned(sender, instance, *args, **kwargs):
    """
    Оповещение пользователя по почте при изменении статуса 'is_banned'
    """

    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # При создании нового пользователя ничего не делаем
    else:
        if obj.is_banned != instance.is_banned:
            if instance.is_banned:
                subject = 'Ваша учетная запись заблокирована!'
                message = 'Теперь вам запрещено оставлять комментарии.'
            else:
                subject = 'Ваша учетная запись разблокирована!'
                message = 'Теперь вам разрешено оставлять комментарии.'
            print(subject, message)
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
            )


@receiver(post_save, sender=Comment)
def comment_create(sender, instance, *args, **kwargs):
    """
    Оповещение пользователя по почте об ответах на его комментарии
    """

    if instance.parent:
        subject = 'Вам ответили в комментариях к статье {}'.format(
            instance.article.title
        )
        message = (
            'Ваш комментарий от {:%Y.%m.%d %H:%M:%S}: {}\n '
            'Ответ пользователя {}: {}'
        ).format(
            instance.parent.created_at, instance.parent.content,
            instance.author.username, instance.content
        )
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.parent.author.email],
            fail_silently=False,
        )
