from django.urls import path

from ai.views import GenerateTweetsView


urlpatterns = [
    path("tweets/generate/", GenerateTweetsView.as_view()),
]