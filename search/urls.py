from django.urls import path

from . import views

urlpatterns = [
    # path('', views.search, name='search') # Using  elasticsearch
    path('', views.SearchView.as_view(), name='search')
]