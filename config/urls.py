from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static



MEDIA_FILE_PATHS = static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

STATIC_FILE_PATHS = static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

# handler404 = 'music.views.handler404'
# handler500 = 'music.views.handler500'

urlpatterns = [
    path('', include('music.urls')),
    path('account/', include('account.urls')),
    path('search/', include('search.urls')),
    path('blog/', include("blog.urls")),
    path('tinymce/', include('tinymce.urls')),
    path('feedback/', include('feedback.urls')),
    path('admin/', admin.site.urls),

] + MEDIA_FILE_PATHS + STATIC_FILE_PATHS
