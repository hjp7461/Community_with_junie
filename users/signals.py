from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import UserProfile, UserRole, UserRoleAssignment

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a user profile when a new user is created.
    """
    if created:
        UserProfile.objects.create(user=instance)
        
        # Assign default role if available
        try:
            default_role = UserRole.objects.get(name='Member')
            UserRoleAssignment.objects.create(
                user=instance,
                role=default_role
            )
        except UserRole.DoesNotExist:
            # Create default role if it doesn't exist
            default_role = UserRole.objects.create(
                name='Member',
                description='Regular member with basic permissions',
                can_edit_posts=True,
                can_delete_posts=False,
                can_ban_users=False,
                can_approve_content=False,
                can_manage_roles=False
            )
            UserRoleAssignment.objects.create(
                user=instance,
                role=default_role
            )