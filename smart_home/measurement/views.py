from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        sensor = Sensor.objects.get(pk=pk)

        serializer = SensorSerializer(sensor, data=request.data, partial=True)  # Используем partial=True для PATCH
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        sensors = Sensor.objects.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        sensor = Sensor.objects.get(pk=pk)
        serializer = SensorDetailSerializer(sensor)
        return Response(serializer.data)


class MeasurementViewSet(viewsets.ViewSet):

    def create(self, request):
        # Убедимся, что в запросе указываем 'sensor' как 'sensor_id'
        sensor_id = request.data.get('sensor')  # Получаем ID датчика из запроса

        # Проверяем, существует ли датчик
        if not Sensor.objects.filter(pk=sensor_id).exists():
            return Response({'error': 'Sensor not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Создаем новое измерение
        temperature = request.data.get('temperature')
        measurement = Measurement(sensor_id=sensor_id, temperature=temperature)

        # Сохраняем измерение
        measurement.save()
        return Response({'status': 'Measurement added'}, status=status.HTTP_201_CREATED)
