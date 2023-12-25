from django.urls import path
from .views import WorkOrderListCreateView, WorkOrderApprovalView

urlpatterns = [
    path('', WorkOrderListCreateView.as_view(), name='crear_listar_ot'),
    path('approve/<int:pk>/', WorkOrderApprovalView.as_view(), name='aprobar_orden'),
    
]