from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import handel_address 

@csrf_exempt
def analyze_address(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            street = data.get("street")
            house_number = data.get("houseNumber")
            
            if not street:
                return JsonResponse({"error": "Missing 'street' field"}, status=400)
            if not house_number: 
                return JsonResponse({"error": "Missing 'house number' field"}, status=400)
            response_data = handel_address(street, house_number, radius=50)  
            return JsonResponse(response_data)  

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)


@csrf_exempt
def get_streets(request):
    with open('api/data/streets.json', 'r', encoding='utf-8') as f:
        street_data = json.load(f)
    street_names = street_data.get("t_rechov_values", [])
    return JsonResponse({"streets": street_names})