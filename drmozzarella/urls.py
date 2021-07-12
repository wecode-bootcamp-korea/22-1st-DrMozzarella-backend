from django.urls    import path, include

from products.views import MenuView

urlpatterns = [
    path('menus'    , MenuView.as_view()),
    path('accounts' , include('accounts.urls')),
    path('events'   , include('events.urls')),
]
