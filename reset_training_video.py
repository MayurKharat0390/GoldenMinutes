import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule

try:
    cpr = TrainingModule.objects.get(slug='cpr-basics')
    # Use reliable Google sample for now to ensure NO ERRORS.
    # The Admin can now upload a real 'cpr.mp4' file via the Admin Panel.
    cpr.video_url = ''
    cpr.video_file = None # Clear file if any
    cpr.description = "⚠️ DEMO VIDEO: Please upload a real CPR video file in the Admin Admin > Training Modules.\n\n" + cpr.description
    cpr.save()
    print("✅ Reset video to safe demo. Admin upload for real video enabled.")
except TrainingModule.DoesNotExist:
    print("❌ CP Module not found.")
