from django.core.management.base import BaseCommand
from core.models import Company, KPI
import pandas as pd

class Command(BaseCommand):
    help = 'Analyzes portfolio health and flags at-risk companies'

    def handle(self, *args, **options):
        companies = Company.objects.filter(status__in=['RSD', 'ASC'])
        self.stdout.write(self.style.SUCCESS('Starting portfolio analysis...'))

        for company in companies:
            kpis = company.kpis.order_by('date')
            if kpis.count() < 2:
                continue # Not enough data to analyze

            df = pd.DataFrame(list(kpis.values('date', 'mrr', 'active_users')))
            df = df.sort_values('date')

            # --- Simple Risk Logic ---
            # Rule 1: Is MRR declining or flat for the last 2 months?
            if df.iloc[-1]['mrr'] <= df.iloc[-2]['mrr']:
                company.is_at_risk = True
                self.stdout.write(self.style.WARNING(f'Flagged {company.name} as at-risk due to stalling MRR.'))
            else:
                company.is_at_risk = False

            company.save()
        self.stdout.write(self.style.SUCCESS('Analysis complete.'))