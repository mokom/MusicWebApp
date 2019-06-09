from django.urls import path, include

from . import views

urlpatterns = [
path('track/<slug>', views.track_comment_thread, name='track-comment-thread'),
path('<int:id>', views.comment_thread, name='comment-thread'),
# path('<slug>', views.comment_delete, name='comment_delete'),
]
