import time
import logging
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

# Set up logger
logger = logging.getLogger('permission_audit')

class PermissionAuditMiddleware:
    """
    Middleware to audit permission usage and enforce security policies.
    
    This middleware:
    1. Logs permission checks for auditing purposes
    2. Enforces the principle of least privilege
    3. Detects potential permission abuse
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize permission usage tracking
        self.permission_usage = {}
        
    def __call__(self, request):
        # Process request
        if request.user.is_authenticated:
            # Store the start time for performance monitoring
            start_time = time.time()
            
            # Store original permissions for comparison
            original_permissions = self._get_user_permissions(request.user) if request.user.is_authenticated else {}
            
            # Process the request
            response = self.get_response(request)
            
            # Check for permission usage after request processing
            if hasattr(request, 'permission_checks') and request.permission_checks:
                self._log_permission_usage(request, request.permission_checks, start_time)
                self._check_for_unusual_activity(request, request.permission_checks)
            
            return response
        else:
            # For unauthenticated users, just process the request
            return self.get_response(request)
    
    def _get_user_permissions(self, user):
        """Get all permissions for a user."""
        return user.get_permissions() if hasattr(user, 'get_permissions') else {}
    
    def _log_permission_usage(self, request, permission_checks, start_time):
        """Log permission usage for auditing."""
        user = request.user
        path = request.path
        method = request.method
        execution_time = time.time() - start_time
        
        # Log each permission check
        for permission, granted in permission_checks.items():
            logger.info(
                f"PERMISSION CHECK: User={user.username} ({user.id}), "
                f"Permission={permission}, Granted={granted}, "
                f"Path={path}, Method={method}, Time={execution_time:.4f}s"
            )
            
            # Update permission usage statistics
            if user.id not in self.permission_usage:
                self.permission_usage[user.id] = {}
            
            if permission not in self.permission_usage[user.id]:
                self.permission_usage[user.id][permission] = {
                    'count': 0,
                    'last_used': None,
                    'granted_count': 0,
                    'denied_count': 0
                }
            
            self.permission_usage[user.id][permission]['count'] += 1
            self.permission_usage[user.id][permission]['last_used'] = timezone.now()
            
            if granted:
                self.permission_usage[user.id][permission]['granted_count'] += 1
            else:
                self.permission_usage[user.id][permission]['denied_count'] += 1
    
    def _check_for_unusual_activity(self, request, permission_checks):
        """Check for unusual permission usage patterns."""
        user = request.user
        
        # Check for multiple denied permissions in a short time
        denied_permissions = [p for p, granted in permission_checks.items() if not granted]
        if len(denied_permissions) >= getattr(settings, 'PERMISSION_DENIED_THRESHOLD', 5):
            logger.warning(
                f"UNUSUAL ACTIVITY: User={user.username} ({user.id}) had {len(denied_permissions)} "
                f"permission denials in a single request: {', '.join(denied_permissions)}"
            )
            
            # Optionally notify the user
            messages.warning(
                request, 
                _("Unusual permission activity detected. This has been logged for security purposes.")
            )

class PermissionTrackingMiddleware:
    """
    Middleware to track permission checks during request processing.
    
    This middleware adds a permission_checks attribute to the request object
    that can be used to track which permissions were checked during processing.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Initialize permission tracking
        request.permission_checks = {}
        
        # Monkey patch the has_permission method to track usage
        if request.user.is_authenticated and hasattr(request.user, 'has_permission'):
            original_has_permission = request.user.has_permission
            
            def tracked_has_permission(permission_name):
                result = original_has_permission(permission_name)
                request.permission_checks[permission_name] = result
                return result
            
            request.user.has_permission = tracked_has_permission
        
        response = self.get_response(request)
        
        # Restore original method if we patched it
        if request.user.is_authenticated and hasattr(request.user, 'has_permission'):
            if hasattr(request.user, '_original_has_permission'):
                request.user.has_permission = request.user._original_has_permission
        
        return response

class LeastPrivilegeMiddleware:
    """
    Middleware to enforce the principle of least privilege.
    
    This middleware periodically reviews user permissions and suggests
    removing unused or unnecessary permissions.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_review = {}
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Periodically check for unused permissions
        if request.user.is_authenticated:
            user_id = request.user.id
            now = timezone.now()
            
            # Check if it's time to review this user's permissions
            if (user_id not in self.last_review or 
                (now - self.last_review[user_id]).days >= getattr(settings, 'PERMISSION_REVIEW_DAYS', 30)):
                
                self._review_user_permissions(request.user)
                self.last_review[user_id] = now
        
        return response
    
    def _review_user_permissions(self, user):
        """Review a user's permissions and log recommendations."""
        # This would typically analyze permission usage data and make recommendations
        # For now, we'll just log that a review was performed
        logger.info(f"PERMISSION REVIEW: Performed review for user={user.username} ({user.id})")
        
        # In a real implementation, this would:
        # 1. Check permission usage statistics
        # 2. Identify permissions that haven't been used in a long time
        # 3. Log recommendations for removing unnecessary permissions
        # 4. Potentially notify administrators