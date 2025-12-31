import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule

try:
    cpr = TrainingModule.objects.get(slug='cpr-basics')
    print(f"OLD URL: '{cpr.video_url}'")
    
    # FORCE UPDATE
    cpr.video_url = 'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4'
    cpr.save()
    
    # Re-fetch to confirm
    cpr.refresh_from_db()
    print(f"NEW URL: '{cpr.video_url}'")
    
    if cpr.video_url:
        print("✅ SUCCESS: Database updated.")
    else:
        print("❌ FAILURE: Database did not persist change.")

except TrainingModule.DoesNotExist:
    print("❌ CP Module not found.")
