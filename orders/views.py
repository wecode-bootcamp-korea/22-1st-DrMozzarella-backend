import json

from django.http    import JsonResponse
from django.views   import View

from products.models import Option
from orders.models   import Cart
from accounts.utils  import user_validator

class CartView(View):
    @user_validator
    def post(self, request):
        try:
            data          = json.loads(request.body)
            cart, created = Cart.objects.get_or_create(account=request.user, option=Option.objects.get(id=data['option_id']))

            if not created:
                cart.quantity += 1
                cart.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except IndexError:
            return JsonResponse({"message": "INDEX_ERROR"}, status=400)

        except Option.DoesNotExist:
            return JsonResponse({"message": "INVALID"}, status=404)

    @user_validator
    def get(self, request):
        carts = Cart.objects.filter(account=request.user)

        results = {
            'carts': [
                {
                    "product_name"        : cart.option.product.name,
                    "thumbnail_image_url" : cart.option.product.thumbnail_image_url,
                    "product_id"          : cart.option.product_id,
                    "option_id"           : cart.option.id,
                    "weight"              : cart.option.weight,
                    "price"               : float(cart.option.price),
                    "quantity"            : cart.quantity,
                    "stocks"              : cart.option.stocks,
                    "availability"        : (cart.option.stocks >= cart.quantity)
                } for cart in carts],
            'total': sum(cart.quantity for cart in carts)
        }

        return JsonResponse({"results": results}, status=200)

    @user_validator
    def patch(self, request, option_id):
        try:
            data = json.loads(request.body)

            if data['quantity'] <= 0:
                return JsonResponse({"message": "INVALID_QUANTITY"}, status=409)

            cart = Cart.objects.get(account=request.user, option_id=option_id)

            cart.quantity = data['quantity']
            cart.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION"}, status=404)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400) 

        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "JSON_ERROR"}, status=400)

    @user_validator
    def delete(self, request, option_id):
        try:
            cart = Cart.objects.get(account=request.user, option_id=option_id)
            cart.delete()

            return JsonResponse({"message": "SUCCESS"}, status=204)
        
        except Cart.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION"}, status=404)
