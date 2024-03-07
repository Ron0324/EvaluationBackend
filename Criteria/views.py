from django.shortcuts import render
from .models import Criteria
from django.http import JsonResponse

def show_criteria(request):
    criteria = Criteria.objects.all().values()
    return JsonResponse(list(criteria), safe=False)

