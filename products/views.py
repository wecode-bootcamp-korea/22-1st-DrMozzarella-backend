import json
from operator         import itemgetter

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from django.db.models import Count

from .models  import Category, Option, Product, ProductCategory

class ProductsView(View) :
    def get(self,request) :
        try :
            category_id  = request.GET.get("id",0)
            option       = request.GET.get("option","none")
            offset       = int(request.GET.get("offset",0))
            limit        = int(request.GET.get("limit",10))
            price_option = request.GET.get("price","desc")
            category     = None
            products     = None
            result = []

            if option == "all" :
                category = Category.objects.all().filter(Q(id=category_id) and Q(name="all"))

            if option == "best" :
                category = Category.objects.all().filter(Q(id=category_id) and Q(name="bestsellers"))

            if option == "none" :
                category = Category.objects.filter(Q(id=category_id))

            if category.exists():

                if option == "all":
                    order_by_product =  ['-max_price' if price_option =="desc" else 'max_price','name']
                    products = Product.objects.all().order_by(*order_by_product)[offset: offset+limit]

                if option == "best":
                    order_by_sales =  ['-sales' if price_option =="desc" else 'sales','name']
                    products = Product.objects.all().order_by(*order_by_sales)[offset: offset+limit]

                if option == "none":
                    order_by_price =  ['-max_price' if price_option =="desc" else 'max_price','name']
                    product_list = (ProductCategory.objects.filter(Q(category=category_id)).distinct('product').values_list('product', flat=True).distinct())
                    products = Product.objects.filter(pk__in=product_list).order_by(*order_by_price)

                category_menu = [{"id"          : info.id,
                                "name"          : info.name,
                                "iamge"         : info.image_url,
                                "descirption"   : info.description}
                                for info in category]
                result.append({"category":category_menu})  
                productlist = [{"id"            : product.id,
                                "name"          : product.name,
                                "descirption"   : product.description,
                                "iamge"         : product.thumbnail_image_url,
                                "hover"         : product.hover_image_url,
                                "score"         : product.score,
                                "sales"         : product.sales,
                                "price"         : product.max_price,
                                "option"        : list(Product.objects.filter(Q(id=product.id)).prefetch_related('option_set').values('option__price','option__sales','option__weight')) 
                                                    if Product.objects.filter(id =product.id).prefetch_related('option_set').values('option__price','option__sales','option__weight').count() > 1 
                                                    else []
                                }
                                for product in products]
                result.append({"products":productlist})

                return JsonResponse({'MESSAGE':'SUCCESS', "results": result}, status=201)

            else :
                return JsonResponse({'MESSAGE':'NO DATA'}, status=400)
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

