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

            category = Category.objects.filter(Q(id=category_id))

            if category.exists():

                if option == "all":
                    order_by_product =  ['-option__price' if price_option =="desc" else 'option__price','name']
                    products = Product.objects.filter().prefetch_related('option_set')

                if option == "best":
                    order_by_price =  ['-option__sales' if price_option =="desc" else 'option__sales','name']
                    product_list = (ProductCategory.objects.filter(Q(category=category_id)).distinct('product').values_list('product', flat=True).distinct())
                    products = Product.objects.filter(pk__in=product_list).order_by(*order_by_price)[offset: offset+limit].values()

                if option == "none":
                    order_by_price =  ['-option__price' if price_option =="desc" else 'option__price','name']
                    product_list = (ProductCategory.objects.filter(Q(category=category_id)).distinct('product').values_list('product', flat=True).distinct())
                    products = Product.objects.filter(pk__in=product_list).order_by(*order_by_price)[offset: offset+limit].values()

                print(products,product_list)    

                # category_menu = [{"category_id"        : info.id,
                #                 "category_name"        : info.name,
                #                 "category_image_url"   : info.image_url,
                #                 "category_description" : info.description}
                #                 for info in category]
                # result.append({"category":category_menu})
                # productlist = [{"product_id"       : product.id,
                #                 "product_name"     : product.name,
                #                 "descirption"      : product.description,
                #                 "thumbmail_image"  : product.thumbnail_image_url,
                #                 "hover_image"      : product.hover_image_url,
                #                 "score"            : product.score,
                #                 "sales"            : product.sales,
                #                 "price"            : product.max_price,
                #                 "option"           : list(Product.objects.filter(Q(id=product.id)).prefetch_related('option_set').values('option__price','option__sales','option__weight'))
                #                                     if Product.objects.filter(id =product.id).prefetch_related('option_set').values('option__price','option__sales','option__weight').count() > 1
                #                                     else []
                #                 }
                #                 for product in products]
                # result.append({"products":productlist})

                return JsonResponse({'MESSAGE':'SUCCESS', "results": result}, status=201)

            else :
                return JsonResponse({'MESSAGE':'NO DATA'}, status=400)
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

