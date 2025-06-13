from django.urls import path
from .views import (
    PostListCreateView, PostDetailView, CommentListCreateView,
    AdminPostListView, AdminCommentListView, AdminCommentApproveView,
    AdminCommentBlockView, LikePostView, UnlikePostView
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('admin/posts/', AdminPostListView.as_view(), name='admin_post_list'),
    path('admin/comments/', AdminCommentListView.as_view(), name='admin_comment_list'),
    path('admin/comments/<int:pk>/approve/', AdminCommentApproveView.as_view(), name='admin_comment_approve'),
    path('admin/comments/<int:pk>/block/', AdminCommentBlockView.as_view(), name='admin_comment_block'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post_like'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='post_unlike'),
]