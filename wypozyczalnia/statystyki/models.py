# statystyki/models.py

from django.db import models

class FinansoweStatystyki(models.Model):
    rok = models.IntegerField()
    przychody = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    koszty = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
