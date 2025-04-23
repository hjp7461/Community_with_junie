from django import forms
from django.core.validators import FileExtensionValidator
from .models import Report, Post, Comment, Media

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ReportForm(forms.ModelForm):
    """
    Form for creating a new report.
    """
    class Meta:
        model = Report
        fields = ['report_type', 'content_type', 'content_id', 'reason', 'details']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['details'].help_text = 'Please provide additional details about the issue.'
        self.fields['content_type'].help_text = 'The type of content being reported (e.g., post, comment).'
        self.fields['content_id'].help_text = 'The ID of the content being reported.'


class PostForm(forms.ModelForm):
    """
    Form for creating and updating posts.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'board']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'post-content'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['board'].widget.attrs.update({'class': 'form-control'})


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'comment-content'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})


class MediaForm(forms.ModelForm):
    """
    Form for uploading media files.
    """
    image = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text='Supported formats: jpg, png'
    )

    class Meta:
        model = Media
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['caption'].widget.attrs.update({'class': 'form-control'})


class PostWithMediaForm(forms.Form):
    """
    Combined form for creating a post with media attachments.
    """
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'class': 'post-content form-control'}))
    board = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))
    images = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=MultipleFileInput(attrs={'class': 'form-control-file'}),
        help_text='Supported formats: jpg, png. You can upload multiple images.'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        from .models import Board
        # Filter boards based on user permissions if needed
        self.fields['board'].queryset = Board.objects.filter(is_active=True)
