from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from journals.models import User


def should_send_reminder(user):
    """Check if a reminder should be sent to the user."""
    return not user.has_logged_in_last_24_hours()

def send_reminder_email(user):
    """Send a reminder email to the user."""
    send_mail(
        'Daily Journal Reminder',
        'Hi there, it looks like you haven\'t filled in your journal in the last 24 hours. Don\'t forget to log in and keep your journal updated!',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

@shared_task
def send_reminder_emails():
    """Loop through users and send reminder email"""
    print("STARTED")
    users = User.objects.all()
    for user in users:
        if should_send_reminder(user):
            send_reminder_email(user)

    print("DONE")