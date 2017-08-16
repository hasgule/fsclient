from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    username = models.CharField(max_length=30, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=100, default='')
    image = models.ImageField(blank=True, null=True, default=None)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'username'
    def time(self):
        return self.user.date_joined
    def __unicode__(self):
        return self.user

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True, null='True', blank='True')
    from_user = models.ForeignKey(User, related_name='creator')
    to_user = models.ForeignKey(User, related_name='receiver')
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message


class Display(models.Model):
    displayed_by = models.ForeignKey(User, blank=True, null=True, related_name='displayed_by')
    displayed = models.ForeignKey(User, blank=True, null=True, related_name='displayed')


class VenueSearch(models.Model):
    query = models.CharField(max_length=100)
    near = models.CharField(max_length=100)
    owner = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.query


class Venue(models.Model):
    venue_id = models.CharField(max_length=200, default='something')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)
    checkin_count = models.IntegerField()
    search_id = models.ForeignKey(VenueSearch)

    def __str__(self):
        return self.name