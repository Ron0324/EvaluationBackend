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


def get_evaluation_dates(request):
    evaluation_dates = EvaluationDate.objects.all()
    data = [{'id': date.id, 'semester': date.semester, 'date_started': date.date_started, 'date_ended': date.date_ended} for date in evaluation_dates]
    return JsonResponse(data, safe=False)

@csrf_exempt
def update_evaluation_date(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date_id = data['id']
            date_ended = data['date_ended']

            # Update the corresponding evaluation date in the database
            evaluation_date = EvaluationDate.objects.get(pk=date_id)
            evaluation_date.date_ended = date_ended
            evaluation_date.save()

            return JsonResponse({'message': 'Evaluation date successfully updated.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)