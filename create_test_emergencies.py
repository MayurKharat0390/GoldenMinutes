import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from emergencies.models import Emergency
from accounts.models import User

# Get a user
user = User.objects.first()

# Create different emergency types for testing
emergency_types = [
    ('medical', 'Medical Emergency - CPR'),
    ('accident', 'Accident - Bleeding Control'),
    ('fire', 'Fire - Burns Treatment'),
    ('disaster', 'Disaster - Earthquake/Flood')
]

print("Creating test emergencies...\n")

for etype, description in emergency_types:
    emergency = Emergency.objects.create(
        victim=user,
        emergency_type=etype,
        description=description,
        latitude=20.039601,
        longitude=74.015261
    )
    emergency.calculate_severity()
    emergency.activate_bystander_mode()
    
    print(f"✓ {description}")
    print(f"  URL: http://localhost:8000/emergencies/{emergency.emergency_id}/bystander/\n")

print("All test emergencies created! Visit the URLs above to see different instruction sets.")
