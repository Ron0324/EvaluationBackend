from django.shortcuts import render
from .models import Criteria
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EvaluationDate
import json

def show_criteria(request):
    criteria = Criteria.objects.all().values()
    return JsonResponse(list(criteria), safe=False)

@csrf_exempt
def save_evaluation_date(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        semester = data.get('semester', '')
        date_started = data.get('date_started', '')
        date_ended = data.get('date_ended', '')

        if semester and date_started and date_ended:
            EvaluationDate.objects.create(
                semester=semester,
                date_started=date_started,
                date_ended=date_ended
            )
            return JsonResponse({'message': 'EvaluationDate saved successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
