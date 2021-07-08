from django.http  import JsonResponse
from django.views import View

from products.models import Menu

class MetaView(View):
    def get(self, request):
        menus = Menu.objects.all()
        
        results = {}
        for menu in menus:
            results[menu.name] = {
                "id": menu.id,
                "categories": [
                    {
                        "id": category.id,
                        "name": category.name,
                        "image_url": category.image_url
                    }
                for category in menu.category_set.all()]
            }

        return JsonResponse({"results": results}, status=200)
