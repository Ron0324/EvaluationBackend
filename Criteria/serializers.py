from django.http import JsonResponse
from .models import EvaluationDate
import json

def get_evaluation_dates(request):
    evaluation_dates = EvaluationDate.objects.all()
    data = [{'id': date.id, 'semester': date.semester, 'date_started': date.date_started, 'date_ended': date.date_ended} for date in evaluation_dates]
    return JsonResponse(data, safe=False)