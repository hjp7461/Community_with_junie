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

    def get_roles(self):
        """
        Get all roles assigned to the user.
        """
        return [assignment.role for assignment in self.role_assignments.all()]

    def has_role(self, role_name):
        """
        Check if the user has a specific role.
        """
        return self.role_assignments.filter(role__name=role_name).exists()

    def get_permissions(self):
        """
        Get all permissions from all roles assigned to the user.
        Takes into account role hierarchy.
        """
        permissions = {}
        roles = self.get_roles()

        # Process roles to get all permissions
        for role in roles:
            # Get all permission fields
            for field in role._meta.fields:
                if field.name.startswith('can_') and isinstance(field, models.BooleanField):
                    # If permission is not set or is False, check the value from this role
                    if field.name not in permissions or not permissions[field.name]:
                        permissions[field.name] = getattr(role, field.name)

            # Check parent roles recursively
            current_parent = role.parent_role
            while current_parent:
                for field in current_parent._meta.fields:
                    if field.name.startswith('can_') and isinstance(field, models.BooleanField):
                        # Only override if not already set to True
                        if field.name not in permissions or not permissions[field.name]:
                            permissions[field.name] = getattr(current_parent, field.name)
                current_parent = current_parent.parent_role

        return permissions

    def has_permission(self, permission_name):
        """
        Check if the user has a specific permission.
        Takes into account role hierarchy.
        """
        # Superusers have all permissions
        if self.is_superuser:
            return True

        # Get all permissions
        permissions = self.get_permissions()

        # Check if the permission exists and is True
        return permissions.get(permission_name, False)

    def get_trust_level(self):
        """
        Get the highest trust level from all roles assigned to the user.
        """
        roles = self.get_roles()
        if not roles:
            return 0
        return max(role.trust_level for role in roles)

    def has_temporary_role(self):
        """
        Check if the user has any temporary roles.
        """
        from django.utils import timezone
        return self.role_assignments.filter(
            role__is_temporary=True, 
            role__valid_until__gt=timezone.now()
        ).exists()

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

    This model allows for defining different roles like super admin, admin, moderator, etc.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    # Content Permissions
    can_read_content = models.BooleanField(default=True)
    can_create_content = models.BooleanField(default=False)
    can_edit_own_content = models.BooleanField(default=False)
    can_delete_own_content = models.BooleanField(default=False)
    can_edit_any_content = models.BooleanField(default=False)
    can_delete_any_content = models.BooleanField(default=False)
    can_approve_content = models.BooleanField(default=False)

    # User Management Permissions
    can_view_users = models.BooleanField(default=False)
    can_warn_users = models.BooleanField(default=False)
    can_suspend_users = models.BooleanField(default=False)
    can_ban_users = models.BooleanField(default=False)
    can_change_user_roles = models.BooleanField(default=False)
    can_manage_user_data = models.BooleanField(default=False)

    # System Management Permissions
    can_manage_categories = models.BooleanField(default=False)
    can_manage_system_settings = models.BooleanField(default=False)
    can_access_logs = models.BooleanField(default=False)
    can_manage_api = models.BooleanField(default=False)

    # Role hierarchy
    is_super_role = models.BooleanField(default=False)
    parent_role = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_roles')

    # Trust-based permissions
    trust_level = models.PositiveIntegerField(default=0)

    # Temporary role settings
    is_temporary = models.BooleanField(default=False)
    valid_until = models.DateTimeField(null=True, blank=True)

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
