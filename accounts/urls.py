from django.urls import path

from accounts.views import CreateAccountView, MeView

urlpatterns = [
    path("", CreateAccountView.as_view()),
    path("me/", MeView.as_view()),
]