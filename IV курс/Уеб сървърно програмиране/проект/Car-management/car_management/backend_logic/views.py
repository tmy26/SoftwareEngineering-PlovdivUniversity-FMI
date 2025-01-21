from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Maintenance, Garage
from .serializers import *
from .utils import get_monthly_requests_report 

@api_view(["GET"])
def read_cars(request):
    cars = Car.objects.prefetch_related("garages").all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def create_car(request):
    serializer = CarCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        car = serializer.save()
        return Response(CarSerializer(car).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def delete_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Car.DoesNotExist:
        return Response({"detail": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
def update_car(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return Response({"detail": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CarCreateUpdateSerializer(car, data=request.data, partial=True)
    if serializer.is_valid():
        car = serializer.save()
        return Response(CarSerializer(car).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def read_garages(request):
    """Get a list of all garages"""
    garages = Garage.objects.all()
    serializer = GarageSerializer(garages, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def create_garage(request):
    """Create a new garage"""
    serializer = GarageCreateSerializer(data=request.data)
    if serializer.is_valid():
        garage = serializer.save()
        return Response(GarageSerializer(garage).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def delete_garage(request, garage_id):
    """Delete a garage"""
    try:
        garage = Garage.objects.get(id=garage_id)
        garage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Garage.DoesNotExist:
        return Response({"detail": "Garage not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
def update_garage(request, garage_id):
    """Update an existing garage"""
    try:
        garage = Garage.objects.get(id=garage_id)
    except Garage.DoesNotExist:
        return Response({"detail": "Garage not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = GarageUpdateSerializer(garage, data=request.data, partial=True)
    if serializer.is_valid():
        garage = serializer.save()
        return Response(GarageSerializer(garage).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def read_maintenance(request):
    """Get all maintenance records"""
    maintenances = Maintenance.objects.all()
    serializer = MaintenanceSerializer(maintenances, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def monthly_requests_report(request, garage_id):
    """Get monthly maintenance report"""
    start_month = request.query_params.get("startMonth")
    end_month = request.query_params.get("endMonth")
    
    try:
        start_date = datetime.strptime(start_month, "%Y-%m")
        end_date = datetime.strptime(end_month, "%Y-%m")
    except ValueError:
        return Response(
            {"detail": "Invalid date format. Use YYYY-MM format."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if start_date > end_date:
        return Response(
            {"detail": "Start month cannot be after end month."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    report = get_monthly_requests_report(garage_id, start_date, end_date)
    return Response(report)

@api_view(["POST"])
def create_maintenance(request):
    """Create a new maintenance record"""
    serializer = MaintenanceCreateSerializer(data=request.data)
    if serializer.is_valid():
        maintenance = serializer.save()
        return Response(MaintenanceSerializer(maintenance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def delete_maintenance(request, maintenance_id):
    """Delete a maintenance record"""
    try:
        maintenance = Maintenance.objects.get(id=maintenance_id)
        maintenance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Maintenance.DoesNotExist:
        return Response({"detail": "Maintenance not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
def update_maintenance(request, maintenance_id):
    """Update an existing maintenance record"""
    try:
        maintenance = Maintenance.objects.get(id=maintenance_id)
    except Maintenance.DoesNotExist:
        return Response({"detail": "Maintenance not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MaintenanceUpdateSerializer(maintenance, data=request.data, partial=True)
    if serializer.is_valid():
        updated_maintenance = serializer.save()
        return Response(MaintenanceSerializer(updated_maintenance).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
