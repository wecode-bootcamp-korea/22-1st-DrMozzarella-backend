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

class ProductDetailView(View):
    def get(self, request, product_id):
        current_product  = Product.objects.get(id = product_id)

        nutrition = current_product.nutrition

        product = {
            'product_id'       : current_product.id,
            'product_name'     : current_product.name,
            'summary'          : current_product.summary,
            'description'      : current_product.description,
            'score'            : current_product.score,
            'description_image': current_product.description_image_url,
            'image_urls'       : [image.image_url for image in current_product.image_set.all()],
            'categories'       : [
                {
                    "category_id"         : category.id,
                    "category_name"       : category.name,
                    "category_image_url"  : category.image_url,
                    "category_description": category.description
                } for category in current_product.category.all()
            ],
            'option' : [
                {
                    "price"  : option.price,
                    "weight" : option.weight,
                    "option_id"    : option.id
                } for option in current_product.option_set.all()
            ],
            'nutrition' : [
                {
                    field.name : field.value_from_object(nutrition)
                } for field in nutrition._meta.fields if field.name != "id"
            ]
        }

        milk_category    = current_product.category.get(menu__name="milk")
        style_category   = current_product.category.get(menu__name="style")
        country_category = current_product.category.get(menu__name="countries")

        routine_products = [current_product] + list(Product.objects.filter(category=milk_category).exclude(category=style_category)[:2])
        
        routine = [
            {
                'product_id'     : product.id,
                'product_name'   : product.name,
                'score'          : product.score,
                'thumbnail_image': product.thumbnail_image_url,
                'hover_image'    : product.hover_image_url,
                'current'        : (product == current_product),
                'option' : [
                    {
                        "price"  : option.price,
                        "weight" : option.weight,
                        "id"     : option.id
                    } for option in product.option_set.all()]
            } for product in routine_products]

        compare_products = [current_product] + list(Product.objects.filter(category=milk_category).filter(category=style_category).exclude(category=country_category)[:2])

        compare  = [
            {
                'product_name'   : product.name,
                'description'    : product.description,
                'thumbnail_image': product.thumbnail_image_url,
                'option' : [
                    {
                        "price" : option.price,
                        "weight": option.weight,
                        "id"    : option.id
                    } for option in product.option_set.all()]
            } for product in compare_products]

        results = {
            "product" : product,
            "routine" : routine,
            "compare" : compare
        }
            
        return JsonResponse ({"results": results}, status = 200)