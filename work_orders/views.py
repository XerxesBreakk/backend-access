import random
from datetime import datetime
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import WorkOrder
from .serializers import WorkOrderSerializer, WorkOrderApprovalSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import UserAccount

class WorkOrderListCreateView(ListCreateAPIView):
    serializer_class=WorkOrderSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        is_active_param = self.request.query_params.get('is_active', None)
        if is_active_param is not None:
            # Convierte el valor de 'is_active' a un booleano
            is_active_param = is_active_param.lower() == 'true'
            if user.is_staff:
                return WorkOrder.objects.all().filter(is_active=is_active_param)
            
        if user.is_staff:
            return WorkOrder.objects.all()
        
        return WorkOrder.objects.filter(applicant=user)
    
    def perform_create(self, serializer):
        # Establecemos el solicitante automáticamente basándonos en el usuario autenticado
        serializer.save(applicant=self.request.user, is_active=False)

    
class WorkOrderApprovalView(UpdateAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderApprovalSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Validate and update the serializer data (even though there are no fields)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if the user is an administrator
        if not request.user.is_staff:
            return Response(
                {'detail': 'No tienes permisos para aprobar ordenes de trabajo.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Set is_active to True, set approver to the authenticated user, and generate a random 5-digit PIN
        instance.is_active = True
        instance.approver = request.user
        instance.pin = str(random.randint(10000, 99999))
        instance.save()
        
        # Send emails to the applicant and administrators
        self.send_approval_emails(instance)

        return Response({'detail': 'WorkOrder approved successfully.'})
    
    
    def send_approval_emails(self, work_order):
        # Send email to the applicant
        subject_applicant = 'Orden de trabajo aprobada'
        message_applicant = f'Tu orden de trabajo (ID: {work_order.id}) ha sido aprobada para la fecha {work_order.date} y la compañia {work_order.company}.'
        send_mail(subject_applicant, message_applicant, settings.DEFAULT_FROM_EMAIL, [work_order.applicant.email])

        # Send email to administrators
        subject_admin = 'Nueva orden de trabajo aprobada'
        message_admin = f'Se aprobo una orden de trabajo (ID: {work_order.id}).\n\nDETALLES:\n{work_order}'
        admin_emails = UserAccount.objects.filter(is_staff=True).values_list('email', flat=True)
        send_mail(subject_admin, message_admin, settings.DEFAULT_FROM_EMAIL, admin_emails)