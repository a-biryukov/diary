from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from users import forms
from users.forms import UserPasswordChangeForm
from users.models import User
from users.services import user_verify, pass_recovery


class UserCreateView(generic.CreateView):
    model = User
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        host = self.request.get_host()
        user_verify(user, host)
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.email:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = forms.UserUpdateForm
    template_name = 'users/user_update_form.html'

    def get_success_url(self):
        return reverse('users:user_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.email:
            return self.object
        raise PermissionDenied


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.email or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class PasswordRecoveryTemplateView(generic.TemplateView):
    template_name = 'users/password_recovery.html'
    form_class = forms.PasswordRecoveryForm
    success_url = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            pass_recovery(email)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['form'] = self.form_class
        return context_data


class UserLoginView(LoginView):
    form_class = forms.UserAuthenticationForm


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.email == self.object.email:
            return self.object
        raise PermissionDenied


def email_verification(request, token):
    """Подтверждение почты нового пользователя"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
