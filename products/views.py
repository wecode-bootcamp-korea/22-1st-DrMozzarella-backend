import json

from django.views                import View
from django.http                 import JsonResponse
from django.db.models            import Q, Max, Min, Sum

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
            category_id  = request.GET.get("category", 0)
            offset       = int(request.GET.get("offset",0))
            limit        = int(request.GET.get("limit",10))
            sort_by      = request.GET.get("sort","price-descending")

            options = {
                "price-descending"   : "-max_price",
                "price-ascending"    : "min_price",
                "sales-descending"   : "-total_sales",
                "sales-ascending"    : "total_sales",
                "score-descending"   : "-score",
                "score-ascending"    : "score"
            }

            category = Category.objects.get(id=category_id)

            if category.name == "all":
                q = Q()
            elif category.name == "bestsellers":
                q = Q(total_sales__gte=10000)
            else:
                q = Q(category__id=category_id)

            products = Product.objects.prefetch_related('option_set')\
                .annotate(total_sales=Sum('option__sales'))\
                .annotate(max_price=Max('option__price'))\
                .annotate(min_price=Min('option__price'))\
                .filter(q).order_by(options[sort_by])

            results = [
                {
                    "product_id"      : product.id,
                    "product_name"    : product.name,
                    "category_id"     : category_id,
                    "description"     : product.description,
                    "thumbnail"       : product.thumbnail_image_url,
                    "hover_image"     : product.hover_image_url,
                    "score"           : product.score,
                    "option"          : [
                        {
                            "price"  : option.price,
                            "sales"  : option.sales,
                            "weight" : option.weight,
                            "stocks" : option.stocks
                        } for option in product.option_set.all()
                    ]         
                } for product in products[offset*limit:offset*limit+limit]
            ] 

            return JsonResponse({"results": results}, status=200)

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({"message": "INVALID_CATEGORY_ID"}, stautus=400)



class ProductDetailView(View):
    def get(self, request, product_id):
        current_product = Product.objects.select_related('nutrition')\
            .prefetch_related('category', 'option_set', 'image_set', 'category__menu')\
            .get(id=product_id)

        current_category_dict = {}
        for category in current_product.category.all():
            current_category_dict[category.menu.name] = category

        routine_products = [current_product]
        compare_products = [current_product]

        products = Product.objects.all().prefetch_related('category', 'option_set')

        for product in products:
            if current_category_dict["milk"] in product.category.all():
                if current_category_dict["style"] not in product.category.all():
                    routine_products.append(product)

                elif current_category_dict["countries"] not in product.category.all():
                    compare_products.append(product)

            if len(routine_products) >= 3 and len(compare_products) >=3:
                break

        product_result = {
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
                    "price"     : option.price,
                    "weight"    : option.weight,
                    "option_id" : option.id
                } for option in current_product.option_set.all()
            ],
            'nutrition' : [
                {
                    field.name : field.value_from_object(current_product.nutrition)
                } for field in current_product.nutrition._meta.fields if field.name != "id"
            ]
        }

        routine_results = [
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
            } for product in routine_products[:3]
        ]

        compare_results  = [
            {
                'product_name'   : product.name,
                'description'    : product.description,
                'thumbnail_image': product.thumbnail_image_url,
                'option' : [
                    {
                        "price" : option.price,
                        "weight": option.weight,
                        "id"    : option.id
                    } for option in product.option_set.all()
                ]
            } for product in compare_products[:3]
        ]

        results = {
            "product" : product_result,
            "routine" : routine_results,
            "compare" : compare_results
        }

        return JsonResponse ({"results": results}, status = 200)
