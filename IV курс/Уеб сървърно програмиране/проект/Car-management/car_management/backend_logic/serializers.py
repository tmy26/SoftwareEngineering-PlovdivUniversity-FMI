from rest_framework import serializers
from .models import Garage, Car, Maintenance

class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
    garage_ids = serializers.PrimaryKeyRelatedField(
        source="garages", queryset=Garage.objects.all(), many=True
    )

    class Meta:
        model = Car
        fields = ["id", "make", "model", "production_year", "license_plate", "garage_ids"]

class CarCreateUpdateSerializer(serializers.ModelSerializer):
    garage_ids = serializers.PrimaryKeyRelatedField(
        source="garages", queryset=Garage.objects.all(), many=True, required=False
    )

    class Meta:
        model = Car
        fields = ["make", "model", "production_year", "license_plate", "garage_ids"]

class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = "__all__"

class GarageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = ["name", "city", "location", "capacity"]

class GarageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = ["name", "city", "location", "capacity"]
class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"


class MaintenanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ["scheduledDate", "serviceType", "car", "garage"]

class MaintenanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ["scheduledDate", "serviceType", "car", "garage"]
