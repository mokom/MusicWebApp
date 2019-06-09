from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<slug>', views.post_detail, name='post_detail'),
    path('<slug:slug>/like', views.post_like, name='post_like'),
]