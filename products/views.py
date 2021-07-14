import json

from django.views                import View
from django.http                 import JsonResponse
from django.db.models            import Q
from django.db.models            import Max
from django.db.models.aggregates import Min

from products.models             import Category, Menu, Option, Product

class MenuView(View):
    def get(self, request):
        menus = Menu.objects.all()

        results = {}
        for menu in menus:
            results[menu.name] = {
                "menu_id"    : menu.id,
                "categories" : [
                    {
                        "category_id"          : category.id,
                        "category_name"        : category.name,
                        "category_image_url"   : category.image_url,
                        "category_description" : category.description
                    } for category in menu.category_set.all()]
            }

        return JsonResponse({"results": results}, status=200)

class CategoryView(View):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id = category_id)
            results = {"category_id"           : category.id,
                        "category_name"         : category.name,
                        "category_description"  : category.description,
                        "category_image_url"    : category.image_url
            }   
            return JsonResponse({"results": results }, status=200)

        except Category.DoesNotExist:
            return JsonResponse({"message": "INVALID_CATEGORY_ID"}, status=404)



class ProductsView(View) :
    def get(self,request) :
        try :
            category_id  = request.GET.get("id", 0)
            offset       = int(request.GET.get("offset",0))
            limit        = int(request.GET.get("limit",10))
            sort_by      = request.GET.get("sort_by","price_desc")
            
            options = {
                "price_desc"   : "option__price",
                "price_asc"    : "option__price",
                "sales_desc"   : "option__sales",
                "sales_asc"    : "option__sales"
            }

            offset = offset * limit
            limit  = offset + limit

            q = Q()
            
            if category_id:
                q.add(Q(category__id=category_id),q.AND)

            productlist = [{"product_id"      : product.id,
                            "product_name"    : product.name,
                            "category_id"     : category_id,
                            "descirption"     : product.description,
                            "thumbnail"       : product.thumbnail_image_url,
                            "hover_image"     : product.hover_image_url,
                            "score"           : product.score,
                            "sort_value"      : product.sort_value,
                            "option"          : [{"price"  : option.price,
                                                  "sales"  : option.sales,
                                                  "weight" : option.weight,
                                                  "stocks" : option.stocks} for option in Option.objects.filter(product = product.id)]         
                            }
                            for product in Product.objects.filter(q)\
                            .annotate(sort_value= Max(options[sort_by]) if "desc" in sort_by else Min(options[sort_by]))\
                                .order_by("-sort_value" if "desc" in sort_by else "sort_value")][offset:limit]

            return JsonResponse({'MESSAGE':'SUCCESS', "results": productlist}, status=201)

        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)