from django.urls import path
from .views import WorkOrderCreateView, WorkOrderListView, WorkOrderApproveView

urlpatterns = [
    path('', WorkOrderListView.as_view(), name='crear_orden'),
    path('create/', WorkOrderCreateView.as_view(), name='crear_orden'),
    path('approve/', WorkOrderApproveView.as_view(), name='aprobar_orden'),
    
]