from django.urls    import path

from orders.views    import OrderView

urlpatterns = [
    path(''                                    , OrderView.as_view()),
    path('/<int:order_id>'                     , OrderView.as_view()),
    path('/<int:order_id>/<int:order_item_id>' , OrderView.as_view()),
]
