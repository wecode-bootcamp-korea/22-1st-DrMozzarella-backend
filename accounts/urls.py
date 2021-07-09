from django.urls import path

from accounts.views import SignupView, SigninView

urlpatterns = [
	path('/signup', SignupView.as_view()),
	path('/signin', SigninView.as_vew())
]