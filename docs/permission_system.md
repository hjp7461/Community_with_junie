# Role-Based Permission System

This document describes the role-based permission system implemented in the Community project.

## Overview

The permission system is based on the following principles:

1. **Role-Based Access Control (RBAC)**: Users are assigned roles, and roles have permissions.
2. **Hierarchical Roles**: Roles can inherit permissions from parent roles.
3. **Principle of Least Privilege**: Users should have the minimum permissions necessary.
4. **Dynamic Permissions**: Permissions can be adjusted based on trust level and temporary roles.
5. **Auditing and Logging**: Permission usage is tracked and logged for security purposes.

## Role Hierarchy

The system defines the following default roles, in order of increasing privileges:

1. **Guest**: Read-only access to public content.
2. **Regular User**: Can create and manage their own content.
3. **Moderator**: Can moderate content and warn users.
4. **Admin**: Can manage content, users, and categories.
5. **Super Admin**: Has all permissions and can manage the system.

## Permission Categories

Permissions are divided into three main categories:

### Content Permissions

- `can_read_content`: Can view content
- `can_create_content`: Can create new content
- `can_edit_own_content`: Can edit own content
- `can_delete_own_content`: Can delete own content
- `can_edit_any_content`: Can edit any content (moderation)
- `can_delete_any_content`: Can delete any content (moderation)
- `can_approve_content`: Can approve content before publication

### User Management Permissions

- `can_view_users`: Can view user profiles and information
- `can_warn_users`: Can issue warnings to users
- `can_suspend_users`: Can temporarily suspend users
- `can_ban_users`: Can permanently ban users
- `can_change_user_roles`: Can change user roles
- `can_manage_user_data`: Can access and modify user data

### System Management Permissions

- `can_manage_categories`: Can create, edit, and delete categories
- `can_manage_system_settings`: Can change system settings
- `can_access_logs`: Can view system and audit logs
- `can_manage_api`: Can manage API access and settings

## Dynamic Permission Features

### Trust-Based Permissions

Users can gain additional permissions based on their trust level, which is determined by:

- Account age
- Activity level
- Content quality
- Community standing

Trust levels range from 0 (new users) to 5 (highly trusted users).

### Temporary Roles

Administrators can assign temporary roles to users for specific purposes, such as:

- Event moderators
- Project leaders
- Contest judges

Temporary roles have an expiration date and are automatically removed when they expire.

## Using the Permission System

### In Views

Function-based views can use decorators:

```python
from users.permissions import permission_required, role_required, trust_level_required

@permission_required('can_edit_any_content')
def edit_content(request, content_id):
    # View code here
    pass

@role_required('Moderator')
def moderate_content(request):
    # View code here
    pass

@trust_level_required(3)
def trusted_content(request):
    # View code here
    pass
```

Class-based views can use mixins:

```python
from users.permissions import PermissionRequiredMixin, RoleRequiredMixin, TrustLevelRequiredMixin

class EditContentView(PermissionRequiredMixin, UpdateView):
    permission_required = 'can_edit_any_content'
    # View code here

class ModerateContentView(RoleRequiredMixin, ListView):
    role_required = 'Moderator'
    # View code here

class TrustedContentView(TrustLevelRequiredMixin, ListView):
    trust_level_required = 3
    # View code here
```

### In Templates

Template filters and tags are available for permission checks:

```html
{% load user_tags %}

{% if user|has_permission:"can_edit_any_content" %}
    <a href="{% url 'edit_content' content.id %}">Edit</a>
{% endif %}

{% if user|has_role:"Moderator" %}
    <a href="{% url 'moderate_content' %}">Moderate</a>
{% endif %}

{% if user|has_trust_level:3 %}
    <a href="{% url 'trusted_content' %}">Trusted Content</a>
{% endif %}

{% permission_badge user %}
```

### Management Commands

The system includes management commands for role management:

```bash
# List all roles
python manage.py manage_roles list_roles

# List users with a specific role
python manage.py manage_roles list_users "Moderator"

# Assign a role to a user
python manage.py manage_roles assign "username" "Moderator"

# Assign a temporary role
python manage.py manage_roles assign "username" "Event Moderator" --temporary --days 7

# Remove a role
python manage.py manage_roles remove "username" "Moderator"

# Create a new role
python manage.py manage_roles create_role "Editor" "Can edit content" --parent "Moderator" --permissions can_edit_any_content

# Update a role
python manage.py manage_roles update_role "Editor" --add-permissions can_approve_content

# Delete a role
python manage.py manage_roles delete_role "Editor"

# Audit role assignments
python manage.py manage_roles audit --days 30
```

## Security Considerations

The permission system implements several security features:

1. **Principle of Least Privilege**: Users have only the permissions they need.
2. **Permission Auditing**: All permission checks are logged for auditing.
3. **Unusual Activity Detection**: The system detects and logs unusual permission usage.
4. **Regular Permission Reviews**: The system periodically reviews permissions to identify unused or unnecessary permissions.

## Implementation Details

The permission system is implemented in the following files:

- `users/models.py`: Defines the User, UserRole, and UserRoleAssignment models
- `users/signals.py`: Creates default roles and assigns roles to new users
- `users/permissions.py`: Provides decorators and mixins for permission checks
- `users/templatetags/user_tags.py`: Provides template filters and tags for permission checks
- `users/middleware.py`: Implements permission tracking, auditing, and security features
- `users/management/commands/manage_roles.py`: Provides management commands for role management