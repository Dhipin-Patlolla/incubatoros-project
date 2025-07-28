from django.contrib import admin
from .models import Company, KPI, Mentor, InteractionLog

admin.site.register(Company)
admin.site.register(KPI)
admin.site.register(Mentor)
admin.site.register(InteractionLog)