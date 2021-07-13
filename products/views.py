from django.http  import JsonResponse
from django.views import View

from products.models import Menu, Category, Product

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

class ProductDetailView(View):
    def get(self, request, product_id):
        current_product  = Product.objects.get(id = product_id)

        nutrition = current_product.nutrition

        product = {
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
                'thumbmail_image': product.thumbnail_image_url,
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
                'thumbmail_image': product.thumbnail_image_url,
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
