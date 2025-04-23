from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile, UserRole, UserRoleAssignment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserRoleAssignmentInline(admin.TabularInline):
    model = UserRoleAssignment
    extra = 1
    verbose_name_plural = 'roles'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, UserRoleAssignmentInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'can_edit_posts', 'can_delete_posts', 'can_ban_users', 'can_approve_content', 'can_manage_roles')
    search_fields = ('name', 'description')
    list_filter = ('can_edit_posts', 'can_delete_posts', 'can_ban_users', 'can_approve_content', 'can_manage_roles')

class UserRoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_by', 'assigned_at')
    list_filter = ('role', 'assigned_at')
    search_fields = ('user__username', 'role__name', 'assigned_by__username')
    raw_id_fields = ('user', 'role', 'assigned_by')

# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserRoleAssignment, UserRoleAssignmentAdmin)
