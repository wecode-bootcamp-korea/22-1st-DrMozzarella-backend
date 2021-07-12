from django.urls    import path

from events.views   import EventView

urlpatterns = [
    path('', EventView.as_view()),
]
