
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={
                    'uidb64': uid,
                    'token': token
                })
            )

            send_mail(
                'Activate your account',
                f'Click this link to activate your account: {activation_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            messages.success(request, 'Check your email to activate your account.')
            return redirect('login')

        return render(request, 'accounts/register.html', {'form': form})
    

class ActivateView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, 'Your account has been activated.')
            return redirect('login')

        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('register')
    
    
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are logged in successfully.')
            return redirect('profile')

        return render(request, 'accounts/login.html', {'form': form})
    
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are logged out successfully.')
        return redirect('login')
    
    
class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'accounts/profile.html', {'user': request.user})


class ProfileEditView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'accounts/profile_edit.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

        return render(request, 'accounts/profile_edit.html', {'form': form})