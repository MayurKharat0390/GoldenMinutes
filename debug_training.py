import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule

try:
    cpr = TrainingModule.objects.get(slug='cpr-basics')
    print("--- DEBUG INFO ---")
    print(f"Title: {cpr.title}")
    print(f"Video URL: '{cpr.video_url}'")
    print(f"Video File: '{cpr.video_file}'")
    print("------------------")
except TrainingModule.DoesNotExist:
    print("❌ CP Module not found.")
