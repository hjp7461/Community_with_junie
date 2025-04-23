from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    This model maintains all the functionality of Django's default User model
    while allowing for easy customization.
    """
    email = models.EmailField(_('email address'), unique=True)

    # Add additional fields as needed
    is_verified = models.BooleanField(default=False)

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class UserProfile(models.Model):
    """
    User profile model containing additional user information.

    This model is linked to the User model via a one-to-one relationship.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    profile_picture = models.FileField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    # Social media links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

class UserRole(models.Model):
    """
    User role model for managing permissions and roles.

    This model allows for defining different roles like admin, moderator, etc.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    # Permissions
    can_edit_posts = models.BooleanField(default=False)
    can_delete_posts = models.BooleanField(default=False)
    can_ban_users = models.BooleanField(default=False)
    can_approve_content = models.BooleanField(default=False)
    can_manage_roles = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('user role')
        verbose_name_plural = _('user roles')

class UserRoleAssignment(models.Model):
    """
    Model for assigning roles to users.

    This model creates a many-to-many relationship between users and roles.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='role_assignments'
    )
    role = models.ForeignKey(
        UserRole,
        on_delete=models.CASCADE,
        related_name='user_assignments'
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='role_assignments_given'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    class Meta:
        verbose_name = _('user role assignment')
        verbose_name_plural = _('user role assignments')
        unique_together = ('user', 'role')
