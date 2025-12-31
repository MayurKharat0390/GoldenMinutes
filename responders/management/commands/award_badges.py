from django.core.management.base import BaseCommand
from responders.models import ResponderStats, Badge


class Command(BaseCommand):
    help = 'Award badges to all volunteers based on their current stats'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🎯 Starting badge award process...'))
        
        # Get all responder stats
        all_stats = ResponderStats.objects.all()
        total_volunteers = all_stats.count()
        
        self.stdout.write(f'Found {total_volunteers} volunteers')
        
        # Get all badges
        all_badges = Badge.objects.all()
        total_badges = all_badges.count()
        
        self.stdout.write(f'Found {total_badges} badges to check')
        self.stdout.write('-' * 60)
        
        total_awarded = 0
        
        # Check each volunteer
        for stats in all_stats:
            volunteer_name = stats.responder.username
            badges_awarded = 0
            
            # Check each badge
            for badge in all_badges:
                # Skip if already earned
                if badge.badge_id in stats.badges:
                    continue
                
                # Check if requirements are met
                if self.check_badge_requirement(stats, badge):
                    # Award the badge
                    stats.earn_badge(badge.badge_id, badge.points_reward)
                    badges_awarded += 1
                    total_awarded += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✅ {volunteer_name}: Earned "{badge.name}" (+{badge.points_reward} pts)'
                        )
                    )
            
            if badges_awarded == 0:
                self.stdout.write(f'  ⏭️  {volunteer_name}: No new badges')
        
        self.stdout.write('-' * 60)
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Complete! Awarded {total_awarded} badges to {total_volunteers} volunteers'
            )
        )
    
    def check_badge_requirement(self, stats, badge):
        """Check if a responder meets the requirements for a badge"""
        req_type = badge.requirement_type
        req_value = badge.requirement_value
        
        if req_type == 'total_responses':
            return stats.total_responses >= req_value
        
        elif req_type == 'lives_saved':
            return stats.lives_saved >= req_value
        
        elif req_type == 'response_time':
            return stats.average_response_time <= req_value
        
        elif req_type == 'streak':
            return stats.current_streak >= req_value
        
        elif req_type == 'rating':
            return stats.rating >= req_value
        
        elif req_type == 'completed_responses':
            return stats.completed_responses >= req_value
        
        elif req_type == 'level':
            return stats.level >= req_value
        
        elif req_type == 'points':
            return stats.total_points >= req_value
        
        return False
