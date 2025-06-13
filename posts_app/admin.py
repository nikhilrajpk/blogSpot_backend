from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'read_count')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content',)
    actions = ['approve_comments', 'block_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

    def block_comments(self, request, queryset):
        queryset.update(is_approved=False)
    block_comments.short_description = "Block selected comments"