import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from responders.models import ResponderStats
from accounts.models import User

# Get all volunteers
volunteers = User.objects.filter(role='volunteer')

if not volunteers.exists():
    print("⚠️  No volunteers found. Create a volunteer account first.")
    print("Run: python manage.py createsuperuser")
    print("Then change role to 'volunteer' in admin panel")
else:
    for volunteer in volunteers:
        # Get or create stats
        stats, created = ResponderStats.objects.get_or_create(responder=volunteer)
        
        if created:
            # Add some demo data
            stats.total_responses = 15
            stats.completed_responses = 12
            stats.lives_saved = 3
            stats.average_response_time = 4.2
            stats.rating = 4.7
            stats.current_streak = 5
            stats.longest_streak = 12
            stats.total_points = 450
            
            # Earn some badges
            stats.earn_badge('first_response')
            stats.earn_badge('ten_responses')
            
            stats.save()
            print(f"✓ Created stats for {volunteer.username}")
        else:
            # Update existing stats
            stats.update_stats()
            print(f"✓ Updated stats for {volunteer.username}")
        
        print(f"  Level: {stats.level}")
        print(f"  Points: {stats.total_points}")
        print(f"  Badges: {len(stats.badges)}")
        print()

print("✓ Test data populated!")
print(f"\nAccess dashboard at:")
print(f"http://localhost:8000/responders/dashboard/enhanced/")
