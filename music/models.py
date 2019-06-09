from uuid import uuid4

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from tinymce import models as tinymyce_models
from django.utils.text import slugify

from feedback.models import Comment, Like


def media_directory_with_uuid(instance, filename):
    return '{}/{}'.format(instance.id, uuid4())


STATUS_CHOICES = (
        ('afrobeat', 'AfroBeat'),
        ('hip hop', 'Hip Hop'),
        ('r&b', 'R&B'),
        ('pop', 'Pop'),
        ('gospel', 'Gospel'),
        ('soul', 'Soul'),
        ('n/a', 'N/A')
    )

class AlbumQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(slug__icontains=query) |
                         Q(artist__username__icontains =query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs

class AlbumManager(models.Manager):
    def get_queryset(self):
        return AlbumQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Album(models.Model):
    title = models.CharField(max_length=100, null=False)
    slug = models.SlugField(max_length=100)
    released = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=media_directory_with_uuid, blank=True)
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.CharField(choices=STATUS_CHOICES, max_length=15, default='n/a')
    is_favorite = models.BooleanField(default=False)

    objects = AlbumManager()

    class Meta:
        ordering = ('released',)

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "album_detail",
            kwargs={
                "slug": self.slug
            }
        )

    def get_update_url(self):
        return reverse(
            "update_album",
            kwargs={
                "slug": self.slug
            }
        )

    def get_delete_url(self):
        return reverse(
            "delete_album",
            kwargs={
                "slug": self.slug
            }
        )

class Playlist(models.Model):
    name = models.CharField(max_length=100, help_text="Enter a name for your playlist")
    slug = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Playlist, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'playlist_detail',
            kwargs= {
                'slug': self.slug
            }
        )

    def __str__(self):
        return self.user.username

class MusicBase(models.Model):
    title = models.CharField(max_length=150, null=False)
    slug = models.SlugField(max_length=150)
    duration = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ('title',)


class TrackQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs

class TrackManager(models.Manager):
    def get_queryset(self):
        return TrackQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Track(MusicBase):
    audio_file = models.FileField(upload_to=media_directory_with_uuid)
    released = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=media_directory_with_uuid, blank=True)
    genre = models.CharField(choices=STATUS_CHOICES, max_length=15, default='n/a')
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    playlist = models.ManyToManyField(Playlist, blank=True) # related manager is track_set
    is_favorite = models.BooleanField(default=False)
    lyrics = tinymyce_models.HTMLField(null=True, blank=True)
    video_file = models.FileField(upload_to=media_directory_with_uuid, blank=True, null=True)

    objects = TrackManager()

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Track, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'track_detail',
            kwargs= {
                'slug': self.slug
            }
        )

    @property
    def likes(self):
        qs = Like.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type_like(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type

    @property
    def comments(self):
        qs = Comment.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type_comment(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type

'''
 Not used. Changed my original design plan. 
 But you can remove the video_file attr from the Track class to use this video class
'''

#
# class Video(MusicBase):
#     file = models.FileField(upload_to='video/{}'.format(media_directory_with_uuid))
#     track = models.ForeignKey(Track, on_delete=models.DO_NOTHING, related_name='music_video')
#
#     def __str__(self):
#         return '{}'.format(self.track)
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super(Video, self).save(*args, **kwargs)
