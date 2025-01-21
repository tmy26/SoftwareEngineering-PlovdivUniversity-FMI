from django.db import models

# Create your models here.
class Garage(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    city = models.CharField(max_length=255, db_index=True)
    location = models.CharField(max_length=255, db_index=True)
    capacity = models.IntegerField()

    class Meta:
        db_table = "garages"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["city"]),
            models.Index(fields=["location"]),
        ]

class Car(models.Model):
    make = models.CharField(max_length=255, db_index=True)
    model = models.CharField(max_length=255, db_index=True)
    production_year = models.IntegerField(db_index=True)
    license_plate = models.CharField(max_length=255, db_index=True)
    garages = models.ManyToManyField(
        Garage, related_name="cars", blank=True
    )

    class Meta:
        db_table = "cars"
        indexes = [
            models.Index(fields=["make"]),
            models.Index(fields=["model"]),
            models.Index(fields=["production_year"]),
            models.Index(fields=["license_plate"]),
        ]

class Maintenance(models.Model):
    scheduled_date = models.DateField(db_index=True)
    service_type = models.CharField(max_length=255, db_index=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="maintenances")
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name="maintenances")

    class Meta:
        db_table = "maintenances"
        indexes = [
            models.Index(fields=["scheduled_date"]),
            models.Index(fields=["service_type"]),
        ]
