from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, 
    PasswordResetView, PasswordResetConfirmView
)

from .models import User, UserProfile, UserRole, UserRoleAssignment
from .forms import (
    UserRegistrationForm, UserProfileForm, UserUpdateForm,
    CustomAuthenticationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)

class CustomLoginView(LoginView):
    """
    Custom login view that uses our custom authentication form.
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, _('You have successfully logged in.'))
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    """
    Custom logout view.
    """
    next_page = reverse_lazy('home')
    http_method_names = ["get", "post", "options"]

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _('You have been logged out.'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Logout may be done via GET."""
        logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

class UserRegistrationView(CreateView):
    """
    View for user registration.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a profile for the user
        UserProfile.objects.create(user=self.object)
        # Assign default role if available
        try:
            default_role = UserRole.objects.get(name='Member')
            UserRoleAssignment.objects.create(
                user=self.object,
                role=default_role
            )
        except UserRole.DoesNotExist:
            pass

        messages.success(self.request, _('Your account has been created. You can now log in.'))
        return response

class UserProfileView(LoginRequiredMixin, DetailView):
    """
    View for displaying user profile.
    """
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating user profile.
    """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your profile has been updated.'))
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating user information.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Your account information has been updated.'))
        return super().form_valid(form)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    View for changing password.
    """
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, _('Your password has been changed.'))
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    """
    View for resetting password.
    """
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    View for confirming password reset.
    """
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

# Function-based views for simpler operations

@login_required
def user_list(request):
    """
    View for listing users (admin only).
    """
    if not request.user.is_staff:
        messages.error(request, _('You do not have permission to view this page.'))
        return redirect('home')

    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_detail(request, username):
    """
    View for displaying user details.
    """
    user = get_object_or_404(User, username=username)
    return render(request, 'users/user_detail.html', {'user': user})
