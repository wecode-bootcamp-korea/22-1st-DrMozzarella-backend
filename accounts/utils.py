import jwt
import my_settings

from .models     import Account
from django.http import JsonResponse


def user_validator(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        try:
            if token:
                payload = jwt.decode(token, my_settings.SECRET_KEY, my_settings.algorithm)
                user = Account.objects.get(id = payload["user_id"])
                request.user = user
                return func(self, request, *args, **kwargs)
            
            return JsonResponse({"MESSAGE":"NEED_SIGNIN"}, status = 401)
        
        except jwt.DecodeError:
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"MESSAGE":"EXPIRED_TOKEN"}, status = 401)

        except Account.DoesNotExist:
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)
 
    return wrapper