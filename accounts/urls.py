from django.urls import path

from accounts.views import AccountDetailView, CreateAccountView, MeView

urlpatterns = [
    path("", CreateAccountView.as_view()),
    path("me/", MeView.as_view()),
    path("<uuid:id>/", AccountDetailView.as_view()),
]
