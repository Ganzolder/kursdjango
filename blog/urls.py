from django.urls import path
from django.views.decorators.cache import cache_page

from .views import BlogListView, BlogDetailView, BlogCreateView

app_name = 'blog'

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog_list'),
    path('detail/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
]
