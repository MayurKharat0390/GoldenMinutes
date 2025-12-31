import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from responders.models import Badge

# Clear existing badges
Badge.objects.all().delete()

badges_data = [
    # Milestone Badges
    {
        'badge_id': 'first_response',
        'name': 'First Responder',
        'description': 'Responded to your first emergency',
        'icon_class': 'bi-award-fill',
        'badge_type': 'milestone',
        'requirement_type': 'total_responses',
        'requirement_value': 1,
        'points_reward': 50,
        'color': '#10b981',
        'rarity': 'common'
    },
    {
        'badge_id': 'ten_responses',
        'name': 'Dedicated Helper',
        'description': 'Responded to 10 emergencies',
        'icon_class': 'bi-star-fill',
        'badge_type': 'milestone',
        'requirement_type': 'total_responses',
        'requirement_value': 10,
        'points_reward': 100,
        'color': '#3b82f6',
        'rarity': 'common'
    },
    {
        'badge_id': 'fifty_responses',
        'name': 'Community Guardian',
        'description': 'Responded to 50 emergencies',
        'icon_class': 'bi-shield-fill-check',
        'badge_type': 'milestone',
        'requirement_type': 'total_responses',
        'requirement_value': 50,
        'points_reward': 500,
        'color': '#8b5cf6',
        'rarity': 'rare'
    },
    {
        'badge_id': 'century_club',
        'name': 'Century Club',
        'description': 'Responded to 100 emergencies',
        'icon_class': 'bi-trophy-fill',
        'badge_type': 'milestone',
        'requirement_type': 'total_responses',
        'requirement_value': 100,
        'points_reward': 1000,
        'color': '#FFD700',
        'rarity': 'epic'
    },
    
    # Performance Badges
    {
        'badge_id': 'speed_demon',
        'name': 'Speed Demon',
        'description': 'Average response time under 3 minutes',
        'icon_class': 'bi-lightning-fill',
        'badge_type': 'performance',
        'requirement_type': 'avg_response_time',
        'requirement_value': 3.0,
        'points_reward': 200,
        'color': '#f59e0b',
        'rarity': 'rare'
    },
    {
        'badge_id': 'flash',
        'name': 'The Flash',
        'description': 'Fastest response under 1 minute',
        'icon_class': 'bi-lightning-charge-fill',
        'badge_type': 'performance',
        'requirement_type': 'fastest_response',
        'requirement_value': 1.0,
        'points_reward': 300,
        'color': '#ef4444',
        'rarity': 'epic'
    },
    {
        'badge_id': 'perfect_score',
        'name': 'Perfect Score',
        'description': 'Maintain 5.0 rating with 10+ ratings',
        'icon_class': 'bi-star-fill',
        'badge_type': 'performance',
        'requirement_type': 'rating',
        'requirement_value': 5.0,
        'points_reward': 250,
        'color': '#FFD700',
        'rarity': 'rare'
    },
    
    # Special Badges
    {
        'badge_id': 'night_owl',
        'name': 'Night Owl',
        'description': 'Responded to 10 emergencies between 10 PM - 6 AM',
        'icon_class': 'bi-moon-stars-fill',
        'badge_type': 'special',
        'requirement_type': 'night_responses',
        'requirement_value': 10,
        'points_reward': 150,
        'color': '#6366f1',
        'rarity': 'rare'
    },
    {
        'badge_id': 'early_bird',
        'name': 'Early Bird',
        'description': 'Responded to 10 emergencies between 5 AM - 8 AM',
        'icon_class': 'bi-sunrise-fill',
        'badge_type': 'special',
        'requirement_type': 'morning_responses',
        'requirement_value': 10,
        'points_reward': 150,
        'color': '#f97316',
        'rarity': 'rare'
    },
    {
        'badge_id': 'life_saver',
        'name': 'Life Saver',
        'description': 'Confirmed to have saved 10 lives',
        'icon_class': 'bi-heart-fill',
        'badge_type': 'special',
        'requirement_type': 'lives_saved',
        'requirement_value': 10,
        'points_reward': 1000,
        'color': '#ef4444',
        'rarity': 'legendary'
    },
    {
        'badge_id': 'streak_master',
        'name': 'Streak Master',
        'description': 'Active for 30 consecutive days',
        'icon_class': 'bi-fire',
        'badge_type': 'special',
        'requirement_type': 'current_streak',
        'requirement_value': 30,
        'points_reward': 500,
        'color': '#f59e0b',
        'rarity': 'epic'
    },
    
    # Training Badges
    {
        'badge_id': 'cpr_certified',
        'name': 'CPR Certified',
        'description': 'Completed CPR training module',
        'icon_class': 'bi-heart-pulse-fill',
        'badge_type': 'training',
        'requirement_type': 'training_cpr',
        'requirement_value': 1,
        'points_reward': 100,
        'color': '#ef4444',
        'rarity': 'common'
    },
    {
        'badge_id': 'first_aid_expert',
        'name': 'First Aid Expert',
        'description': 'Completed all first-aid training modules',
        'icon_class': 'bi-bandaid-fill',
        'badge_type': 'training',
        'requirement_type': 'training_all',
        'requirement_value': 1,
        'points_reward': 300,
        'color': '#10b981',
        'rarity': 'rare'
    },
]

for badge_data in badges_data:
    Badge.objects.create(**badge_data)

print(f"✓ Created {len(badges_data)} badges")
print("\nBadge Categories:")
print(f"  - Milestone: 4 badges")
print(f"  - Performance: 3 badges")
print(f"  - Special: 4 badges")
print(f"  - Training: 2 badges")
print(f"\nTotal: {len(badges_data)} badges")
