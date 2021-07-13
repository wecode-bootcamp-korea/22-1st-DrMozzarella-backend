from django.urls    import path

from orders.views    import CouponView 

urlpatterns = [
    path('/coupons/<str:coupon_code>', CouponView.as_view())
]
