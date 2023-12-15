from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import WorkOrder
from .serializers import WorkOrderSerializer

class WorkOrderCreateView(generics.CreateAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Establecemos el solicitante automáticamente basándonos en el usuario autenticado
        serializer.save(applicant=self.request.user, is_active=False)