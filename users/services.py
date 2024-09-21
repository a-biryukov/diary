import smtplib

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import User, Log


def email_send(obj, password=None, url=None):
    """Функция отправки сообщений по электронной почте"""
    if password:
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль: {password}'
        recipient_list = [obj.email]
    else:
        subject = 'Подтверждение почты'
        message = f'Перейдите по ссылке для подтверждения почты {url}'
        recipient_list = [obj.email]
    try:
        server_response = send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )
    except smtplib.SMTPException as e:
        server_response = e
        status = False
    else:
        status = True
    finally:
        Log.objects.create(status=status, server_response=server_response, user=obj)


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
