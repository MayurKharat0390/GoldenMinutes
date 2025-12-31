import os
import django
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncDate, ExtractHour

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from emergencies.models import Emergency, EmergencyResponse
from responders.models import ResponderStats, VolunteerProfile

print("=" * 60)
print("🔍 ANALYTICS DATA DIAGNOSTIC")
print("=" * 60)

# 1. Total Counts
print(f"Total Emergencies: {Emergency.objects.count()}")
print(f"Total Responses:   {EmergencyResponse.objects.count()}")

# 2. Trends Data
thirty_days_ago = timezone.now() - timedelta(days=30)
daily_stats = Emergency.objects.filter(
    triggered_at__gte=thirty_days_ago
).annotate(
    date=TruncDate('triggered_at')
).values('date').annotate(
    count=Count('emergency_id')
).order_by('date')

print("\n📅 DAILY TRENDS:")
dates = [stat['date'].strftime('%Y-%m-%d') for stat in daily_stats]
counts = [stat['count'] for stat in daily_stats]
print(f"Dates: {dates}")
print(f"Counts: {counts}")

if not dates:
    print("❌ NO TREND DATA FOUND (Last 30 days)")

# 3. Peak Hours
peak_stats = Emergency.objects.annotate(
    hour=ExtractHour('triggered_at')
).values('hour').annotate(
    count=Count('emergency_id')
).order_by('hour')

print("\n⏰ PEAK HOURS:")
for stat in peak_stats:
    print(f"  Hour {stat['hour']}: {stat['count']}")

if not peak_stats:
    print("❌ NO HOURLY DATA FOUND")

# 4. Funnel
funnel_triggered = Emergency.objects.count()
funnel_accepted = EmergencyResponse.objects.filter(status='accepted').count()
funnel_arrived = EmergencyResponse.objects.filter(status='arrived').count()
funnel_resolved = Emergency.objects.filter(status='resolved').count()
print("\n📉 FUNNEL:")
print(f"  Triggered: {funnel_triggered}")
print(f"  Accepted:  {funnel_accepted}")
print(f"  Arrived:   {funnel_arrived}")
print(f"  Resolved:  {funnel_resolved}")

print("\n" + "=" * 60)
