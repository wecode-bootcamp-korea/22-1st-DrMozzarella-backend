from os import PRIO_PROCESS
from DrMozzarella.products.models import Nutrition, Option
import json

from django.http import JsonResponse
from django.views import View

from products.models import Product



class ProductView(View):
    def get(self, request):
        data = json.loads(request.body)

        products = Product.objects.all()
        product_list = []

        for product in products:
            product_dict = {
                'product_name': product.name,
                'description' : product.description,
                'nutrition'   : Nutrition.objects.get(pk=data["nutrition"]),
                'sales'       : product.sales,
                'stocks'      : product.stocks,
                'score'       : product.score,
                'thumbnail_1' : product.thumbnail_1_url,
                'thumbnail_2' : product.thunbnail_2_url
                price
                weight
                

            }
            product_list.append(product_dict)
            return JsonResponse({"RESULT":product_list}, status = 200)