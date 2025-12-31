from django.db.models.signals import post_save
from django.dispatch import receiver
from emergencies.models import EmergencyResponse
from .models import ResponderStats, Badge


@receiver(post_save, sender=EmergencyResponse)
def check_and_award_badges(sender, instance, created, **kwargs):
    """
    Automatically check and award badges when emergency response is saved
    """
    if not instance.responder:
        return
    
    # Get or create responder stats
    stats, _ = ResponderStats.objects.get_or_create(responder=instance.responder)
    
    # Update stats first
    stats.update_stats()
    
    # Get all badges
    all_badges = Badge.objects.all()
    
    # Check each badge requirement
    for badge in all_badges:
        # Skip if already earned
        if badge.badge_id in stats.badges:
            continue
        
        # Check if requirements are met
        if check_badge_requirement(stats, badge):
            # Award the badge
            stats.earn_badge(badge.badge_id, badge.points_reward)
            
            # TODO: Send notification to user
            print(f"🎉 Badge earned: {badge.name} by {instance.responder.username}")


def check_badge_requirement(stats, badge):
    """
    Check if a responder meets the requirements for a badge
    """
    req_type = badge.requirement_type
    req_value = badge.requirement_value
    
    if req_type == 'total_responses':
        return stats.total_responses >= req_value
    
    elif req_type == 'lives_saved':
        return stats.lives_saved >= req_value
    
    elif req_type == 'response_time':
        # Average response time should be less than or equal to requirement
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
