from django.contrib import admin

from blog_app.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'is_published', 'title', 'views_count', )
    list_filter = ('is_published',)
    search_fields = ('title', 'body',)
