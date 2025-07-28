from celery import shared_task
from django.utils import timezone
from .models import Company

@shared_task
def send_kpi_reminders():
    # Find companies that haven't submitted KPIs this month
    today = timezone.now().date()
    companies_to_remind = Company.objects.filter(status__in=['RSD', 'ASC'])
    for company in companies_to_remind:
        latest_kpi = company.kpis.order_by('-date').first()
        if not latest_kpi or latest_kpi.date.month != today.month:
            # Logic to send an actual email would go here
            print(f"REMINDER: Sent email to {company.name} to submit KPIs for this month.")
    return "KPI reminder task complete."