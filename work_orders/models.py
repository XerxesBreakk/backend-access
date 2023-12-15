from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class WorkOrder(models.Model):
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    duration = models.DurationField()
    activity= models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applicant')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approver')
    pin = models.CharField(max_length=10,blank=True)

    def clean_date(self):
        # Validación personalizada para la fecha
        if self.date < timezone.now():
            raise ValidationError('La fecha no puede ser anterior a hoy.')

    def clean_applicant(self):
        # Validación personalizada para user_1
        if not self.user_1.is_staff:
            raise ValidationError('El usuario debe ser administrador.')