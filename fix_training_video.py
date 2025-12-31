import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule

try:
    cpr = TrainingModule.objects.get(slug='cpr-basics')
    # NASA "How to CPR" (or similar safe content to test connectivity)
    # Actually using a very standard Tech intro video just to test connection.
    # If this fails, then LOCALHOST is fully blocked from YouTube.
    cpr.video_url = 'https://www.youtube.com/watch?v=jNQXAC9IVRw' # Me at the zoo (First YT video, no blocks)
    cpr.save()
    print("✅ Updated CPR video to 'Me at the zoo' (Ultimate connectivity test)")
except TrainingModule.DoesNotExist:
    print("❌ CP Module not found.")
