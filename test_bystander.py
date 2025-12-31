import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from emergencies.models import Emergency

# Get the most recent emergency
emergency = Emergency.objects.order_by('-triggered_at').first()

if emergency:
    print(f"Emergency ID: {emergency.emergency_id}")
    print(f"Type: {emergency.get_emergency_type_display()}")
    print(f"Status: {emergency.get_status_display()}")
    print(f"Bystander Mode: {'Active' if emergency.bystander_mode_active else 'Inactive'}")
    
    # Activate bystander mode if not already active
    if not emergency.bystander_mode_active:
        emergency.activate_bystander_mode()
        print("\n✓ Bystander mode activated!")
    
    print(f"\nAccess URL: http://localhost:8000/emergencies/{emergency.emergency_id}/bystander/")
else:
    print("No emergencies found. Create one first!")
