from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Garage
from .serializers import GarageSerializer

def get_garages():
    """Retrieve all garages from the database."""
    garages = Garage.objects.all()
    return GarageSerializer(garages, many=True).data

def create_garage(garage_data):
    """Create a new garage and save it to the database."""
    serializer = GarageSerializer(data=garage_data)
    if serializer.is_valid():
        garage = serializer.save()
        return serializer.data
    return {"error": serializer.errors}

def delete_garage(garage_id):
    """Delete a garage by its ID."""
    try:
        garage = get_object_or_404(Garage, id=garage_id)
        garage.delete()
        return {"message": "Garage deleted successfully"}
    except ObjectDoesNotExist:
        return {"error": "Garage not found"}
    except Exception as e:
        return {"error": f"Failed to delete garage: {e}"}

def update_garage(garage_id, garage_data):
    """Update an existing garage by its ID."""
    try:
        garage = get_object_or_404(Garage, id=garage_id)
        serializer = GarageSerializer(garage, data=garage_data, partial=True)
        if serializer.is_valid():
            garage = serializer.save()
            return serializer.data
        return {"error": serializer.errors}
    except ObjectDoesNotExist:
        return {"error": "Garage not found"}
    except Exception as e:
        return {"error": f"Failed to update garage: {e}"}
