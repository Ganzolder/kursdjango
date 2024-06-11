from django.urls import path
from main.apps import MainConfig
from main.views import RecipientCreateView, MessageCreateView, PostCreateView, IndexView, RecipientDetailView, \
    MessageDetailView, PostDetailView, RecipientUpdateView, MessageUpdateView, PostUpdateView, \
    RecipientConfirmDeleteView, RecipientDeleteView, MessageConfirmDeleteView, MessageDeleteView, PostConfirmDeleteView, \
    PostDeleteView, PostLogsView, RecipientListAdminView, UserListAdminView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('recipient_add/', RecipientCreateView.as_view(), name='recipient_form'),
    path('recipient/detail/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/delete/confirm/<int:pk>/', RecipientConfirmDeleteView.as_view(), name='recipient_confirm_delete'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
    path('recipient/list/', RecipientListAdminView.as_view(), name='recipient_list'),

    path('message_add/', MessageCreateView.as_view(), name='message_form'),
    path('message/detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/confirm/<int:pk>/', MessageConfirmDeleteView.as_view(), name='message_confirm_delete'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('post_add/', PostCreateView.as_view(), name='post_form'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/edit/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/confirm/<int:pk>/', PostConfirmDeleteView.as_view(), name='post_confirm_delete'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),

    path('post_logs/', PostLogsView.as_view(), name='post_logs'),
    path('user/list/', UserListAdminView.as_view(), name='user_list'),
]
