from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.TextField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField(max_length=20, blank=True)
    status = models.PositiveSmallIntegerField(default=1)
    valid_till = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "token"