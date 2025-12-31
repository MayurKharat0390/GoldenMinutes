from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class ResponderStats(models.Model):
    """
    Track volunteer/responder performance metrics
    """
    responder = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stats'
    )
    
    # Response Metrics
    total_responses = models.IntegerField(default=0, help_text="Total emergencies accepted")
    completed_responses = models.IntegerField(default=0, help_text="Successfully completed emergencies")
    lives_saved = models.IntegerField(default=0, help_text="Confirmed lives saved")
    
    # Time Metrics
    average_response_time = models.FloatField(default=0.0, help_text="Average time to accept (minutes)")
    average_arrival_time = models.FloatField(default=0.0, help_text="Average time to arrive (minutes)")
    fastest_response = models.FloatField(null=True, blank=True, help_text="Fastest response time (minutes)")
    
    # Rating & Feedback
    rating = models.FloatField(default=5.0, help_text="Average rating from victims")
    total_ratings = models.IntegerField(default=0)
    
    # Streak & Activity
    current_streak = models.IntegerField(default=0, help_text="Consecutive days active")
    longest_streak = models.IntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)
    
    # Points & Gamification
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    badges = models.JSONField(default=list, help_text="List of earned badge IDs")
    
    # Availability
    is_available = models.BooleanField(default=True, help_text="Currently available for emergencies")
    availability_radius_km = models.FloatField(default=5.0, help_text="Willing to travel distance")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_stats(self):
        """Recalculate all statistics"""
        from emergencies.models import Emergency, EmergencyResponse
        
        # Get all responses
        responses = EmergencyResponse.objects.filter(responder=self.responder)
        self.total_responses = responses.count()
        
        # Completed emergencies
        completed = Emergency.objects.filter(
            primary_responder=self.responder,
            status='resolved'
        )
        self.completed_responses = completed.count()
        
        # Calculate average response time
        accepted_responses = responses.filter(status='accepted')
        if accepted_responses.exists():
            times = []
            for resp in accepted_responses:
                if resp.responded_at and resp.notified_at:
                    delta = (resp.responded_at - resp.notified_at).total_seconds() / 60
                    times.append(delta)
            
            if times:
                self.average_response_time = sum(times) / len(times)
                self.fastest_response = min(times)
        
        # Update streak
        self.update_streak()
        
        # Calculate level based on points
        self.level = (self.total_points // 100) + 1
        
        self.save()
    
    def update_streak(self):
        """Update activity streak"""
        if self.last_active:
            days_since = (timezone.now() - self.last_active).days
            if days_since == 1:
                self.current_streak += 1
                if self.current_streak > self.longest_streak:
                    self.longest_streak = self.current_streak
            elif days_since > 1:
                self.current_streak = 0
        
        self.last_active = timezone.now()
    
    def add_points(self, points, reason=""):
        """Add points and check for level up"""
        old_level = self.level
        self.total_points += points
        self.level = (self.total_points // 100) + 1
        
        if self.level > old_level:
            # Level up! Could trigger notification
            pass
        
        self.save()
    
    def earn_badge(self, badge_id):
        """Award a badge to the responder"""
        if badge_id not in self.badges:
            self.badges.append(badge_id)
            self.save()
            return True
        return False
    
    def __str__(self):
        return f"{self.responder.username} - Stats (Level {self.level})"
    
    class Meta:
        verbose_name_plural = "Responder Statistics"


class Badge(models.Model):
    """
    Achievement badges for gamification
    """
    BADGE_TYPES = [
        ('milestone', 'Milestone'),
        ('performance', 'Performance'),
        ('special', 'Special Event'),
        ('training', 'Training'),
    ]
    
    badge_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Bootstrap icon class")
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    
    # Requirements
    requirement_type = models.CharField(max_length=50, help_text="e.g., 'total_responses', 'avg_response_time'")
    requirement_value = models.FloatField(help_text="Threshold to earn badge")
    
    # Rewards
    points_reward = models.IntegerField(default=0)
    
    # Display
    color = models.CharField(max_length=7, default="#FFD700", help_text="Hex color code")
    rarity = models.CharField(max_length=20, default="common", 
                             choices=[('common', 'Common'), ('rare', 'Rare'), 
                                     ('epic', 'Epic'), ('legendary', 'Legendary')])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.badge_type})"
    
    class Meta:
        ordering = ['badge_type', 'requirement_value']
