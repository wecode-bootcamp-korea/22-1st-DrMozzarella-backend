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
        
        if not re.search(EMAIL_REGES, data["email"]):
            return JsonResponse ({"MESSAGE":"INVALID EMAIL"}, status = 400)
        
        if not re.search(PASSWORD_REGES, data["password"]):
            return JsonResponse ({"MESSAGE": "INVALID PASSWORD"}, status = 400)

        if Account.objects.filter(email=data["email"]).exists():
            return JsonResponse ({"MESSAGE":"EXISTED EMAIL"}, status = 400)
        
        hashed_passwored = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode()
        
        try:
            Account.objects.create(
                name     = data["name"],
                email    = data["email"],
                password = hashed_passwored,
                address  = data["address"]
            )
            return JsonResponse ({"MESSAGE":"SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse ({"MESSAGE":"KEY_ERROR"}, status = 400)