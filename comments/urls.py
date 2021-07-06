from django.urls import path

from comments.views import CommentView

urlpatterns = [
    path('/<int:product_id>', CommentView.as_view()),
]

