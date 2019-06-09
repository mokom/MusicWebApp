from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from music.models import Track
from .models import Comment
from .forms import CommentForm

def track_comment_thread(request, slug):
    track = get_object_or_404(Track, slug=slug)
    track_comments = track.comments
    print(track_comments)
    initial_data = {
        "content_type": track.get_content_type_comment,
        "object_id": track.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")

        Comment.objects.get_or_create(
            author=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data
        )
        return redirect(
            reverse(
                "track-comment-thread",
                kwargs={
                    'slug': track.slug
                }
            )
        )
    context = {
        "track_comments": track_comments,
        "form": form
    }

    return render(request, "feedback/comments.html", context)


def comment_thread(request, id):
    comment = get_object_or_404(Comment, id=id)
    content_object = comment.content_object# Post that the comment is on
    content_id = comment.content_object.id

    initial_data = {
        "content_type": comment.content_type,
        "object_id": comment.object_id
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try: # ensure we have a parent id in the form being submitted
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id: # ensures parent exists in db
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        Comment.objects.get_or_create(
            author=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data,
            parent = parent_obj
        )
        return redirect(
            reverse(
                "comment-thread",
                kwargs={
                    'id': comment.id
                }
            )
        )
    context = {
        "comment": comment,
        "form": form
    }
    return render(request, "feedback/comment_thread.html", context)
