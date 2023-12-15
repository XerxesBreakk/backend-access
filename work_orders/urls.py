from django.urls import path
from .views import WorkOrderCreateView

urlpatterns = [
    path('crear_orden/', WorkOrderCreateView.as_view(), name='crear_orden'),
]