import json
from operator         import itemgetter

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from django.db.models import Count, Max

from .models  import Category, Option, Product

class ProductsView(View) :
    def get(self,request) :
        try :
            category_id  = request.GET.get("id",0)
            offset       = int(request.GET.get("offset",0))
            limit        = int(request.GET.get("limit",10))
            sort_by = request.GET.get("sort_by","price_desc")
            result = []

            options = {
                "price_desc"   : "-option__price",
                "price_asc"    : "option__price",
                "sales_desc"   : "-option__sales",
                "sales_asc"    : "option__sales",
                "best_option"  : "-option__sales"
            }


            print(Option.objects.select_related('product').filter(product_id = 2).values("weight","price").count())

            category = Category.objects.filter(id=category_id)
            if category.exists():
                products = Product.objects.filter(category = list(category.values_list('id',flat=True))[0])\
                .annotate(max_price = Max('option__price'))\
                .annotate(max_sales = Max('option__sales'))\
                .order_by(options[sort_by])[offset: offset+limit]


                productlist = [{"id"            : product.id,
                                "name"          : product.name,
                                "descirption"   : product.description,
                                "iamge"         : product.thumbnail_image_url,
                                "hover"         : product.hover_image_url,
                                "score"         : product.score,
                                "sales"         : product.max_sales,
                                "price"         : product.max_price,
                                "option"        : [{option.weight,option.price} for option in Option.objects.select_related('product').filter(product_id = product.id).values()]
                                }
                                for product in products]
                result.append({"products":productlist})
                return JsonResponse({'MESSAGE':'SUCCESS', "results": result}, status=201)
            else :
                return JsonResponse({'MESSAGE':'Invalid Category'}, status=400)
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

