"""
Create demo emergencies for testing
Run with: python manage.py shell < create_demo_emergencies.py
"""
from django.contrib.auth import get_user_model
from emergencies.models import Emergency, EmergencyTimeline
from decimal import Decimal
from django.utils import timezone

User = get_user_model()

# Get a citizen user
try:
    citizen = User.objects.filter(role='citizen').first()
    if not citizen:
        print("No citizen users found. Please run populate_demo_data first.")
        exit()
    
    # Create some demo emergencies
    emergencies_data = [
        {
            'emergency_type': 'medical',
            'latitude': Decimal('19.0760'),
            'longitude': Decimal('72.8777'),
            'description': 'Person collapsed on street, needs immediate help'
        },
        {
            'emergency_type': 'accident',
            'latitude': Decimal('19.1136'),
            'longitude': Decimal('72.8697'),
            'description': 'Car accident at intersection'
        },
        {
            'emergency_type': 'fire',
            'latitude': Decimal('19.0596'),
            'longitude': Decimal('72.8295'),
            'description': 'Small fire in building'
        },
    ]
    
    for data in emergencies_data:
        emergency = Emergency.objects.create(
            victim=citizen,
            emergency_type=data['emergency_type'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            description=data['description'],
            status='active'
        )
        
        # Calculate severity
        emergency.calculate_severity()
        
        # Create timeline entry
        EmergencyTimeline.objects.create(
            emergency=emergency,
            event_type='sos_triggered',
            description=f'SOS triggered by {citizen.username}',
            actor=citizen
        )
        
        print(f"Created {emergency.get_emergency_type_display()} emergency at {emergency.latitude}, {emergency.longitude}")
    
    print(f"\nSuccessfully created {len(emergencies_data)} demo emergencies!")
    print("Visit http://127.0.0.1:8000/emergencies/map/ to see them on the map")

except Exception as e:
    print(f"Error: {e}")
