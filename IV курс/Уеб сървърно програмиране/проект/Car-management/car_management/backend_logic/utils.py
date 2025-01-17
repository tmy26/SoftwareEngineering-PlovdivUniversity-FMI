from .models import Maintenance
from datetime import timedelta

def get_monthly_requests_report(garage_id, start_date, end_date):
    """Generate the monthly report for a given garage within a date range"""
    maintenances = Maintenance.objects.filter(
        garage_id=garage_id,
        scheduledDate__gte=start_date,
        scheduledDate__lte=end_date
    )

    report = []
    for maintenance in maintenances:
        report.append({
            "scheduledDate": maintenance.scheduledDate,
            "serviceType": maintenance.serviceType,
            "car": maintenance.car.id,
            "garage": maintenance.garage.id,
        })

    return report
