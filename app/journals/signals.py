from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entry, Journal

@receiver(post_save, sender=Entry)
def update_experience_for_entry(sender, instance, created, **kwargs):
    """ Increment user experience points from creating an Entry """
    if created:
        profile = instance.journal.owner.profile
        profile.add_experience(50)
        profile.save()

@receiver(post_save, sender=Journal)
def update_experience_for_journal(sender, instance, created, **kwargs):
    """ Increment user experience points from creating a Journal """
    if created:
        
        profile = instance.owner.profile
        profile.add_experience(100)
        profile.save()