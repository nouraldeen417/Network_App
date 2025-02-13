from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

#@receiver(post_save, sender=User)
def notify_admin_on_registration(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        # Send email to admin
        send_mail(
            subject='New User Registration Pending Approval',
            message=f'User {instance.username} has registered and is awaiting approval.',
            from_email='your-email@example.com',
            recipient_list=['hishamhagag18@gmail.com'],  # Add admin email(s) here
        )

class Device(models.Model):
    uniqename = models.CharField (max_length=100,  unique=True)
    hostname  = models.CharField (max_length=100,  unique=True)
    ip        = models.CharField (max_length=15 ,  unique=True)

    def __str__(self):
        return self.uniqename
    