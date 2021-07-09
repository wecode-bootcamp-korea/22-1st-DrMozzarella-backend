from django.views import View
from django.http  import JsonResponse

from events.models import ProductEvent, CategoryEvent

class EventView(View):
    def get(self, request):
        try:
            product_events_count  = int(request.GET.get('product-events-count', 4))
            category_events_count = int(request.GET.get('category-events-count', 2))

            product_events = ProductEvent.objects.all().order_by('-created_at')[:product_events_count]
            category_events = CategoryEvent.objects.all().order_by('-created_at')[:category_events_count]

            product_events_results = [
                {
                        "image_url"  : product_event.image_url,
                        "product_id" : product_event.product_id
                }
            for product_event in product_events]
            

            category_events_results = [
                {
                        "image_url": category_event.image_url,
                        "category_id": category_event.category_id,
                        "title": category_event.title,
                        "description": category_event.description
                }
            for category_event in category_events]
            
            results = {
                "product_events"  : product_events_results,
                "category_events" : category_events_results
            }

            return JsonResponse({"results": results}, status=200)
        
        except IndexError:
            return JsonResponse({"message": "DATABASE_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "INVALID_COUNT"}, status=400)
