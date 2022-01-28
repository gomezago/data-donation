from celery import shared_task
from django.core.mail import send_mail

@shared_task()
def add(x,y):
    return x+y

@shared_task()
def send_email_task(subject, message, sender_email, recipient_list):
    print('Sending Email')
    send_mail(subject, message, sender_email, recipient_list, fail_silently=False)
    return 'Email Sent'