from django.urls    import path

from orders.views    import OrderView, CartView, CouponView 

urlpatterns = [
    path(''                           , OrderView.as_view()),
    path('/<int:order_id>'            , OrderView.as_view()),
    path('/cart'                      , CartView.as_view()),
    path('/cart/<int:option_id>'      , CartView.as_view()),
    path('/coupons/<str:coupon_code>' , CouponView.as_view())
]
