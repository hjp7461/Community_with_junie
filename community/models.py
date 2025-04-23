from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.text import slugify
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

class Category(models.Model):
    """
    Category model for organizing boards.

    Categories are the top-level organization structure for the community.
    Each category can contain multiple boards.
    """
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    order = models.IntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order', 'name']

class Board(models.Model):
    """
    Board model for organizing discussions.

    Boards belong to categories and contain posts.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='boards',
        verbose_name=_('category')
    )
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    slug = models.SlugField(_('slug'))
    order = models.IntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    is_private = models.BooleanField(_('is private'), default=False)
    moderators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='moderated_boards',
        verbose_name=_('moderators'),
        blank=True
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('board')
        verbose_name_plural = _('boards')
        ordering = ['category', 'order', 'name']
        unique_together = ('category', 'slug')

class Report(models.Model):
    """
    Report model for reporting inappropriate content.

    Users can report posts, comments, or other users for moderation.
    """
    REPORT_TYPES = (
        ('post', _('Post')),
        ('comment', _('Comment')),
        ('user', _('User')),
    )

    REPORT_STATUSES = (
        ('pending', _('Pending')),
        ('reviewing', _('Reviewing')),
        ('resolved', _('Resolved')),
        ('rejected', _('Rejected')),
    )

    REPORT_REASONS = (
        ('spam', _('Spam')),
        ('harassment', _('Harassment')),
        ('inappropriate', _('Inappropriate Content')),
        ('illegal', _('Illegal Content')),
        ('other', _('Other')),
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_submitted',
        verbose_name=_('reporter')
    )
    report_type = models.CharField(_('report type'), max_length=10, choices=REPORT_TYPES)
    content_type = models.CharField(_('content type'), max_length=100)
    content_id = models.PositiveIntegerField(_('content ID'))
    reason = models.CharField(_('reason'), max_length=20, choices=REPORT_REASONS)
    details = models.TextField(_('details'), blank=True)
    status = models.CharField(
        _('status'),
        max_length=10,
        choices=REPORT_STATUSES,
        default='pending'
    )
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_handled',
        verbose_name=_('moderator')
    )
    moderator_notes = models.TextField(_('moderator notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f"Report #{self.id} - {self.get_report_type_display()}"

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')
        ordering = ['-created_at']

class Notice(models.Model):
    """
    Notice model for community announcements.

    Notices are important announcements visible to all users.
    """
    NOTICE_TYPES = (
        ('announcement', _('Announcement')),
        ('update', _('Update')),
        ('maintenance', _('Maintenance')),
        ('event', _('Event')),
    )

    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    notice_type = models.CharField(_('notice type'), max_length=20, choices=NOTICE_TYPES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notices',
        verbose_name=_('author')
    )
    is_pinned = models.BooleanField(_('is pinned'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    start_date = models.DateTimeField(_('start date'), null=True, blank=True)
    end_date = models.DateTimeField(_('end date'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('notice')
        verbose_name_plural = _('notices')
        ordering = ['-is_pinned', '-created_at']

class FAQ(models.Model):
    """
    FAQ model for frequently asked questions.

    FAQs help users find answers to common questions.
    """
    question = models.CharField(_('question'), max_length=255)
    answer = models.TextField(_('answer'))
    category = models.CharField(_('category'), max_length=100, blank=True)
    order = models.IntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order', 'category', 'question']


class Post(models.Model):
    """
    Post model for user-created content.

    Posts belong to boards and can have comments and media attachments.
    """
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('board')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('author')
    )
    is_pinned = models.BooleanField(_('is pinned'), default=False)
    is_locked = models.BooleanField(_('is locked'), default=False)
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-is_pinned', '-created_at']


class Comment(models.Model):
    """
    Comment model for user responses to posts.

    Comments can be replies to posts or to other comments (for nested comments).
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('post')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('author')
    )
    content = models.TextField(_('content'))
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name=_('parent comment')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created_at']


class Media(models.Model):
    """
    Media model for image uploads.

    Supports jpg and png uploads, converts and stores as webp.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name=_('post')
    )
    image = models.ImageField(_('image'), upload_to='posts/%Y/%m/%d/')
    webp_image = models.ImageField(_('webp image'), upload_to='posts/%Y/%m/%d/webp/', blank=True)
    caption = models.CharField(_('caption'), max_length=255, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def save(self, *args, **kwargs):
        # First save to get the image field populated
        super().save(*args, **kwargs)

        # Convert to webp if this is a new image or the image has changed
        if self.image and not self.webp_image:
            # Open the image using PIL
            img = Image.open(self.image.path)

            # Create a BytesIO object to hold the webp image
            webp_io = BytesIO()

            # Save the image as webp to the BytesIO object
            img.save(webp_io, 'WEBP')

            # Generate a filename for the webp image
            filename = os.path.splitext(os.path.basename(self.image.name))[0] + '.webp'

            # Save the webp image to the webp_image field
            self.webp_image.save(
                filename,
                ContentFile(webp_io.getvalue()),
                save=False
            )

            # Save again to update the webp_image field
            super().save(update_fields=['webp_image'])

    def __str__(self):
        return f"Media for {self.post.title}"

    class Meta:
        verbose_name = _('media')
        verbose_name_plural = _('media')
        ordering = ['created_at']
