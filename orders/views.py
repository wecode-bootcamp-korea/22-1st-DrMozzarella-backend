import json
import uuid

from django.http    import JsonResponse
from django.views   import View

from orders.models  import Cart, Order, OrderItem, OrderStatus, ItemStatus
from accounts.utils import user_validator

class OrderView(View):
    @user_validator
    def post(self, request):
        try:
            carts = Cart.objects.filter(account=request.user)

            if carts:
                order = Order.objects.create(
                    account      = request.user,
                    order_number = uuid.uuid4(),
                    status       = OrderStatus.objects.get(name="Pending")
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

    @user_validator
    def get(self, request):
        orders  = Order.objects.filter(account=request.user).order_by('-ordered_at')
        
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

    @user_validator
    def put(self, request, order_id):
        try:
            data  = json.loads(request.body)
            order = Order.objects.get(id=order_id, account=request.user)
            
            order.status = OrderStatus.objects.get(name = data['order_status'])
            order.save()
            
            return JsonResponse({"message": "SUCCESS"}, status=201)
        
        except Order.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER_ID"}, status=404)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    @user_validator
    def patch(self, request, order_id, order_item_id):
        try:
            data       = json.loads(request.body)
            order_item = OrderItem.objects.get(
                id             = order_item_id,
                order_id       = order_id,
                order__account = request.user
            )
            order_item.status = ItemStatus.objects.get(name = data['item_status'])
            order_item.save()
            
            return JsonResponse({"message": "SUCCESS"}, status=201)

        except OrderItem.DoesNotExist:
            return JsonResponse({"message": "INVALID_ITEM"}, status=404)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
