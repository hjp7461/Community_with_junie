from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import UserProfile, UserRole, UserRoleAssignment

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    """
    Signal to create default roles after migration.
    """
    if sender.name == 'users':
        # Create Super Admin role if it doesn't exist
        super_admin, created = UserRole.objects.get_or_create(
            name='Super Admin',
            defaults={
                'description': 'System-wide administrator with all permissions',
                'can_read_content': True,
                'can_create_content': True,
                'can_edit_own_content': True,
                'can_delete_own_content': True,
                'can_edit_any_content': True,
                'can_delete_any_content': True,
                'can_approve_content': True,
                'can_view_users': True,
                'can_warn_users': True,
                'can_suspend_users': True,
                'can_ban_users': True,
                'can_change_user_roles': True,
                'can_manage_user_data': True,
                'can_manage_categories': True,
                'can_manage_system_settings': True,
                'can_access_logs': True,
                'can_manage_api': True,
                'is_super_role': True,
                'trust_level': 5
            }
        )

        # Create Admin role if it doesn't exist
        admin, created = UserRole.objects.get_or_create(
            name='Admin',
            defaults={
                'description': 'Administrator with permissions to manage content and users',
                'can_read_content': True,
                'can_create_content': True,
                'can_edit_own_content': True,
                'can_delete_own_content': True,
                'can_edit_any_content': True,
                'can_delete_any_content': True,
                'can_approve_content': True,
                'can_view_users': True,
                'can_warn_users': True,
                'can_suspend_users': True,
                'can_ban_users': True,
                'can_change_user_roles': False,
                'can_manage_user_data': True,
                'can_manage_categories': True,
                'can_manage_system_settings': False,
                'can_access_logs': True,
                'can_manage_api': False,
                'parent_role': super_admin,
                'trust_level': 4
            }
        )

        # Create Moderator role if it doesn't exist
        moderator, created = UserRole.objects.get_or_create(
            name='Moderator',
            defaults={
                'description': 'Content moderator with permissions to manage content',
                'can_read_content': True,
                'can_create_content': True,
                'can_edit_own_content': True,
                'can_delete_own_content': True,
                'can_edit_any_content': True,
                'can_delete_any_content': True,
                'can_approve_content': True,
                'can_view_users': True,
                'can_warn_users': True,
                'can_suspend_users': False,
                'can_ban_users': False,
                'can_change_user_roles': False,
                'can_manage_user_data': False,
                'can_manage_categories': False,
                'can_manage_system_settings': False,
                'can_access_logs': False,
                'can_manage_api': False,
                'parent_role': admin,
                'trust_level': 3
            }
        )

        # Create Regular User role if it doesn't exist
        regular_user, created = UserRole.objects.get_or_create(
            name='Regular User',
            defaults={
                'description': 'Regular user with basic content creation permissions',
                'can_read_content': True,
                'can_create_content': True,
                'can_edit_own_content': True,
                'can_delete_own_content': True,
                'can_edit_any_content': False,
                'can_delete_any_content': False,
                'can_approve_content': False,
                'can_view_users': False,
                'can_warn_users': False,
                'can_suspend_users': False,
                'can_ban_users': False,
                'can_change_user_roles': False,
                'can_manage_user_data': False,
                'can_manage_categories': False,
                'can_manage_system_settings': False,
                'can_access_logs': False,
                'can_manage_api': False,
                'parent_role': moderator,
                'trust_level': 1
            }
        )

        # Create Guest role if it doesn't exist
        guest, created = UserRole.objects.get_or_create(
            name='Guest',
            defaults={
                'description': 'Guest user with read-only permissions',
                'can_read_content': True,
                'can_create_content': False,
                'can_edit_own_content': False,
                'can_delete_own_content': False,
                'can_edit_any_content': False,
                'can_delete_any_content': False,
                'can_approve_content': False,
                'can_view_users': False,
                'can_warn_users': False,
                'can_suspend_users': False,
                'can_ban_users': False,
                'can_change_user_roles': False,
                'can_manage_user_data': False,
                'can_manage_categories': False,
                'can_manage_system_settings': False,
                'can_access_logs': False,
                'can_manage_api': False,
                'parent_role': None,
                'trust_level': 0
            }
        )

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a new user is created.
    """
    if created:
        UserProfile.objects.create(user=instance)

        # Assign default role if available
        try:
            default_role = UserRole.objects.get(name='Regular User')
            UserRoleAssignment.objects.create(
                user=instance,
                role=default_role
            )
        except UserRole.DoesNotExist:
            # If Regular User role doesn't exist, create it
            default_role = UserRole.objects.create(
                name='Regular User',
                description='Regular user with basic content creation permissions',
                can_read_content=True,
                can_create_content=True,
                can_edit_own_content=True,
                can_delete_own_content=True,
                can_edit_any_content=False,
                can_delete_any_content=False,
                can_approve_content=False,
                can_view_users=False,
                can_warn_users=False,
                can_suspend_users=False,
                can_ban_users=False,
                can_change_user_roles=False,
                can_manage_user_data=False,
                can_manage_categories=False,
                can_manage_system_settings=False,
                can_access_logs=False,
                can_manage_api=False,
                trust_level=1
            )
            UserRoleAssignment.objects.create(
                user=instance,
                role=default_role
            )
