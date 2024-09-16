from django.urls import path
from .views import SensorViewSet, MeasurementViewSet

sensor_list = SensorViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

sensor_detail = SensorViewSet.as_view({
    'get': 'retrieve',
    'patch': 'update'
})

measurement_create = MeasurementViewSet.as_view({
    'post': 'create'
})

urlpatterns = [
    path('sensors/', sensor_list, name='sensor-list'),
    path('sensors/<int:pk>/', sensor_detail, name='sensor-detail'),
    path('measurements/', measurement_create, name='measurement-create'),
]

