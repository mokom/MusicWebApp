from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from taggit.models import Tag

from actions.utils import create_action
from feedback.forms import CommentForm
from feedback.models import Comment, Like
from music.decorators import ajax_required

from .models import Post, PostView


@login_required
def post_list(request, tag_slug=None):
    most_recent = Post.objects.order_by('-timestamp')[:3]
    queryset = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags__in=[tag])

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        "queryset": posts,
        "tag": tag,
        "most_recent": most_recent
    }
    return render(request, 'blog/post_list.html', context)


@login_required
def post_detail(request, slug):
    most_recent = Post.objects.order_by('-timestamp').exclude(slug=slug)[:3]
    post = get_object_or_404(Post, slug=slug)
    view = None
    if not PostView.objects.filter(post=post, session=request.session.session_key):
        view = PostView(post=post, ip=request.META['REMOTE_ADDR'], session=request.session.session_key)
        view.save()

    initial_data = {
        "content_type": post.get_content_type_comment,
        "object_id": post.id
    }

    comments = post.comments
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

        new_comment, created = Comment.objects.get_or_create(
            author=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data,
            parent = parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-timestamp')[:4]
    tag_count = Tag.objects.values('taggit_taggeditem_items').annotate(frequency=Count('taggit_taggeditem_items'))
    context = {
        "post": post,
        "similar_posts": similar_posts,
        "most_recent": most_recent,
        "tag_count": tag_count,
        "view": view,
        "comments": comments,
        "form": form

    }
    return render(request, 'blog/post_detail.html', context)



@ajax_required
@login_required
@require_POST
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    action = request.POST.get('action')
    if post and action:
        try:
            if action == 'like':
                Like.objects.get_or_create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.id
                )
                create_action(request.user, 'likes post', post)
            else:
                Like.objects.filter(object_id=post.id).filter(user_id=request.user.id).delete()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
