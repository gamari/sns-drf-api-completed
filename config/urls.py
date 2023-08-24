from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # local-app
    path("", include("follows.urls")),
    path("posts/", include("posts.urls")),
    path("accounts/", include("accounts.urls")),
    path("likes/", include("likes.urls")),
    path("ai/", include("ai.urls")),
]

# 本番では管理者画面は使わないようにする
if config("MODE", None) != "production":
    urlpatterns += [path('admin/', admin.site.urls)]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
