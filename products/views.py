import json
from operator               import itemgetter

from django.views           import View
from django.http            import JsonResponse

from products.models        import Category, Option, Product

class CategoryView(View) :
    def get(self,request) :

        default_option = "none"
        offset = 0
        limit = 0
        price = "desc"  

        try :
            if "option" in request.GET :
                option = request.GET["option"]
            else :
                option = default_option

            if "category_id" in request.GET :
                category_id = request.GET["category_id"] 
            if "offset" in request.GET :
                offset = int(request.GET["offset"])
            if "limit" in request.GET :
                limit = int(request.GET["limit"]) 
            if "price" in request.GET :
                price = request.GET["price"] 

            result = ["result"] 
            if Category.objects.filter(id = category_id).exists()  :
                category = Category.objects.get(id = category_id)
                if option != "all" :
                    result.append({"cateogories":[{
                        "id":           category.id,
                        "name":         category.name,
                        "image":        category.image_url,
                        "description":  category.description}]})
                products = Product.objects.filter(category = category.id)[offset: offset+limit]

                if option == "all":
                    products = Product.objects.all()[offset: offset+limit]

                if option == "best":
                    products = products[:10]

                productlist = []
                for product in products :
                    price = product.option_set.all().order_by('-price').first().price
                    print('name:',product.name,'price:',price)
                    productlist.append({
                        "id":               product.id,
                        "name":             product.name,
                        "category":         category.name,
                        "description":      product.description,
                        "thumbnail":        product.thumbnail_image_url,
                        "hover":            product.hover_image_url,
                        "score":            product.score,
                        "sales":            product.sales,
                        "price":            price
                    })
                result.append({"products":[productlist]})    

            else :
                return JsonResponse({'MESSAGE':'NO DATA'}, status=400)

        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        return JsonResponse({'MESSAGE':{'SUCCESS': result}}, status=201)