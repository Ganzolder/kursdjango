from django import forms
from django.db import models

from main.models import Recipient, Message, Post


class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control form-floating'


class RecipientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Recipient
        fields = ('name', 'email', 'description', 'enabled')


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ('subject', 'text', 'enabled')


class PostForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Post
        fields = ('recipient', 'message', 'name', 'start_at', 'next_send_date', 'description', 'status', 'period', 'enabled')
        widgets = {
            'recipient': forms.SelectMultiple(),
            'start_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Фильтруем список получателей и сообщений по текущему пользователю или с user=None
        self.fields['recipient'].queryset = Recipient.objects.filter(creator=user)
        self.fields['message'].queryset = Message.objects.filter(creator=user)
