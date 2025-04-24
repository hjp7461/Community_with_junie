from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

def permission_required(permission_name, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission.
    """
    def check_permission(user):
        if not user.is_authenticated:
            return False
        return user.has_permission(permission_name)
    
    return user_passes_test(check_permission, login_url=login_url, raise_exception=raise_exception)

def role_required(role_name, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular role.
    """
    def check_role(user):
        if not user.is_authenticated:
            return False
        return user.has_role(role_name)
    
    return user_passes_test(check_role, login_url=login_url, raise_exception=raise_exception)

def trust_level_required(level, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has at least the specified trust level.
    """
    def check_trust_level(user):
        if not user.is_authenticated:
            return False
        return user.get_trust_level() >= level
    
    return user_passes_test(check_trust_level, login_url=login_url, raise_exception=raise_exception)

class PermissionRequiredMixin(UserPassesTestMixin):
    """
    Mixin for views that checks whether a user has a particular permission.
    """
    permission_required = None
    login_url = None
    permission_denied_message = _("You don't have permission to access this page.")
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        if isinstance(self.permission_required, str):
            perms = [self.permission_required]
        else:
            perms = self.permission_required
            
        for perm in perms:
            if not self.request.user.has_permission(perm):
                return False
        return True
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            raise PermissionDenied(self.permission_denied_message)
        return redirect(self.login_url or 'users:login')

class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin for views that checks whether a user has a particular role.
    """
    role_required = None
    login_url = None
    permission_denied_message = _("You don't have the required role to access this page.")
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        if isinstance(self.role_required, str):
            roles = [self.role_required]
        else:
            roles = self.role_required
            
        for role in roles:
            if self.request.user.has_role(role):
                return True
        return False
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            raise PermissionDenied(self.permission_denied_message)
        return redirect(self.login_url or 'users:login')

class TrustLevelRequiredMixin(UserPassesTestMixin):
    """
    Mixin for views that checks whether a user has at least the specified trust level.
    """
    trust_level_required = 0
    login_url = None
    permission_denied_message = _("Your trust level is not high enough to access this page.")
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.get_trust_level() >= self.trust_level_required
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            raise PermissionDenied(self.permission_denied_message)
        return redirect(self.login_url or 'users:login')