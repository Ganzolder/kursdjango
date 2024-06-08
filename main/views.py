from django.urls import reverse_lazy
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from main.forms import RecipientForm, MessageForm, PostForm
from main.models import Recipient, Message, Post
from django.utils.timezone import make_aware


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['num_recipients'] = Recipient.objects.filter(creator=user).count()
        context['num_messages'] = Message.objects.filter(creator=user).count()
        context['num_posts'] = Post.objects.filter(creator=user).count()
        return context


class RecipientCreateView(CreateView):

    model = Recipient
    form_class = RecipientForm

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('main:recipient_form')

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Recipient.objects.filter(creator=self.request.user)
        context_data['title'] = f'Список адресатов в базе'
        context_data['object_type'] = 'recipient'
        # context_data['recipient_list'] = recipient_list
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class RecipientDetailView(DetailView):
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

"""
class RecipientListView(ListView):

    model = Recipient

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)

        context_data['title'] = f'Список адресатов'
        # context_data['recipient_list'] = recipient_list
        return context_data
"""

class MessageCreateView(CreateView):

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
        context_data['objects_list'] = Message.objects.filter(creator=self.request.user)
        context_data['title'] = f'Список адресатов в базе'
        context_data['object_type'] = 'message'
        # context_data['recipient_list'] = recipient_list
        return context_data

"""
class MessageListView(ListView):

    model = Message

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)

        print(context_data['objects_list'])
        context_data['title'] = f'Список адресатов'
        # context_data['recipient_list'] = recipient_list
        return context_data

"""
class MessageDetailView(DetailView):
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




class PostCreateView(CreateView):

    model = Post
    form_class = PostForm

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('main:post_form')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.start_at = make_aware(parse_datetime(self.request.POST['start_at']))
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        # recipient_list = Recipient.objects.filter(creator=self.request.user)
        context_data = super().get_context_data(*args, **kwargs)
        context_data['objects_list'] = Post.objects.filter(creator=self.request.user)
        context_data['title'] = f'Список рассылок в базе'
        context_data['object_type'] = 'post'
        # context_data['recipient_list'] = recipient_list
        return context_data


class PostDetailView(DetailView):
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

        return context_data
