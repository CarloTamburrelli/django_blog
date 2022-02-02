from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import os
import logging

logging.basicConfig(level=logging.INFO) # Here


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):

	    if not instance.pk:
	        return False

	    try:
	        old_file = Profile.objects.get(pk=instance.pk).image
	    except Profile.DoesNotExist:
	        return False
	    if old_file != 'default.jpg':
		    new_file = instance.image
		    if not old_file == new_file:
		        if os.path.isfile(old_file.path):
		            os.remove(old_file.path)


'''@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
		instance.profile.save()'''

'''
@receiver(pre_save, sender=Profile)
def before_save_profile(sender, instance, **kwargs):
		logging.info("Entro...")
		logging.info(kwargs)
		instance.image.delete()'''
