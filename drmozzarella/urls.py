from django.urls import path, include

urlpatterns = [
    path('events', include('events.urls')),
]
