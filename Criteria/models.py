from django.db import models

class Criteria (models.Model):
    criteria_a = models.CharField(max_length=250)
    criteria_b = models.CharField(max_length=250)
    criteria_c = models.CharField(max_length=250)
    criteria_d = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.criteria_a} - {self.criteria_b} - {self.criteria_c} - {self.criteria_d}"
    
    class Meta:
        db_table = 'Criteria'

class EvaluationDate (models.Model):
    semester = models.CharField(max_length = 15)
    date_started = models.DateField()
    date_ended = models.DateField()
    
    class Meta:
        db_table = 'EvaluationDate'