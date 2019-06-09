from itertools import chain

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from music.models import Track, Album
from account.models import Profile
from blog.models import Post

from .documents import TrackDocument, AlbumDocument

'''
Using Elastic Search
'''

# def search(request):
#     q = request.GET.get('q')
#
#     if q:
#         # tracks = TrackDocument.search().query("match", title=q)
#         tracks = TrackDocument.search().query("multi_match", query=q, fields=['title', 'slug']).to_queryset()
#         albums = AlbumDocument.search().query("multi_match", query=q, fields=['title', 'slug']).to_queryset()
#     else:
#         tracks = ''
#         albums = ''
#     context = {
#         'tracks': tracks,
#         'albums': albums,
#         'q': q
#     }
#     return render(request, 'search/search.html', context)


class SearchView(ListView):
    template_name = 'search/search.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            track_results = Track.objects.search(query=query)
            album_results = Album.objects.search(query=query)
            profile_results = Profile.objects.search(query=query)
            post_results = Post.objects.search(query=query)

            # combine querysets
            queryset_chain = chain(
                track_results,
                album_results,
                profile_results,
                post_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs) # Since qs is actually a list
            print(qs)
            return qs
        return Track.objects.none()
