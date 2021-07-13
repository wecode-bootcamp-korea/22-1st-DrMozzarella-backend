import jwt

from .models     import Account
from django.http import JsonResponse
from my_settings import SECRET_KEY, ALGORITHM

def user_validator(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        try:
            if token:
                payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
                user         = Account.objects.get(id = payload["user_id"])
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