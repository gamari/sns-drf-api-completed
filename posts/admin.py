from django.contrib import admin

from posts.models import Post, PostImage

admin.site.register(Post)
admin.site.register(PostImage)
