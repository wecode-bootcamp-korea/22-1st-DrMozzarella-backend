from django.urls    import path

from orders.views    import CartView, OrderView

urlpatterns = [
    path(''                      , OrderView.as_view()),
    path('/cart'                 , CartView.as_view()),
    path('/cart/<int:option_id>' , CartView.as_view())
]
