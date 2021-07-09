from django.urls import path

from events.views   import EventView

urlpatterns = [
    path('meta', EventView.as_view()),
]
