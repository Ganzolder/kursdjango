from msilib.schema import ListView

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
import secrets
from users.forms import UserRegisterForm
from users.models import User
from config.settings import EMAIL_HOST_USER

class UserCreateView(CreateView):
    login_url = reverse_lazy('users:login')
    model = User

    form_class = UserRegisterForm

    """permission_required = 'catalog:add_product'"""
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user = form.save()
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = ''
    user.save()
    return redirect(reverse("users:login"))
