from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import Category, Board, Report, Notice, FAQ, Post, Comment, Media
from .forms import ReportForm, PostForm, CommentForm, MediaForm, PostWithMediaForm

class CategoryListView(ListView):
    """
    View for displaying all categories and their boards.
    """
    model = Category
    template_name = 'community/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related(
            'boards'
        )

class BoardDetailView(DetailView):
    """
    View for displaying a specific board and its posts.
    """
    model = Board
    template_name = 'community/board_detail.html'
    context_object_name = 'board'
    paginate_by = 20

    def get_queryset(self):
        return Board.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get posts for this board with pagination
        posts_list = self.object.posts.all().order_by('-is_pinned', '-created_at')
        paginator = Paginator(posts_list, self.paginate_by)
        page = self.request.GET.get('page', 1)
        posts = paginator.get_page(page)

        context['posts'] = posts
        context['post_form'] = PostForm(initial={'board': self.object})
        return context

class NoticeListView(ListView):
    """
    View for displaying all notices.
    """
    model = Notice
    template_name = 'community/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 10

    def get_queryset(self):
        return Notice.objects.filter(is_active=True)

class NoticeDetailView(DetailView):
    """
    View for displaying a specific notice.
    """
    model = Notice
    template_name = 'community/notice_detail.html'
    context_object_name = 'notice'

    def get_queryset(self):
        return Notice.objects.filter(is_active=True)

class FAQListView(ListView):
    """
    View for displaying all FAQs.
    """
    model = FAQ
    template_name = 'community/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('order', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group FAQs by category
        faqs_by_category = {}
        for faq in context['faqs']:
            category = faq.category or 'General'
            if category not in faqs_by_category:
                faqs_by_category[category] = []
            faqs_by_category[category].append(faq)
        context['faqs_by_category'] = faqs_by_category
        return context

@method_decorator(login_required, name='dispatch')
class ReportCreateView(CreateView):
    """
    View for creating a new report.
    """
    model = Report
    form_class = ReportForm
    template_name = 'community/report_form.html'
    success_url = reverse_lazy('community:report_success')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        messages.success(self.request, 'Your report has been submitted and will be reviewed by a moderator.')
        return super().form_valid(form)

def report_success(request):
    """
    View for displaying a success message after submitting a report.
    """
    return render(request, 'community/report_success.html')

def search_view(request):
    """
    View for searching across categories, boards, notices, FAQs, and posts.
    """
    query = request.GET.get('q', '')
    results = {
        'categories': [],
        'boards': [],
        'notices': [],
        'faqs': [],
        'posts': [],
    }

    if query:
        results['categories'] = Category.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )
        results['boards'] = Board.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )
        results['notices'] = Notice.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_active=True
        )
        results['faqs'] = FAQ.objects.filter(
            Q(question__icontains=query) | Q(answer__icontains=query),
            is_active=True
        )
        results['posts'] = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    return render(request, 'community/search_results.html', {
        'query': query,
        'results': results,
    })


# Post Views
@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    """
    View for creating a new post.
    """
    model = Post
    form_class = PostForm
    template_name = 'community/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class PostWithMediaCreateView(CreateView):
    """
    View for creating a new post with media attachments.
    """
    template_name = 'community/post_with_media_form.html'
    form_class = PostWithMediaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Create the post
        post = Post(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            board=form.cleaned_data['board'],
            author=self.request.user
        )
        post.save()

        # Handle uploaded images
        images = self.request.FILES.getlist('images')
        for image in images:
            media = Media(post=post, image=image)
            media.save()

        messages.success(self.request, 'Your post has been created successfully.')
        return redirect('community:post_detail', pk=post.pk)


class PostDetailView(DetailView):
    """
    View for displaying a specific post and its comments.
    """
    model = Post
    template_name = 'community/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Increment view count
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])

        # Get comments with pagination
        comments = self.object.comments.filter(parent=None).order_by('created_at')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['media_form'] = MediaForm()
        return context


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    """
    View for updating an existing post.
    """
    model = Post
    form_class = PostForm
    template_name = 'community/post_form.html'

    def get_queryset(self):
        # Only allow the author to update their own posts
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    """
    View for deleting an existing post.
    """
    model = Post
    template_name = 'community/post_confirm_delete.html'
    success_url = reverse_lazy('community:category_list')

    def get_queryset(self):
        # Only allow the author to delete their own posts
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Comment Views
@login_required
@require_POST
def comment_create(request, post_id):
    """
    View for creating a new comment.
    """
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user

        # Check if this is a reply to another comment
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)
            comment.parent = parent

        comment.save()
        messages.success(request, 'Your comment has been added successfully.')
    else:
        messages.error(request, 'There was an error with your comment.')

    return redirect('community:post_detail', pk=post_id)


@login_required
def comment_update(request, comment_id):
    """
    View for updating an existing comment.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated successfully.')
            return redirect('community:post_detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'community/comment_form.html', {
        'form': form,
        'comment': comment,
    })


@login_required
def comment_delete(request, comment_id):
    """
    View for deleting an existing comment.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_id = comment.post.id

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully.')
        return redirect('community:post_detail', pk=post_id)

    return render(request, 'community/comment_confirm_delete.html', {
        'comment': comment,
    })


# Media Views
@login_required
@require_POST
def media_upload(request, post_id):
    """
    View for uploading media to an existing post.
    """
    post = get_object_or_404(Post, id=post_id)

    # Check if the user is the author of the post
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to add media to this post.")

    form = MediaForm(request.POST, request.FILES)

    if form.is_valid():
        media = form.save(commit=False)
        media.post = post
        media.save()
        messages.success(request, 'Your media has been uploaded successfully.')
    else:
        messages.error(request, 'There was an error with your media upload.')

    return redirect('community:post_detail', pk=post_id)


@login_required
def media_delete(request, media_id):
    """
    View for deleting media from a post.
    """
    media = get_object_or_404(Media, id=media_id)

    # Check if the user is the author of the post
    if media.post.author != request.user:
        return HttpResponseForbidden("You don't have permission to delete media from this post.")

    post_id = media.post.id

    if request.method == 'POST':
        media.delete()
        messages.success(request, 'The media has been deleted successfully.')
        return redirect('community:post_detail', pk=post_id)

    return render(request, 'community/media_confirm_delete.html', {
        'media': media,
    })
