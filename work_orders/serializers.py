from django.utils import timezone
from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    applicant_username = serializers.ReadOnlyField(source='applicant.username')
    class Meta:
        model = WorkOrder
        fields = ['id', 'date', 'duration', 'activity', 'company', 'capacity','applicant_username']
        read_only_fields = ['applicant_username']
        
    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('La fecha no puede ser anterior.')
        return value
    
    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError('La capacidad debe ser al menos 1.')
        return value
        
class WorkOrderApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = ['approver']

    def validate_approver(self, value):
        # Ensure that the user approving the order is a staff member
        if not value.is_staff:
            raise serializers.ValidationError("Solo administradores pueden aprobar ordenes de trabajo.")
        return value