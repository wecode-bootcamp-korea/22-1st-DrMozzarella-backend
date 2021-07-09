import json
import uuid

from django.http    import JsonResponse
from django.views   import View

from orders.models  import Cart, Order, OrderItem, ItemStatus, OrderStatus

class CartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = 1
            if Cart.objects.filter(account_id=user_id, option_id=data['option_id']).exists():
                cart = Cart.objects.get(account_id=user_id, option_id=data['option_id'])

                if data['quantity'] > 0:
                    cart.quantity = data['quantity']
                    cart.save()
                else:
                    return JsonResponse({"message": "INVALID_QUANTITY"}, status=409)

            else:
                Cart.objects.create(
                    account_id = user_id,
                    option_id  = data['option_id'],
                    quantity   = data['quantity']
                )

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
                "option_id"           : cart.option.id,
                "weight"              : cart.option.weight,
                "price"               : cart.option.price,
                "quantity"            : cart.quantity
            }
        for cart in carts]

        return JsonResponse({"results": results}, status=200)

    def delete(self, request, option_id):
        try:
            user_id = 1
            cart = Cart.objects.get(account_id=user_id, option_id=option_id)
            cart.delete()

            return JsonResponse({"message": "SUCCESS"}, status=204)
        
        except Cart.DoesNotExist:
            return JsonResponse({"message": "INVALID_OPTION"}, status=400)

class OrderView(View):
    def post(self, request):
        try:
            user_id = 1
            data = json.loads(request.body)
            carts = Cart.objects.filter(account_id=user_id)

            if carts.exists():
                order = Order.objects.create(
                    account_id   = user_id,
                    order_number = uuid.uuid4(),
                    order_status = OrderStatus.objects.get(status_name=data['order_status'])
                )
                
                for cart in carts:
                    OrderItem.objects.create(
                        order_id    = order.id,
                        option_id   = cart.option.id,
                        quantity    = cart.quantity,
                        item_status = ItemStatus.objects.get(status_name=data['item_status'])
                    )
                
                carts.delete()

                return JsonResponse({"message": "SUCCESS"}, status=200)

            else:
                return JsonResponse({"message":"EMPTY_CART"}, status=400)

        except IndexError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
