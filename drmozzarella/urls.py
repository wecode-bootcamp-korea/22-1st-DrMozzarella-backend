from django.urls import path, include

from products.views import MetaView

urlpatterns = [
    path('meta', MetaView.as_view()),
]
