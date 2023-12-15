from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = ['id', 'date', 'duration', 'activity', 'company', 'capacity', 'pin', 'approver']
        read_only_fields = ['pin', 'approver']
        
        def create(self, validated_data):
            # Al crear, eliminamos pin y approver del validated_data
            pin = validated_data.pop('pin', None)
            approver = validated_data.pop('approver', None)

            # Luego, llamamos al método create del modelo y obtenemos la instancia
            instance = super().create(validated_data)

            # Si pin o approver se proporcionaron, los establecemos ahora
            if pin:
                instance.pin = pin
            if approver:
                instance.approver = approver

            # Guardamos la instancia actualizada
            instance.save()

            return instance