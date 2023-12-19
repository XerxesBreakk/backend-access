from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from accounts.models import UserAccount

class WorkOrder(models.Model):
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    duration = models.DurationField()
    activity= models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    company = models.CharField(max_length=255)
    applicant = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='applicant')
    approver = models.ForeignKey(UserAccount, on_delete=models.CASCADE,null=True, blank=True, related_name='approver')
    pin = models.CharField(max_length=10,blank=True)
    
    def __str__(self):
        return f'Orden de Trabajo {self.id} - {self.applicant.username}'

    def clean_date(self):
        # Validación personalizada para la fecha
        if self.date < timezone.now():
            raise ValidationError('La fecha no puede ser anterior a la fecha actual.')

    def clean_approver(self):
        # Validación personalizada para user_1
        if not self.approver.is_staff:
            raise ValidationError('El usuario debe ser administrador.')