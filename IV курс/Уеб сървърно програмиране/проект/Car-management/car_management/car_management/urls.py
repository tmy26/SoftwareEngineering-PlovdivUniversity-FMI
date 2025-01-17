"""
URL configuration for car_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend_logic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("cars/", views.read_cars, name="read_cars"),
    path("cars/", views.create_car, name="create_car"),
    path("cars/<int:car_id>/", views.delete_car, name="delete_car"),
    path("cars/<int:car_id>/", views.update_car, name="update_car"),
    path('garages/', views.read_garages, name='read_garages'),
    path('garages/', views.create_garage, name='create_garage'),
    path('garages/<int:garage_id>/', views.delete_garage, name='delete_garage'),
    path('garages/<int:garage_id>/', views.update_garage, name='update_garage'),
    path('maintenance/', views.read_maintenance, name='read_maintenance'),
    path('maintenance/create/', views.create_maintenance, name='create_maintenance'),
    path('maintenance/<int:maintenance_id>/delete/', views.delete_maintenance, name='delete_maintenance'),
    path('maintenance/<int:maintenance_id>/update/', views.update_maintenance, name='update_maintenance'),
    path('maintenance/monthlyRequestsReport/<int:garage_id>/', views.monthly_requests_report, name='monthly_requests_report'),
]
