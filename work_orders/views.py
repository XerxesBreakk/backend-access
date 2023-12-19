import random
from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import WorkOrder
from .serializers import WorkOrderSerializer, WorkOrderApproveSerializer

class WorkOrderCreateView(generics.CreateAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Establecemos el solicitante automáticamente basándonos en el usuario autenticado
        serializer.save(applicant=self.request.user, is_active=False)
        
        
class WorkOrderListView(generics.ListAPIView):
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Obtener el usuario autenticado
        user = self.request.user

        # Si el usuario es un administrador, mostrar todas las órdenes de trabajo
        if user.is_staff:
            return WorkOrder.objects.all()
        
        # Si el usuario no es un administrador, mostrar solo sus órdenes de trabajo
        return WorkOrder.objects.filter(applicant=user)
    
class WorkOrderApproveView(generics.ListCreateAPIView):
    serializer_class = WorkOrderApproveSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Filter the queryset to include only work orders with a future date
        return WorkOrder.objects.filter(date__gt=datetime.now())

    def perform_create(self, serializer):
        # Generate a 5-digit random number for the pin
        pin = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        
        # Update the serializer data with the generated pin and the user approving the order
        serializer.validated_data['pin'] = pin
        serializer.validated_data['approver'] = self.request.user
        
        # Perform the update
        serializer.save()