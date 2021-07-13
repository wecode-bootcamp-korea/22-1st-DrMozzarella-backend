from django.urls    import path

from orders.views    import CartView

urlpatterns = [
    path('/cart'                               , CartView.as_view()),
    path('/cart/<int:option_id>'               , CartView.as_view()),
]
