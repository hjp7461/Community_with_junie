from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile

class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
        help_text=_('Required. Enter a valid email address.')
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm Password')})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is already in use.'))
        return email

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile.
    """
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture', 'birth_date', 'location', 'website', 'facebook', 'twitter', 'instagram')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with styled widgets.
    """
    username = forms.CharField(
        label=_('Email'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}),
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form with styled widgets.
    """
    old_password = forms.CharField(
        label=_('Old password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Old password')}),
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('New password')}),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('New password confirmation')}),
    )

class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom password reset form with styled widgets.
    """
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
    )

class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom set password form with styled widgets.
    """
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('New password')}),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('New password confirmation')}),
    )