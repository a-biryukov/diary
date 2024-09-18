
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import User


def email_send(obj, password=None, url=None, fail_silently=True):
    """Функция отправки сообщений по электронной почте"""
    if isinstance(obj, User) and password:
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль: {password}'
        recipient_list = [obj.email]
    elif isinstance(obj, User) and url:
        subject = 'Подтверждение почты'
        message = f'Перейдите по ссылке для подтверждения почты {url}'
        recipient_list = [obj.email]

    server_response = send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=fail_silently
    )
    if not fail_silently:
        return server_response


def user_verify(user, host) -> None:
    """Делает неактивным нового пользователя, создает токен и отправляет письмо со ссылкой для верификации на почту"""
    user.is_active = False
    user.make_token()
    user.save()
    url = f'http://{host}/email-confirm/{user.token}/'
    email_send(user, url=url)


def pass_recovery(email) -> None:
    """Устанавливает пользователю случайный пароль и отправляет его на почту"""
    user = User.objects.get(email=email)
    password = user.set_password()
    user.save()
    email_send(user, password=password)
