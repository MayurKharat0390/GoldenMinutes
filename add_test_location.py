"""
Quick script to add test location data for responders
This enables the ETA feature to work
"""

from emergencies.models import ResponderLocation, Emergency
from accounts.models import User

# Get the emergency
emergency = Emergency.objects.get(emergency_id='8334ad70-c347-43e0-b48a-a73c80f990ce')

print(f"Emergency: {emergency}")
print(f"Victim: {emergency.victim}")
print(f"Primary Responder: {emergency.primary_responder}")
print(f"Status: {emergency.status}")

if emergency.primary_responder:
    # Add/Update responder location
    # Let's place them 2km away from the emergency
    responder_lat = float(emergency.latitude) + 0.018  # ~2km north
    responder_lng = float(emergency.longitude)
    
    location, created = ResponderLocation.objects.update_or_create(
        responder=emergency.primary_responder,
        defaults={
            'latitude': responder_lat,
            'longitude': responder_lng,
            'accuracy': 10.0
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"\n✓ {action} location for {emergency.primary_responder.username}")
    print(f"  Location: {responder_lat}, {responder_lng}")
    print(f"  Emergency at: {emergency.latitude}, {emergency.longitude}")
    print(f"\n🎯 Now refresh the emergency detail page to see the ETA!")
else:
    print("\n⚠️  No primary responder assigned yet!")
    print("Assign a responder first, then run this script again.")
