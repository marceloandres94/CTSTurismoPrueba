from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_verification_email_task(email, verification_link):
    """
    Tarea asíncrona para enviar correos electrónicos de verificación.
    """
    send_mail(
        'Verificación de correo electrónico',
        f'Haga clic en el siguiente enlace para verificar su correo electrónico: {verification_link}',
        'no-reply@hotel.com',
        [email],
        fail_silently=False,
    )
