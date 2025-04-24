from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from users.models import UserRole, UserRoleAssignment

User = get_user_model()

class Command(BaseCommand):
    help = 'Manage user roles and permissions'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='Command to run')
        
        # List roles
        list_parser = subparsers.add_parser('list_roles', help='List all roles')
        
        # List users with role
        list_users_parser = subparsers.add_parser('list_users', help='List users with a specific role')
        list_users_parser.add_argument('role', type=str, help='Role name')
        
        # Assign role
        assign_parser = subparsers.add_parser('assign', help='Assign a role to a user')
        assign_parser.add_argument('username', type=str, help='Username')
        assign_parser.add_argument('role', type=str, help='Role name')
        assign_parser.add_argument('--temporary', action='store_true', help='Make the role temporary')
        assign_parser.add_argument('--days', type=int, default=30, help='Number of days for temporary role')
        
        # Remove role
        remove_parser = subparsers.add_parser('remove', help='Remove a role from a user')
        remove_parser.add_argument('username', type=str, help='Username')
        remove_parser.add_argument('role', type=str, help='Role name')
        
        # Create role
        create_parser = subparsers.add_parser('create_role', help='Create a new role')
        create_parser.add_argument('name', type=str, help='Role name')
        create_parser.add_argument('description', type=str, help='Role description')
        create_parser.add_argument('--parent', type=str, help='Parent role name')
        create_parser.add_argument('--permissions', type=str, nargs='+', help='Permissions to grant')
        
        # Update role
        update_parser = subparsers.add_parser('update_role', help='Update an existing role')
        update_parser.add_argument('name', type=str, help='Role name')
        update_parser.add_argument('--description', type=str, help='Role description')
        update_parser.add_argument('--parent', type=str, help='Parent role name')
        update_parser.add_argument('--add-permissions', type=str, nargs='+', help='Permissions to add')
        update_parser.add_argument('--remove-permissions', type=str, nargs='+', help='Permissions to remove')
        
        # Delete role
        delete_parser = subparsers.add_parser('delete_role', help='Delete a role')
        delete_parser.add_argument('name', type=str, help='Role name')
        
        # Audit roles
        audit_parser = subparsers.add_parser('audit', help='Audit role assignments')
        audit_parser.add_argument('--days', type=int, default=30, help='Number of days to look back')

    def handle(self, *args, **options):
        command = options['command']
        
        if command == 'list_roles':
            self.list_roles()
        elif command == 'list_users':
            self.list_users(options['role'])
        elif command == 'assign':
            self.assign_role(options['username'], options['role'], options['temporary'], options['days'])
        elif command == 'remove':
            self.remove_role(options['username'], options['role'])
        elif command == 'create_role':
            self.create_role(options['name'], options['description'], options['parent'], options['permissions'])
        elif command == 'update_role':
            self.update_role(options['name'], options['description'], options['parent'], 
                            options['add_permissions'], options['remove_permissions'])
        elif command == 'delete_role':
            self.delete_role(options['name'])
        elif command == 'audit':
            self.audit_roles(options['days'])
        else:
            raise CommandError('Unknown command: {}'.format(command))

    def list_roles(self):
        """List all roles with their permissions."""
        roles = UserRole.objects.all().order_by('-trust_level')
        
        self.stdout.write(self.style.SUCCESS('Available roles:'))
        for role in roles:
            self.stdout.write(self.style.SUCCESS(f'- {role.name} (Trust Level: {role.trust_level})'))
            self.stdout.write(f'  Description: {role.description}')
            
            # Get parent role if any
            if role.parent_role:
                self.stdout.write(f'  Parent Role: {role.parent_role.name}')
            
            # List permissions
            permissions = []
            for field in role._meta.fields:
                if field.name.startswith('can_') and isinstance(field, type(role._meta.get_field('can_read_content'))):
                    if getattr(role, field.name):
                        permissions.append(field.name)
            
            if permissions:
                self.stdout.write('  Permissions:')
                for perm in permissions:
                    self.stdout.write(f'    - {perm}')
            else:
                self.stdout.write('  No permissions')
            
            self.stdout.write('')

    def list_users(self, role_name):
        """List all users with a specific role."""
        try:
            role = UserRole.objects.get(name=role_name)
        except UserRole.DoesNotExist:
            raise CommandError(f'Role "{role_name}" does not exist')
        
        assignments = UserRoleAssignment.objects.filter(role=role).select_related('user')
        
        self.stdout.write(self.style.SUCCESS(f'Users with role "{role_name}":'))
        if assignments:
            for assignment in assignments:
                self.stdout.write(f'- {assignment.user.username} ({assignment.user.email})')
                if assignment.assigned_by:
                    self.stdout.write(f'  Assigned by: {assignment.assigned_by.username}')
                self.stdout.write(f'  Assigned at: {assignment.assigned_at}')
                
                # Check if temporary
                if role.is_temporary and role.valid_until:
                    if role.valid_until > timezone.now():
                        self.stdout.write(f'  Valid until: {role.valid_until}')
                    else:
                        self.stdout.write(self.style.WARNING(f'  Expired at: {role.valid_until}'))
                
                self.stdout.write('')
        else:
            self.stdout.write('No users found with this role')

    def assign_role(self, username, role_name, temporary=False, days=30):
        """Assign a role to a user."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')
        
        try:
            role = UserRole.objects.get(name=role_name)
        except UserRole.DoesNotExist:
            raise CommandError(f'Role "{role_name}" does not exist')
        
        # Check if the user already has this role
        if UserRoleAssignment.objects.filter(user=user, role=role).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already has role "{role_name}"'))
            return
        
        # Set temporary role if requested
        if temporary:
            role.is_temporary = True
            role.valid_until = timezone.now() + timedelta(days=days)
            role.save()
        
        # Create the assignment
        UserRoleAssignment.objects.create(user=user, role=role)
        
        self.stdout.write(self.style.SUCCESS(f'Assigned role "{role_name}" to user "{username}"'))
        if temporary:
            self.stdout.write(f'Role is temporary and will expire on {role.valid_until}')

    def remove_role(self, username, role_name):
        """Remove a role from a user."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')
        
        try:
            role = UserRole.objects.get(name=role_name)
        except UserRole.DoesNotExist:
            raise CommandError(f'Role "{role_name}" does not exist')
        
        # Check if the user has this role
        try:
            assignment = UserRoleAssignment.objects.get(user=user, role=role)
            assignment.delete()
            self.stdout.write(self.style.SUCCESS(f'Removed role "{role_name}" from user "{username}"'))
        except UserRoleAssignment.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'User "{username}" does not have role "{role_name}"'))

    def create_role(self, name, description, parent=None, permissions=None):
        """Create a new role."""
        # Check if the role already exists
        if UserRole.objects.filter(name=name).exists():
            raise CommandError(f'Role "{name}" already exists')
        
        # Get parent role if specified
        parent_role = None
        if parent:
            try:
                parent_role = UserRole.objects.get(name=parent)
            except UserRole.DoesNotExist:
                raise CommandError(f'Parent role "{parent}" does not exist')
        
        # Create the role
        role = UserRole.objects.create(
            name=name,
            description=description,
            parent_role=parent_role
        )
        
        # Set permissions if specified
        if permissions:
            for perm in permissions:
                if hasattr(role, perm):
                    setattr(role, perm, True)
                else:
                    self.stdout.write(self.style.WARNING(f'Unknown permission: {perm}'))
            role.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created role "{name}"'))

    def update_role(self, name, description=None, parent=None, add_permissions=None, remove_permissions=None):
        """Update an existing role."""
        try:
            role = UserRole.objects.get(name=name)
        except UserRole.DoesNotExist:
            raise CommandError(f'Role "{name}" does not exist')
        
        # Update description if specified
        if description:
            role.description = description
        
        # Update parent role if specified
        if parent:
            try:
                parent_role = UserRole.objects.get(name=parent)
                role.parent_role = parent_role
            except UserRole.DoesNotExist:
                raise CommandError(f'Parent role "{parent}" does not exist')
        
        # Add permissions if specified
        if add_permissions:
            for perm in add_permissions:
                if hasattr(role, perm):
                    setattr(role, perm, True)
                else:
                    self.stdout.write(self.style.WARNING(f'Unknown permission: {perm}'))
        
        # Remove permissions if specified
        if remove_permissions:
            for perm in remove_permissions:
                if hasattr(role, perm):
                    setattr(role, perm, False)
                else:
                    self.stdout.write(self.style.WARNING(f'Unknown permission: {perm}'))
        
        role.save()
        self.stdout.write(self.style.SUCCESS(f'Updated role "{name}"'))

    def delete_role(self, name):
        """Delete a role."""
        try:
            role = UserRole.objects.get(name=name)
        except UserRole.DoesNotExist:
            raise CommandError(f'Role "{name}" does not exist')
        
        # Check if the role is assigned to any users
        if UserRoleAssignment.objects.filter(role=role).exists():
            self.stdout.write(self.style.WARNING(f'Role "{name}" is assigned to users. Deleting it will remove it from all users.'))
            confirm = input('Are you sure you want to continue? (y/n): ')
            if confirm.lower() != 'y':
                self.stdout.write('Operation cancelled')
                return
        
        # Check if the role is a parent of other roles
        if UserRole.objects.filter(parent_role=role).exists():
            self.stdout.write(self.style.WARNING(f'Role "{name}" is a parent of other roles. Deleting it will remove the parent relationship.'))
            confirm = input('Are you sure you want to continue? (y/n): ')
            if confirm.lower() != 'y':
                self.stdout.write('Operation cancelled')
                return
        
        # Delete the role
        role.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted role "{name}"'))

    def audit_roles(self, days=30):
        """Audit role assignments."""
        # Get recent assignments
        recent_date = timezone.now() - timedelta(days=days)
        recent_assignments = UserRoleAssignment.objects.filter(assigned_at__gte=recent_date).select_related('user', 'role', 'assigned_by')
        
        self.stdout.write(self.style.SUCCESS(f'Role assignments in the last {days} days:'))
        if recent_assignments:
            for assignment in recent_assignments:
                self.stdout.write(f'- User: {assignment.user.username}')
                self.stdout.write(f'  Role: {assignment.role.name}')
                if assignment.assigned_by:
                    self.stdout.write(f'  Assigned by: {assignment.assigned_by.username}')
                self.stdout.write(f'  Assigned at: {assignment.assigned_at}')
                self.stdout.write('')
        else:
            self.stdout.write('No recent role assignments found')
        
        # Check for expired temporary roles
        expired_roles = UserRole.objects.filter(is_temporary=True, valid_until__lt=timezone.now())
        if expired_roles:
            self.stdout.write(self.style.WARNING('Expired temporary roles:'))
            for role in expired_roles:
                assignments = UserRoleAssignment.objects.filter(role=role).select_related('user')
                for assignment in assignments:
                    self.stdout.write(f'- User: {assignment.user.username}')
                    self.stdout.write(f'  Role: {role.name}')
                    self.stdout.write(f'  Expired at: {role.valid_until}')
                    self.stdout.write('')
        else:
            self.stdout.write('No expired temporary roles found')