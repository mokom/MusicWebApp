from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.functions import datetime
from django.urls import reverse
from tinymce import models as tinymyce_models
from django.utils.text import slugify
from taggit.managers import TaggableManager

from feedback.models import Comment, Like


class PostView(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    ip = models.CharField(max_length=50, default=0)
    session = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class PostQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(slug__icontains=query) |
                         Q(tags__name__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=120, unique_for_date='timestamp')
    content = tinymyce_models.HTMLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail = models.ImageField(blank=False, null=False)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    tags = TaggableManager()

    objects = PostManager()


    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'post_detail',
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
    def view_count(self):
        # grab all the postView objects and filter where post == self.post
        return PostView.objects.filter(post=self).count()

    @property
    def comments(self):
        qs = Comment.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type_comment(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type

    @property
    def get_content_type_likes(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type
