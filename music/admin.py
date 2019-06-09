from django.contrib import admin
from .models import Album, Track,  Playlist


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'released')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'artist')
    search_fields = ('title', 'artist')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'released')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'artist', 'released')
    search_fields = ('title', 'artist')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')