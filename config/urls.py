from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("admin/", admin.site.urls),
    # local-app
    path("", include("follows.urls")),
    path("posts/", include("posts.urls")),
    path("accounts/", include("accounts.urls")),
    path("likes/", include("likes.urls")),
    path("ai/", include("ai.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
