from itertools import count

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, RedirectView, ListView, CreateView, UpdateView, DeleteView

from actions.utils import create_action
from feedback.forms import CommentForm
from feedback.models import Comment, Like
from music.decorators import ajax_required
from .models import Track, Album, Playlist
from .forms import TrackForm, AlbumForm

@login_required
def index(request):
    tracks = Track.objects.all().exclude(album__isnull=False).order_by('-released')[:12]
    albums = Album.objects.order_by('-released')[:12]
    context = {
        'tracks': tracks,
        'albums': albums
    }
    return render(request, 'index.html', context)

# ALBUM CRUD
@login_required
def create_album(request):
    title = 'Create'
    upload = 'Upload your album'
    form = AlbumForm(request.POST or None, request.FILES or None)
    artist = get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.artist = artist
            new_album.save()
            create_action(request.user, 'uploaded a new album', new_album)
            return redirect(
                reverse(
                    "user_detail",
                    kwargs={
                        'username': artist
                    }
                )
            )
    else:
        form = AlbumForm(initial={'artist': request.user})
    context = {
        'title': title,
        'form': form,
        'upload': upload
    }
    return render(request, 'music/upload.html', context)


@login_required
def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug)
    tracks = Track.objects.filter()
    context = {
        'album': album,
        'tracks': tracks
    }
    return render(request, 'music/album/album_detail.html', context)


@login_required
def edit_album(request, slug):
    title = 'Update'
    upload = 'Edit your album'
    album = get_object_or_404(Album, slug=slug)
    form = AlbumForm(request.POST or None, request.FILES or None, instance=album)
    artist = request.user
    if request.method == 'POST':
        if form.is_valid():
            form.instance.artist = artist
            form.save()
            return redirect(
                reverse(
                    "user_detail",
                    kwargs={
                        'username': artist
                    }
                )
            )
    context = {
        'title': title,
        'form': form,
        'upload': upload
    }
    return render(request, 'music/upload.html', context)


@login_required
def delete_album(request, slug):
    album = get_object_or_404(Album, slug=slug)
    album.delete()
    return redirect(
        reverse(
            "user_detail",
            kwargs={
                'username': album.artist
            }
        )
    )



# Track CRUD
@login_required
def create_track(request):
    title = 'Create'
    upload = 'Upload your single'
    form = TrackForm(request.POST or None, request.FILES or None)
    artist = get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        if form.is_valid():
            new_single = form.save(commit=False)
            new_single.artist = artist
            new_single.save()
            create_action(request.user, 'uploaded a new single', new_single)
            return redirect(
                reverse(
                    "user_detail",
                    kwargs={
                        'username': artist
                    }
                )
            )
    context = {
        'title': title,
        'form': form,
        'upload': upload
    }
    return render(request, 'music/upload.html', context)


@login_required
def create_track_album(request, slug):
    title = 'Add track to album'
    upload = 'Upload track'
    album = get_object_or_404(Album, slug=slug)
    form = TrackForm(request.POST or None, request.FILES or None)
    artist = get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.artist = artist
            form.instance.album = album
            form.instance.thumbnail = album.thumbnail
            print(form.instance)
            form.save()
            return redirect(
                reverse(
                    "album_detail",
                    kwargs={
                        'slug': slug
                    }
                )
            )
    else:
        form = TrackForm(initial={'thumbnail': album.thumbnail})
    context = {
        'title': title,
        'form': form,
        'upload': upload
    }
    return render(request, 'music/upload.html', context)



@login_required
def edit_track(request, slug):
    title = 'Update'
    upload = 'Edit track'
    track = get_object_or_404(Track, slug=slug)
    form = TrackForm(request.POST or None, request.FILES or None, instance=track)
    artist = request.user
    if request.method == 'POST':
        if form.is_valid():
            form.instance.artist = artist
            form.save()
            return redirect(
                reverse(
                    "user_detail",
                    kwargs={
                        'username': artist
                    }
                )
            )
    context = {
        'title': title,
        'form': form,
        'upload': upload
    }
    return render(request, 'music/upload.html', context)


@login_required
def track_detail(request, slug):
    track = get_object_or_404(Track, slug=slug)
    playlists = Playlist.objects.all().filter(owner=request.user)
    # comments = track.comments
    initial_data = {
        "content_type": track.get_content_type_comment,
        "object_id": track.id
    }
    print("hello")

    comments = track.comments[:3]
    print(track.comments)
    print(track.comments.count())

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        print(form.cleaned_data)
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
            author=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        'form': form,
        'track': track,
        'playlists': playlists,
        'comments': comments
    }

    return render(request, 'music/track_detail.html', context)


@login_required
def delete_track(request, slug):
    track = get_object_or_404(Track, slug=slug)
    track.delete()
    if track.album:
        return redirect(
            reverse(
                "album_detail",
                kwargs={
                    'slug': track.album.slug
                }
            )
        )
    else:
        return redirect(
            reverse(
                "user_detail",
                kwargs={
                    'username': track.artist
                }
            )
        )


@login_required
def album_list(request):
    queryset = Album.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 18)
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
    context ={
        "queryset": albums
    }
    return render(request, 'music/album/album_list.html', context)


# Playlist CRUD
class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerPlaylistMixin(OwnerMixin):
    model = Playlist


class OwnerPlaylistEditMixin(OwnerPlaylistMixin, OwnerEditMixin):
    fields = ['name']
    success_url = reverse_lazy('index')
    template_name = "music/playlist/playlist_create.html"


class ManagePlaylistListView(LoginRequiredMixin, OwnerPlaylistMixin, ListView):
    template_name = 'music/playlist/playlist_list.html'


class PlaylistCreateView(LoginRequiredMixin, OwnerPlaylistEditMixin, CreateView):
    pass


class PlaylistDetail(DetailView):
    model = Playlist
    template_name = 'music/playlist/playlist_detail.html'


class PlaylistUpdateView(LoginRequiredMixin, OwnerPlaylistEditMixin, UpdateView):
    pass


class PlaylistDeleteView(LoginRequiredMixin, OwnerPlaylistMixin, DeleteView):
    model = Playlist
    template_name = 'music/playlist/playlist_delete.html'
    success_url = reverse_lazy('manage_playlist_list')


class AddToPlaylist(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, track, playlist, *args, **kwargs):
        print(type(track))
        track = get_object_or_404(Track, id=track)
        playlist = get_object_or_404(Playlist, id=playlist)
        track.playlist.add(playlist)
        return reverse(
            'track_detail',
            kwargs={
                'slug': track.slug
            }
        )


class RemoveFromPlaylist(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, track, playlist, *args, **kwargs):
        playlist = get_object_or_404(Playlist, id=playlist)
        track = get_object_or_404(Track, id=track)
        playlist.track_set.remove(track)
        return reverse(
            'playlist_detail',
            kwargs={
                'slug': playlist.slug
            }
        )


def favorite_track(request, slug):
    track = get_object_or_404(Track, slug=slug)
    try:
        if track.is_favorite:
            track.is_favorite = False
        else:
            track.is_favorite = True
        track.save()
    except (KeyError, Track.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, slug):
    album = get_object_or_404(Album, slug=slug)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

@ajax_required
@login_required
@require_POST
def track_like(request, slug):
    track = get_object_or_404(Track, slug=slug)
    action = request.POST.get('action')
    print(track)
    print(action)
    if track and action:
        try:
            if action == 'like':
                Like.objects.get_or_create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(track),
                    object_id=track.id
                )
                create_action(request.user, 'likes track', track)
            else:
                Like.objects.filter(object_id=track.id).filter(user_id=request.user.id).delete()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
