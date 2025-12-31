import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from django.contrib.auth import get_user_model
from emergencies.models import Emergency, EmergencyResponse
from responders.models import ResponderStats, Badge
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()

print("=" * 60)
print("TESTING AUTO-AWARD BADGES SYSTEM")
print("=" * 60)

# Get a volunteer
volunteer = User.objects.filter(role='volunteer').first()
if not volunteer:
    print("❌ No volunteers found!")
    exit()

print(f"\n📍 Testing with volunteer: {volunteer.username}")

# Get their stats
stats, created = ResponderStats.objects.get_or_create(responder=volunteer)
print(f"Current stats:")
print(f"  - Total Responses: {stats.total_responses}")
print(f"  - Lives Saved: {stats.lives_saved}")
print(f"  - Badges: {len(stats.badges)}")
print(f"  - Points: {stats.total_points}")

# Remove a badge to test re-awarding
if 'ten_responses' in stats.badges:
    stats.badges.remove('ten_responses')
    stats.save()
    print(f"\n🔄 Removed 'ten_responses' badge for testing")

# Create a test emergency
print(f"\n📝 Creating test emergency...")
emergency = Emergency.objects.create(
    victim=volunteer,
    emergency_type='medical',
    severity='high',
    latitude=18.5204,
    longitude=73.8567,
    location_address='Test Location',
    status='active'
)
print(f"✅ Emergency created: {emergency.emergency_id}")

# Create multiple emergency responses to meet requirements
print(f"\n🚨 Creating 10 emergency responses to meet badge requirements...")
for i in range(10):
    # Create a new emergency for each response
    em = Emergency.objects.create(
        victim=volunteer,
        emergency_type='medical',
        severity='high',
        latitude=18.5204,
        longitude=73.8567,
        location_address=f'Test Location {i}',
        status='active'
    )
    
    response = EmergencyResponse.objects.create(
        emergency=em,
        responder=volunteer,
        status='accepted',
        responded_at=timezone.now(),
        notified_at=timezone.now() - timedelta(seconds=180)
    )
print(f"✅ Created 10 responses")

# Check if badge was awarded
stats.refresh_from_db()
print(f"\n📊 After response:")
print(f"  - Total Responses: {stats.total_responses}")
print(f"  - Badges: {len(stats.badges)}")
print(f"  - Points: {stats.total_points}")

# Check specific badges
badges_to_check = ['first_response', 'ten_responses', 'fifty_responses']
print(f"\n🏆 Badge Status:")
for badge_id in badges_to_check:
    has_badge = badge_id in stats.badges
    status = "✅" if has_badge else "❌"
    print(f"  {status} {badge_id}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nIf you see new badges awarded above, the system is working!")
print("Check the console for '🎉 Badge earned' messages")
