import smtplib

import pytz

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from django.core.mail import send_mail
from django.utils import timezone
import datetime as dt

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_datetime
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, DeleteView, ListView

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

import users
from main.forms import RecipientForm, MessageForm, PostForm
from main.models import Recipient, Message, Post, PostLogs
from django.utils.timezone import make_aware

from users.models import User


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['num_recipients'] = Recipient.objects.filter(creator=user).count()
        context['num_messages'] = Message.objects.filter(creator=user).count()
        context['num_posts'] = Post.objects.filter(creator=user).count()
        return context


class RecipientCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = Recipient

    form_class = RecipientForm

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('main:recipient_form')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Recipient.objects.filter(creator=self.request.user).order_by('-enabled')
        context_data['title'] = f'Список адресатов в базе'
        context_data['object_type'] = 'recipient'

        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'main/recipient_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        recipient = self.get_object()
        if recipient.enabled is True:
            context_data['enabled'] = 'Активен'
        else:
            context_data['enabled'] = 'Не активен'

        context_data['title'] = f'Адресат {recipient.name}'
        context_data['email'] = f'Почта {recipient.email}'
        context_data['text'] = f'{recipient.description}'
        context_data['creator'] = f'Автор: {recipient.creator}'

        return context_data


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('main:recipient_form')

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Recipient.objects.filter(creator=self.request.user).order_by('-enabled')
        context_data['title'] = f'Список адресатов в базе'
        context_data['object_type'] = 'recipient'
        # context_data['recipient_list'] = recipient_list
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient

    success_url = reverse_lazy('main:recipient_form')

    def post(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу (pk)
        obj = get_object_or_404(Recipient, pk=kwargs['pk'])

        # Удаляем объект
        obj.delete()

        # Перенаправляем на нужную страницу после удаления
        return redirect('main:recipient_form')


class RecipientConfirmDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'main/recipient_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(Recipient, pk=kwargs['pk'])
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    login_url = reverse_lazy('users:login')

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('main:message_form')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Message.objects.filter(creator=self.request.user).order_by('-enabled')
        context_data['title'] = f'Список адресатов в базе'
        context_data['object_type'] = 'message'

        return context_data


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('main:message_form')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Message.objects.filter(creator=self.request.user).order_by('-enabled')
        context_data['title'] = f'Список адресатов в базе'
        context_data['object_type'] = 'message'
        # context_data['recipient_list'] = recipient_list
        return context_data


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'main/message_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        message = self.get_object()
        if message.enabled is True:
            context_data['enabled'] = 'Активно'
        else:
            context_data['enabled'] = 'Не активно'

        context_data['title'] = f'Тема письма: {message.subject}'
        context_data['text'] = f'{message.text}'
        context_data['creator'] = f'Автор: {message.creator}'

        return context_data


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message

    success_url = reverse_lazy('main:message_form')

    def post(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу (pk)
        obj = get_object_or_404(Message, pk=kwargs['pk'])

        # Удаляем объект
        obj.delete()

        # Перенаправляем на нужную страницу после удаления
        return redirect('main:message_form')


class MessageConfirmDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'main/message_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(Message, pk=kwargs['pk'])
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    login_url = reverse_lazy('users:login')

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('main:post_form')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user

        start_at_str = self.request.POST.get('start_at')

        if start_at_str:
            start_at = parse_datetime(start_at_str)
            self.object.start_at = make_aware(start_at)
        else:
            form.add_error('start_at', 'Заполните поле даты и времени.')
            return self.form_invalid(form)

        message = self.request.POST.get('message')

        if not message:
            form.add_error('message', 'Заполните поле сообщения.')
            return self.form_invalid(form)

        self.object.save()
        form.save_m2m()

        user = User.objects.get(email='gnmsapr24@yandex.ru')
        print(user.get_all_permissions())  # Права пользователя
        print(user.groups.all())  # Группы пользователя
        for group in user.groups.all():
            print(group.permissions.all())

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Post.objects.filter(creator=self.request.user).order_by('-enabled')
        context_data['title'] = f'Список рассылок в базе'
        context_data['object_type'] = 'post'
        # context_data['recipient_list'] = recipient_list
        return context_data


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'main/post_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        message = self.get_object()
        recipients = message.recipient.all()
        messages = message.message

        if message.enabled is True:
            context_data['enabled'] = 'Активно'
        else:
            context_data['enabled'] = 'Не активно'

        context_data['title'] = f'Название рассылки: {message.name}'
        context_data['text'] = f'{message.description}'
        context_data['creator'] = f'Автор: {message.creator}'
        context_data['recipients'] = recipients
        context_data['object_type'] = 'recipient'
        context_data['message'] = messages
        context_data['post_status'] = message.status
        context_data['period'] = message.period
        context_data['start_at'] = message.start_at
        context_data['next_send_date'] = message.next_send_date

        return context_data


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    success_url = reverse_lazy('main:post_form')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user

        start_at_str = self.request.POST.get('start_at')

        if start_at_str:
            start_at = parse_datetime(start_at_str)
            self.object.start_at = make_aware(start_at)
        else:
            form.add_error('start_at', 'Заполните поле даты и времени.')
            return self.form_invalid(form)

        message = self.request.POST.get('message')

        if not message:
            form.add_error('message', 'Заполните поле сообщения.')
            return self.form_invalid(form)

        self.object.start_at = make_aware(parse_datetime(self.request.POST['start_at']))
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Post.objects.filter(creator=self.request.user).order_by('-enabled')
        context_data['title'] = f'Список рассылок в базе'
        context_data['object_type'] = 'post'
        # context_data['recipient_list'] = recipient_list
        return context_data


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    success_url = reverse_lazy('main:post_form')

    def post(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу (pk)
        obj = get_object_or_404(Post, pk=kwargs['pk'])

        # Удаляем объект
        obj.delete()

        # Перенаправляем на нужную страницу после удаления
        return redirect('main:post_form')


class PostConfirmDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'main/post_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(Post, pk=kwargs['pk'])
        return context


class SendMailing:

    @staticmethod
    def send_mailing():
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = zone.localize(dt.datetime.now()).replace(second=0, microsecond=0)
        mailings = Post.objects.filter(status='created').filter(start_at__lte=current_datetime)
        additional_mailings = Post.objects.filter(status='published').filter(next_send_date__lte=current_datetime)
        combined_mailings = mailings.union(additional_mailings)
        mailings = combined_mailings
        print(mailings)

        if mailings:
            for mailing in mailings:
                mailing.status = 'published'
                mailing.save()
                try:
                    server_response = send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.text,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recipient.email for recipient in mailing.recipient.all()],
                        fail_silently=False
                    )

                    if server_response:
                        PostLogs.objects.create(post=mailing, try_date=current_datetime, result='success')
                        mailing.next_send_date = current_datetime
                        if mailing.period == 'daily':
                            mailing.next_send_date += dt.timedelta(days=1)
                        elif mailing.period == 'weekly':
                            mailing.next_send_date += dt.timedelta(days=7)
                        elif mailing.period == 'monthly':
                            mailing.next_send_date += dt.timedelta(days=30)

                        mailing.save()
                    else:
                        PostLogs.objects.create(post=mailing, try_date=current_datetime, result='failed')
                except smtplib.SMTPException as err:
                    PostLogs.objects.create(post=mailing, try_date=current_datetime, result='failed', error_message=err)


def start_scheduler():
    scheduler = BackgroundScheduler()
    send_mailing_instance = SendMailing()
    scheduler.add_job(send_mailing_instance.send_mailing, 'interval', seconds=60)  # Запускаем задачу каждые 60 секунд
    scheduler.start()


class PostLogsView(LoginRequiredMixin, TemplateView):
    template_name = 'main/post_logs.html'

    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('users.view_post_logs'):
            context['post'] = PostLogs.objects.filter
        elif PostLogs.objects.filter(user=self.request.user).exists():
            context['post'] = PostLogs.objects.filter(user=self.request.user)
        else:
            context['post'] = None
        context['object_type'] = 'post'

        return context


class RecipientListAdminView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'users.view_recipients'

    login_url = reverse_lazy('users:login')
    model = Recipient

    success_url = reverse_lazy('main:recipient_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Recipient.objects.all()
        context_data['object_type'] = 'recipient'
        return context_data


class UserListAdminView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'users.view_users'
    template_name = 'main/user_list.html'

    login_url = reverse_lazy('users:login')
    model = User

    success_url = reverse_lazy('main:index')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = User.objects.all()
        context_data['object_type'] = 'user'
        return context_data


class PostListAdminView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'users.view_posts'
    template_name = 'main/post_list.html'

    login_url = reverse_lazy('users:login')
    model = Post

    success_url = reverse_lazy('main:index')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        from main.services import get_posts_from_cache
        context_data['objects_list'] = get_posts_from_cache()
        context_data['object_type'] = 'post'
        return context_data
