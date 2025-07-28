from django.db import models

class Company(models.Model):
    class StatusChoices(models.TextChoices):
        PRE_INCUBATEE = 'PRE', 'Pre-Incubatee'
        ASSOCIATE = 'ASC', 'Associate Incubatee'
        RESIDENT = 'RSD', 'Resident Incubatee'
        GRADUATED = 'GRD', 'Graduated'
        DROPPED = 'DRP', 'Dropped'

    name = models.CharField(max_length=200, unique=True)
    founders = models.CharField(max_length=500)
    contact_email = models.EmailField(unique=True)
    website = models.URLField(blank=True, null=True)
    sector = models.CharField(max_length=100)
    one_liner = models.TextField()
    status = models.CharField(max_length=3, choices=StatusChoices.choices, default=StatusChoices.PRE_INCUBATEE)
    date_joined = models.DateField(auto_now_add=True)
    # AI-driven field
    health_score = models.IntegerField(default=75, help_text="Calculated score 0-100")
    is_at_risk = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class KPI(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='kpis')
    date = models.DateField()
    mrr = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Monthly Recurring Revenue ($)")
    active_users = models.IntegerField(default=0)
    capital_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.company.name} - {self.date}"

class Mentor(models.Model):
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=200, help_text="Comma-separated values, e.g., Marketing, B2B Sales, Fundraising")
    email = models.EmailField(unique=True)
    assigned_companies = models.ManyToManyField(Company, blank=True)

    def __str__(self):
        return self.name

class InteractionLog(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interactions')
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True)
    interaction_type = models.CharField(max_length=50, choices=[('Meeting', 'Meeting'), ('Email', 'Email'), ('Workshop', 'Workshop')])
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()

    def __str__(self):
        return f"Interaction with {self.company.name} on {self.date.strftime('%Y-%m-%d')}"