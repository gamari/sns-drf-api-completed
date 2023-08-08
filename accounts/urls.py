from django.urls import path

from accounts.views import (
    AccountRetrieveUpdateView,
    CreateAccountView,
    MeView,
)

urlpatterns = [
    path("", CreateAccountView.as_view()),
    path("me/", MeView.as_view()),
    path("<uuid:id>/", AccountRetrieveUpdateView.as_view()),
]
