import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule

try:
    cpr = TrainingModule.objects.get(slug='cpr-basics')
    # Restore clean description
    cpr.description = 'Learn the fundamentals of Cardiopulmonary Resuscitation (CPR) and how to save a life during cardiac arrest.'
    cpr.save()
    print("✅ Restored Clean Description for CPR Module.")
except TrainingModule.DoesNotExist:
    print("❌ CP Module not found.")
