from django.contrib import admin
from .models import Garage, Car, Maintenance

#add your models here

admin.site.register(Garage)
admin.site.register(Car)
admin.site.register(Maintenance)
