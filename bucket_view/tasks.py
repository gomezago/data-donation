from celery import shared_task
from django.core.mail import EmailMessage

@shared_task()
def add(x,y):
    return x+y

@shared_task()
def send_email_task(subject, message, sender_email, recipient_list):
    print('Sending Email')
    email_msg = EmailMessage(subject, message, sender_email, recipient_list)
    email_msg.content_subtype = 'html'
    email_msg.send()
    return 'Email Sent'