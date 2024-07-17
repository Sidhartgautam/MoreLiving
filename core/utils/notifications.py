from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(user_email, message):
    subject = 'New Notification'
    email_message = f'You have a new notification: {message}'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, email_message, email_from, recipient_list)
