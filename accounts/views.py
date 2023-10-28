from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import resolve_url, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView

from accounts.forms import CustomRegisterForm
from accounts.models import Profile
from accounts.token import account_activation_token


class RegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("bulletin_board:announcement_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)

        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('accounts/acc_active_email.html', {
            'user': user,
            'domain': self.request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return response


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("bulletin_board:announcement_list")

    def get_default_redirect_url(self):
        return resolve_url('bulletin_board:announcement_list')


class CustomLogoutView(LogoutView):
    template_name = '/accounts/login.html'

    def get_default_redirect_url(self):
        return resolve_url('accounts:login')


def confirm_email(request, auth_token):
    profile_obj = Profile.objects.filter(pk=urlsafe_base64_decode(auth_token)).first()
    if profile_obj:
        profile_obj.confirmed = True
        profile_obj.save()
        messages.success(request, 'You account is been verified')
        return redirect('bulletin_board:announcement_list')
    return HttpResponse('Activation link is invalid!')
