from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from auth_app.models import CustomUser
import logging

logger = logging.getLogger(__name__)


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]
    
    def get(self, request, *args, **kwargs):
        logger.info(f"Post detail request: post_id={self.kwargs['pk']}, headers={dict(request.headers)}")
        return super().get(request, *args, **kwargs)

    def get_object(self):
        obj = super().get_object()
        logger.info(f"Incrementing read_count for post {obj.id}")
        obj.read_count += 1
        obj.save(update_fields=['read_count'])
        return obj

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'], is_approved=True)

    def create(self, request, *args, **kwargs):
        logger.info(f"Comment creation request: user={request.user}, post_id={self.kwargs['post_id']}, data={request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Serializer validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['post_id'])
            serializer.save(author=self.request.user, post=post, is_approved=False)
        except Exception as e:
            logger.error(f"Comment creation failed: {str(e)}")
            raise

class AdminPostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminCommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminCommentApproveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.is_approved = True
        comment.save()
        return Response({'status': 'approved', 'comment_id': comment.id}, status=status.HTTP_200_OK)

class AdminCommentBlockView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response({'status': 'blocked', 'comment_id': comment.id}, status=status.HTTP_200_OK)

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        if user in post.likes.all():
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)
        post.likes.add(user)
        if user in post.unlikes.all():
            post.unlikes.remove(user)
        return Response({'status': 'liked', 'user_id': user.id}, status=status.HTTP_200_OK)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user
        if user in post.unlikes.all():
            return Response({'status': 'already unliked'}, status=status.HTTP_400_BAD_REQUEST)
        post.unlikes.add(user)
        if user in post.likes.all():
            post.likes.remove(user)
        return Response({'status': 'unliked', 'user_id': user.id}, status=status.HTTP_200_OK)