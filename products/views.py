import json
from operator         import itemgetter

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from django.db.models import Count, Max

from .models          import Category, Option, Product

class ProductsView(View) :
    def get(self,request) :
        try :
            category_id  = request.GET.get("id", 0)
            offset       = int(request.GET.get("offset",0))
            limit        = int(request.GET.get("limit",10))
            sort_by      = request.GET.get("sort_by","price_desc")
            
            options = {
                "price_desc"   : "-option__price",
                "price_asc"    : "option__price",
                "sales_desc"   : "-option__sales",
                "sales_asc"    : "option__sales",
                "best_seller"  : "-option__sales",
            }
            
            offset = offset * limit
            limit  = limit * offset

            where_clause = Q()
            if category_id:
                where_clause.add(Q(category__id=category_id),where_clause.AND)
 
            productlist = [{"product_id"      : product.id,
                            "product_name"    : product.name,
                            "category_id"     : category_id,
                            "descirption"     : product.description,
                            "thumbmail_image" : product.thumbnail_image_url,
                            "hover_image"     : product.hover_image_url,
                            "score"           : product.score,
                            "sales"           : product.max_sales,
                            "price"           : product.max_price,
                            "stocks"          : product.max_stock,
                            "option"          : [{"pricde" : option.price,
                                                  "sales"  : option.sales,
                                                  "weight" : option.weight,
                                                  "stocks" : option.stocks} for option in product.option_set.all()]         
                            }
                            for product in Product.objects.filter(where_clause)\
                                            .annotate(max_price = Max('option__price'))\
                                            .annotate(max_sales = Max('option__sales'))\
                                            .annotate(max_stock = Max('option__stocks'))\
                                            .order_by(options[sort_by])[offset : limit]]

            return JsonResponse({'MESSAGE':'SUCCESS', "results": productlist}, status=201)

        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

