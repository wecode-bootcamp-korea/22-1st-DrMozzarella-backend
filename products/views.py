from django.http  import JsonResponse
from django.views import View

from products.models import Menu

class MenuView(View):
    def get(self, request):
        menus = Menu.objects.all()
        
        results = [
            {
                "menu_id"    : menu.id,
                "menu_name"  : menu.name,
                "categories" : [
                    {
                        "category_id"          : category.id,
                        "category_name"        : category.name,
                        "category_image_url"   : category.image_url,
                        "category_description" : category.description
                    } for category in menu.category_set.all()]
            } for menu in menus]

        return JsonResponse({"results": results}, status=200)
