from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Category and Board URLs
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('board/<int:pk>/<slug:slug>/', views.BoardDetailView.as_view(), name='board_detail'),

    # Notice URLs
    path('notices/', views.NoticeListView.as_view(), name='notice_list'),
    path('notices/<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),

    # FAQ URLs
    path('faq/', views.FAQListView.as_view(), name='faq_list'),

    # Report URLs
    path('report/', views.ReportCreateView.as_view(), name='report_create'),
    path('report/success/', views.report_success, name='report_success'),

    # Search URL
    path('search/', views.search_view, name='search'),

    # Post URLs
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/create/with-media/', views.PostWithMediaCreateView.as_view(), name='post_with_media_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs
    path('post/<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    # Media URLs
    path('post/<int:post_id>/media/upload/', views.media_upload, name='media_upload'),
    path('media/<int:media_id>/delete/', views.media_delete, name='media_delete'),
]
