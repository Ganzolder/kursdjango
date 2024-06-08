from django.urls import path
from main.apps import MainConfig
from main.views import RecipientCreateView, MessageCreateView, PostCreateView, IndexView, RecipientDetailView, \
    MessageDetailView, PostDetailView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('recipient_add/', RecipientCreateView.as_view(), name='recipient_form'),
    path('recipient/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('message_add/', MessageCreateView.as_view(), name='message_form'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('post_add/', PostCreateView.as_view(), name='post_form'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
