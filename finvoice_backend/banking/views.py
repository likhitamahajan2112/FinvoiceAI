from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Existing views
def login_view(request):
    # Example placeholder
    return JsonResponse({"message": "Login endpoint"})

def balance_view(request):
    return JsonResponse({"balance": 12450.80})

def transactions_view(request):
    return JsonResponse({"transactions": [
        {"merchant": "Amazon Marketplace", "amount": -84.20},
        {"merchant": "Starbucks Coffee", "amount": -12.50}
    ]})

def transfer_view(request):
    return JsonResponse({"status": "Transfer successful"})

# New input view for your frontend form
@csrf_exempt
def input_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            account = data.get("account")
            password = data.get("password")
            return JsonResponse({
                "status": "success",
                "account": account,
                "password": password
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)