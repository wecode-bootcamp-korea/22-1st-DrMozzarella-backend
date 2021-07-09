import json
from operator         import itemgetter

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from products.models  import Category, Option, Product

class ProductsView(View) :
    def get(self,request) :

        try :
            option       = request.GET.get("option","none")
            category_id  = request.GET.get("category_id","all") 
            offset       = int(request.GET.get("offset",0))
            limit        = int(request.GET.get("limit",10)) 
            price_option = request.GET.get("price","desc") 
            q = Q(id = category_id)

            result = [] 
            if Category.objects.filter(q).exists()  :
                category = Category.objects.get(id = category_id)
                result.append({"category":{
                    "id":          category.id,
                    "name":        category.name,
                    "image":       category.image_url,
                    "description": category.description}})
                products = Product.objects.filter(category = category.id)[offset: offset+limit]

                if option == "all":
                    products = Product.objects.all()[offset: offset+limit]

                if option == "best":
                    products = products[:10]

                productlist = []
                keys        = ["id","name","category","description","thumbnail","hover","score","sales","price"]
                for product in products :
                    values  = []
                    price   = product.option_set.all().order_by('-price').first().price
                    values  = [product.id,product.name,category.name,product.description,product.thumbnail_image_url,product.hover_image_url,product.score,product.sales,price]
                    productlist.append(dict(zip(keys,values)))
                
                if option not in (["all","best","none"]) :
                    if price_option == "desc" :
                        productlist = sorted(productlist,key=itemgetter('price'),reverse=True)
                    else :
                        productlist = sorted(productlist,key=itemgetter('price'),reverse=False)

                result.append({"products":productlist})    
            else :
                return JsonResponse({'MESSAGE':'NO DATA'}, status=400)

            return JsonResponse({'MESSAGE':'SUCCESS', "results": result}, status=201)

        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
