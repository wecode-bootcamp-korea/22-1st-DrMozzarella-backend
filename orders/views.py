from datetime    import date 

from django.http    import JsonResponse
from django.views   import View

from orders.models  import Coupon

class CouponView(View):
    def get(self, request, coupon_code):
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            
            results = {
                'availability'     : date.today() < coupon.expiry_date,
                'discount_percent' : float(coupon.discount_percent),
                'discount_price'   : float(coupon.discount_price)
            }

            return JsonResponse({"results": results}, status=200)
        
        except Coupon.DoesNotExist:
            return JsonResponse({"message": "INVALID_COUPON"}, status=404)

