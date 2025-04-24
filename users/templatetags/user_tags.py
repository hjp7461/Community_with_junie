from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def has_permission(user, permission_name):
    """
    Template filter to check if a user has a specific permission.
    
    Usage:
    {% if user|has_permission:"can_edit_any_content" %}
        <a href="{% url 'edit_content' %}">Edit Content</a>
    {% endif %}
    """
    if not user.is_authenticated:
        return False
    return user.has_permission(permission_name)

@register.filter
def has_role(user, role_name):
    """
    Template filter to check if a user has a specific role.
    
    Usage:
    {% if user|has_role:"Admin" %}
        <a href="{% url 'admin_dashboard' %}">Admin Dashboard</a>
    {% endif %}
    """
    if not user.is_authenticated:
        return False
    return user.has_role(role_name)

@register.filter
def has_trust_level(user, level):
    """
    Template filter to check if a user has at least a specific trust level.
    
    Usage:
    {% if user|has_trust_level:3 %}
        <a href="{% url 'trusted_content' %}">Trusted Content</a>
    {% endif %}
    """
    if not user.is_authenticated:
        return False
    try:
        level = int(level)
    except (ValueError, TypeError):
        return False
    return user.get_trust_level() >= level

@register.simple_tag
def if_has_permission(user, permission_name, true_value, false_value=""):
    """
    Template tag to output different values based on user permission.
    
    Usage:
    {% if_has_permission user "can_edit_any_content" "Edit" "View Only" %}
    """
    if not user.is_authenticated:
        return mark_safe(false_value)
    if user.has_permission(permission_name):
        return mark_safe(true_value)
    return mark_safe(false_value)

@register.simple_tag
def if_has_role(user, role_name, true_value, false_value=""):
    """
    Template tag to output different values based on user role.
    
    Usage:
    {% if_has_role user "Admin" "Admin Dashboard" "" %}
    """
    if not user.is_authenticated:
        return mark_safe(false_value)
    if user.has_role(role_name):
        return mark_safe(true_value)
    return mark_safe(false_value)

@register.simple_tag
def if_has_trust_level(user, level, true_value, false_value=""):
    """
    Template tag to output different values based on user trust level.
    
    Usage:
    {% if_has_trust_level user 3 "Trusted Content" "" %}
    """
    if not user.is_authenticated:
        return mark_safe(false_value)
    try:
        level = int(level)
    except (ValueError, TypeError):
        return mark_safe(false_value)
    if user.get_trust_level() >= level:
        return mark_safe(true_value)
    return mark_safe(false_value)

@register.inclusion_tag('users/permission_badge.html')
def permission_badge(user):
    """
    Template tag to display a badge with the user's highest role.
    
    Usage:
    {% permission_badge user %}
    """
    roles = user.get_roles() if user.is_authenticated else []
    highest_role = None
    highest_trust_level = -1
    
    for role in roles:
        if role.trust_level > highest_trust_level:
            highest_trust_level = role.trust_level
            highest_role = role
    
    return {
        'user': user,
        'highest_role': highest_role,
        'is_authenticated': user.is_authenticated,
    }