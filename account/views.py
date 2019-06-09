from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST

from actions.models import Action
from actions.utils import create_action
from music.decorators import ajax_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from music.views import Album, Playlist, Track

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated Successfully")
            return redirect(
                reverse(
                    "user_detail",
                    kwargs={
                        'username': request.user
                    }
                )
            )
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit_profile.html', context)


@login_required
def user_list(request):
    queryset = User.objects.filter(is_active=True).exclude(username='admin')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 18)
    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        user = paginator.page(1)
    except EmptyPage:
        user = paginator.page(paginator.num_pages)
    context = {
        "queryset": user
    }
    return render(request, 'account/user/list.html', context)


@login_required
def user_detail(request, username):
    following_ids = request.user.profile.following.values_list('id', flat=True) # get the id values of followers
    actions = None
    if following_ids:
        # if user is following others, retrieve only their actions
        actions = Action.objects.exclude(user=request.user)
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    user = get_object_or_404(User, username=username, is_active=True)

    albums = Album.objects.all().filter(artist_id=user.id)
    tracks = Track.objects.all().filter(artist_id=user.id).exclude(album__isnull=False)
    playlists = Playlist.objects.all().filter(owner_id=user.id)
    context = {
        'user': user,
        'albums': albums,
        'tracks': tracks,
        'playlists': playlists,
        'actions': actions
    }
    return render(request, 'account/user/detail.html', context)


@ajax_required
@login_required
@require_POST
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    action = request.POST.get('action')
    if user and action:
        try:
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user.profile, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user.profile, user_to=user).delete()
                create_action(request.user, 'unfollowed', user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status':'ko'})
