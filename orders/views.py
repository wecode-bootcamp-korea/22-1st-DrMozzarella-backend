import json
import uuid

from django.http    import JsonResponse
from django.views   import View

from orders.models  import Cart, Order, OrderItem, ItemStatus, OrderStatus

class CartView(View):
    def post(self, request):
        try:
            user_id       = 1
            data          = json.loads(request.body)
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
                "price"               : float(cart.option.price),
                "quantity"            : cart.quantity,
                "stocks"              : cart.option.stocks,
                "availability"        : (cart.option.stocks >= cart.quantity)
            } for cart in carts]

        return JsonResponse({"results": results}, status=200)

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
            carts = Cart.objects.filter(account_id=user_id)

            if carts.exists():
                order = Order.objects.create(
                    account_id   = user_id,
                    order_number = uuid.uuid4(),
                    status = OrderStatus.objects.get(name="Pending")
                )
                
                for cart in carts:
                    if cart.quantity > cart.option.stocks:
                        order.delete()
                        return JsonResponse({"messeage": "INVALID_QUANTITY"}, status=400)

                    OrderItem.objects.create(
                        order_id  = order.id,
                        option_id = cart.option.id,
                        quantity  = cart.quantity,
                        status    = ItemStatus.objects.get(name="Pending")
                    )
                    cart.option.stocks -= cart.quantity
                    cart.option.sales  += cart.quantity
                    cart.option.save()
                
                carts.delete()

                return JsonResponse({"message": "SUCCESS"}, status=200)

            else:
                return JsonResponse({"message":"EMPTY_CART"}, status=400)

        except IndexError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    def get(self, request):
        user_id = 1
        orders  = reversed(Order.objects.filter(account_id=user_id))
        
        results = [
            {
                "order_id"       : order.id,
                "order_number"   : order.order_number,
                "order_status"   : order.status.name,
                "ordered_at"     : order.ordered_at,
                "order_products" : [
                    {
                        "order_item_id"     : orderitem.id,
                        "product_id"        : orderitem.option.product_id,
                        "product_name"      : orderitem.option.product.name,
                        "product_image_url" : orderitem.option.product.thumbnail_image_url,
                        "quantity"          : orderitem.quantity,
                        "option_id"         : orderitem.option_id,
                        "weight"            : orderitem.option.weight,
                        "price"             : float(orderitem.option.price),
                        "item_status"       : orderitem.status.name
                    } for orderitem in order.orderitem_set.all()]
            } for order in orders]

        return JsonResponse({"results": results}, status=200)

    def put(self, request, order_id):
        user_id = 1
        
        try:
            data = json.loads(request.body)
            order = Order.objects.get(id = order_id, account_id = user_id)
            
            order.status = OrderStatus.objects.get(name = data['order_status'])
            order.save()
            
            return JsonResponse({"message": "SUCCESS"}, status=201)
        
        except Order.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER_ID"}, status=400)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def patch(self, request, order_id, order_item_id):
        user_id = 1

        try:
            data = json.loads(request.body)
            order_item = OrderItem.objects.get(
                id                = order_item_id,
                order_id          = order_id,
                order__account_id = user_id
            )
            order_item.status = ItemStatus.objects.get(name = data['item_status'])
            order_item.save()
            
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except OrderItem.DoesNotExist:
            return JsonResponse({"message": "INVALID_ITEM"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
