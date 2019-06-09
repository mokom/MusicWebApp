from django_elasticsearch_dsl import DocType, Index
from music.models import Track, Album

tracks = Index('tracks')
albums = Index('albums')

@tracks.doc_type
class TrackDocument(DocType):
    class Meta:
        model = Track

        fields = [
            'title',
            'id',
            'slug'
        ]

@albums.doc_type
class AlbumDocument(DocType):
    class Meta:
        model = Album

        fields = [
            'title','slug', 'id'
        ]