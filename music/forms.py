from django import forms
from tinymce.widgets import TinyMCE
from .models import Track, Album, Comment

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class AlbumForm(forms.ModelForm):
    artist = forms.HiddenInput(attrs={
        'name': 'artist',
        'required': False
    })

    class Meta:
        model = Album
        fields = ['title', 'thumbnail', 'genre']


class TrackForm(forms.ModelForm):
    lyrics = forms.CharField(widget=TinyMCE(
        mce_attrs={
            'required': False,
            'cols':30,
            'rows':10
        }, attrs={'required': True}
    ))
    album = forms.HiddenInput(attrs={
        'name': 'album',
        'required': False
    })

    class Meta:
        model = Track
        fields = ['title', 'duration', 'thumbnail', 'audio_file', 'video_file', 'genre', 'lyrics']
