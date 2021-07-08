from django.views import View
from django.http  import JsonResponse

from events.models import ProductEvent, CategoryEvent

class EventView(View):
    def get(self, request):
        try:
            product_events = ProductEvent.objects.all().order_by('-created_at')[:4]
            category_events = CategoryEvent.objects.all().order_by('-created_at')[:2]

            product_events_results = []
            for product_event in product_events:
                product_events_results.append(
                    {
                        "image_url"  : product_event.image_url,
                        "product_id" : product_event.product_id
                    }
                )

            category_events_results = []
            for category_events in category_events:
                category_events_results.append(
                    {
                        "image_url": category_events.image_url,
                        "category_id": category_events.category_id,
                        "title": category_events.title,
                        "description": category_events.description
                    }
                )
            
            results = {
                "product_events"  : product_events_results,
                "category_events" : category_events_results
            }

            return JsonResponse({"results": results}, status=200)
        
        except IndexError:
            return JsonResponse({"message": "DATABASE_ERROR"}, status=400)
