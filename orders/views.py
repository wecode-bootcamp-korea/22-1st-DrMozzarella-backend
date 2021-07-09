import json
import uuid

from django.http    import JsonResponse
from django.views   import View

from orders.models  import Cart, Order, OrderItem, ItemStatus, OrderStatus

class CartView(View):
    def post(self, request):
        try:
            user_id = 1
            data = json.loads(request.body)
            cart, created = Cart.objects.get_or_create(account_id=user_id, option_id=data['option_id'])

            if not created:
                cart.quantity += 1
                cart.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except IndexError:
            return JsonResponse({"message": "INDEX_ERROR"}, status=400)

    def get(self, request):
        user_id = 1
        carts = Cart.objects.filter(account_id=user_id)

        results = [
            {
                "product_name"        : cart.option.product.name,
                "thumbnail_image_url" : cart.option.product.thumbnail_image_url,
                "product_id"          : cart.option.product_id,
                "option_id"           : cart.option.id,
                "weight"              : cart.option.weight,
                "price"               : cart.option.price,
                "quantity"            : cart.quantity
            } for cart in carts]

        return JsonResponse({"results": results}, status=200)

    def delete(self, request, option_id):
        try:
            user_id = 1
            cart = Cart.objects.get(account_id=user_id, option_id=option_id)
            cart.delete()

            return JsonResponse({"message": "SUCCESS"}, status=204)
        
        except Cart.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION"}, status=400)

    def patch(self, request, option_id):
        try:
            user_id = 1
            data = json.loads(request.body)
            cart = Cart.objects.get(account_id=user_id, option_id=option_id)

            if data['quantity'] <= 0:
                return JsonResponse({"message": "INVALID_QUANTITY"}, status=409)

            cart.quantity = data['quantity']
            cart.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400) 

        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class OrderView(View):
    def post(self, request):
        try:
            user_id = 1
            data  = json.loads(request.body)
            carts = Cart.objects.filter(account_id=user_id)

            if carts.exists():
                order = Order.objects.create(
                    account_id   = user_id,
                    order_number = uuid.uuid4(),
                    order_status = OrderStatus.objects.get(status_name=data['order_status'])
                )
                
                for cart in carts:
                    quantity = min(cart.quantity, cart.option.product.stocks)

                    OrderItem.objects.create(
                        order_id    = order.id,
                        option_id   = cart.option.id,
                        quantity    = quantity,
                        item_status = ItemStatus.objects.get(status_name=data['item_status'])
                    )
                    cart.option.product.stocks -= quantity
                    cart.option.product.sales  += quantity
                    cart.option.product.save()
                
                carts.delete()

                return JsonResponse({"message": "SUCCESS"}, status=200)

            else:
                return JsonResponse({"message":"EMPTY_CART"}, status=400)

        except IndexError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    def get(self, request):
        user_id = 1
        orders = Order.objects.filter(account_id=user_id)
        
        results = [
            {
                "order_number": order.order_number,
            } for order in orders]

        return JsonResponse({"results": "message"})
