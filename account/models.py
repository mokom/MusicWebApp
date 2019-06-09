from uuid import uuid4

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse


def profile_photo_directory_with_uuid(instance, filename):
    return '{}/{}'.format(instance.id, uuid4())

class ProfileQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(user__username__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null='True')
    photo = models.ImageField(upload_to=profile_photo_directory_with_uuid, blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contact', related_name='followers', symmetrical=False)

    objects = ProfileManager()

    def __str__(self):
        # return 'Profile for user {}'.format(self.user)
        return '{}'.format(self.user.username)

    # def get_follow_url(self):
    #     return reverse(
    #         'follow-toggle',
    #         kwargs={
    #             'username': self.user.username
    #         }
    #     )


class Contact(models.Model):
    user_from = models.ForeignKey(Profile, related_name='rel_from_set', on_delete=models.CASCADE) # for user that creates the relationship
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE) # for user being followed
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)
