import json
from operator         import itemgetter
from django.db.models.aggregates import Min
from django.db.models.query import QuerySet

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
                "price_desc"   : "option__price",
                "price_asc"    : "option__price",
                "sales_desc"   : "option__sales",
                "sales_asc"    : "option__sales",
                "best_seller"  : "option__sales",
            }
            offset = offset * limit
            limit  = offset + limit

            where_clause = Q()
            if category_id:
                where_clause.add(Q(category__id=category_id),where_clause.AND)


            print(offset,limit)

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
                            for product in Product.objects.filter(where_clause)\
                            .annotate(sort_value= Max(options[sort_by]) if "desc" in sort_by else Min(options[sort_by])).order_by('sort_value')][offset:limit]

            return JsonResponse({'MESSAGE':'SUCCESS', "results": productlist}, status=201)

        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

