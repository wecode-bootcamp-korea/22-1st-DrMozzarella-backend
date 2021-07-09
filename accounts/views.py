import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from accounts.models import Account
from my_settings     import SECRET_KEY

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        EMAIL_REGES    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        PASSWORD_REGES = '[A-Za-z0-9@#$%^&+=]{8,}'
        try:
            if not re.search(EMAIL_REGES, data["email"]):
                return JsonResponse ({"MESSAGE":"INVALID EMAIL"}, status = 400)
            
            if not re.search(PASSWORD_REGES, data["password"]):
                return JsonResponse ({"MESSAGE": "INVALID PASSWORD"}, status = 400)

            if Account.objects.filter(email=data["email"]).exists():
                return JsonResponse ({"MESSAGE":"EXISTED EMAIL"}, status = 400)
            
            hashed_passwored = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode()
        
            Account.objects.create(
                name     = data["name"],
                email    = data["email"],
                password = hashed_passwored,
                address  = data["address"]
            )
            return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse ({"MESSAGE":"KEY_ERROR"}, status = 400)

class SigninView(View):
    def get(self, request):
        data = json.loads(request.body)
        
        try:
            user = Account.objects.get(email=data["email"])
            if not Account.objects.get(email=data["email"]).exists():
                return JsonResponse({"MESSAGE":"INVALID USER"}, status = 400)

            if bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
                access_token = jwt.encode({"user_id":user.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse ({"MESSAGE":"SUCCESS", "TOKEN":access_token}, status = 200)

            return JsonResponse({"MESSAGE":"INVALID USER"}, status = 400)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY ERROR"}, status = 401)