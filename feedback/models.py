from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class CommentManager(models.Manager):
    
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs
    
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True) # enables us toreference it inside of an instance itself
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp'] # newest show up first

    def __unicode__(self):
        return str(self.author.username)

    def __str__(self):
        return str(self.author.username)

    def get_absolute_url(self):
        return reverse(" comment-thread", kwargs={"id": self.id})

    def children(self): # replies
        return Comment.objects.filter(parent=self).order_by('timestamp')

    @property
    def is_parent(self):
        # if there is a parent value in this, then this comment is not the parent but rather a child
        if self.parent is not None:
            return False
        return True



class LikeManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(LikeManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_like')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = LikeManager()



