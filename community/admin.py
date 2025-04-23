from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Board, Report, Notice, FAQ, Post, Comment, Media

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'is_active', 'is_private', 'created_at')
    list_filter = ('category', 'is_active', 'is_private')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('moderators',)
    ordering = ('category', 'order', 'name')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_type', 'reason', 'status', 'reporter', 'moderator', 'created_at')
    list_filter = ('report_type', 'reason', 'status')
    search_fields = ('details', 'moderator_notes')
    readonly_fields = ('reporter', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('reporter', 'report_type', 'content_type', 'content_id', 'reason', 'details')
        }),
        ('Moderation', {
            'fields': ('status', 'moderator', 'moderator_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'author', 'is_pinned', 'is_active', 'created_at')
    list_filter = ('notice_type', 'is_pinned', 'is_active')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'notice_type', 'author')
        }),
        ('Display Options', {
            'fields': ('is_pinned', 'is_active', 'start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer', 'category')
    ordering = ('order', 'category', 'question')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'author', 'is_pinned', 'is_locked', 'view_count', 'created_at')
    list_filter = ('board', 'is_pinned', 'is_locked')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'board', 'author')
        }),
        ('Display Options', {
            'fields': ('is_pinned', 'is_locked')
        }),
        ('Statistics', {
            'fields': ('view_count',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'parent', 'created_at')
    list_filter = ('post__board',)
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'content', 'parent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'caption', 'created_at')
    list_filter = ('post__board',)
    search_fields = ('caption', 'post__title')
    readonly_fields = ('created_at', 'image_preview', 'webp_preview')
    fieldsets = (
        (None, {
            'fields': ('post', 'image', 'image_preview', 'webp_image', 'webp_preview', 'caption')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" />')
        return 'No image'

    def webp_preview(self, obj):
        if obj.webp_image:
            return mark_safe(f'<img src="{obj.webp_image.url}" style="max-height: 200px; max-width: 200px;" />')
        return 'No webp image'

    image_preview.short_description = 'Image Preview'
    webp_preview.short_description = 'WebP Preview'
