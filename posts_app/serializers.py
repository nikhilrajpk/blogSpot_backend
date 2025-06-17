from rest_framework import serializers
from .models import Post, Comment
from auth_app.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_title', 'author', 'content', 'created_at', 'is_approved']
        read_only_fields = ['author', 'created_at', 'is_approved', 'post']
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Comment must be at least 5 characters long.")
        if len(value) > 500:
            raise serializers.ValidationError("Comment cannot exceed 500 characters.")
        return value

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    likes_count = serializers.SerializerMethodField()
    unlikes_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    unlikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'image', 'created_at', 'updated_at', 'read_count', 'likes', 'unlikes', 'likes_count', 'unlikes_count', 'comments']
        read_only_fields = ['author', 'created_at', 'updated_at', 'read_count', 'likes', 'unlikes']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_unlikes_count(self, obj):
        return obj.unlikes.count()
    
    def get_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True)
        return CommentSerializer(approved_comments, many=True).data
    
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError("Title cannot exceed 100 characters.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        if len(value) > 5000:
            raise serializers.ValidationError("Content cannot exceed 5000 characters.")
        return value

    def validate_image(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file size cannot exceed 5MB.")
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            ext = value.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError("Image must be a JPG, JPEG, PNG, or GIF file.")
        return value