from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import Blog
from .forms import BlogForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        context_data['objects_list'] = Blog.objects.all()
        return context_data


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blogs'


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'users.blog_create'
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')
