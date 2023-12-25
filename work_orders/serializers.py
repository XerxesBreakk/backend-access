from django.utils import timezone
from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    applicant_username = serializers.ReadOnlyField(source='applicant.username')
    class Meta:
        model = WorkOrder
        fields = ['id', 'date', 'duration', 'activity', 'company', 'capacity','pin','is_active','applicant_username']
        read_only_fields = ['is_active','pin','applicant_username']
        
    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('La fecha no puede ser anterior.')
        return value
    
    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError('La capacidad debe ser al menos 1.')
        return value
        
class WorkOrderApprovalSerializer(serializers.Serializer):
    pass  # No need for additional fields for this case