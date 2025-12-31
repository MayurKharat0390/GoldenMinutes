from django.db import models
from django.conf import settings


class VolunteerProfile(models.Model):
    """
    Extended profile for volunteers/responders
    Includes verification, certifications, and impact scoring
    """
    ROLE_LEVEL_CHOICES = [
        ('general', 'General Volunteer'),
        ('first_aid', 'First-Aid Trained'),
        ('medical', 'Medical Professional'),
    ]
    
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_profile')
    
    # Verification
    role_level = models.CharField(max_length=20, choices=ROLE_LEVEL_CHOICES, default='general')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    id_document = models.FileField(upload_to='verifications/ids/', blank=True, null=True)
    certification = models.FileField(upload_to='verifications/certs/', blank=True, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_volunteers')
    
    # Availability
    is_available = models.BooleanField(default=True)
    availability_radius_km = models.IntegerField(default=5)  # How far willing to travel
    
    # Life Impact Score
    total_responses = models.IntegerField(default=0)
    successful_responses = models.IntegerField(default=0)
    average_response_time_minutes = models.FloatField(default=0.0)
    impact_score = models.IntegerField(default=0)  # Calculated score
    
    # Bio
    bio = models.TextField(blank=True)
    specializations = models.CharField(max_length=255, blank=True, help_text="Comma-separated specializations")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_verified(self):
        return self.verification_status == 'approved'
        
    @property
    def is_medical(self):
        return self.role_level == 'medical'

    def calculate_impact_score(self):
        """
        Calculate impact score based on:
        - Number of responses (weight: 40%)
        - Success rate (weight: 30%)
        - Timeliness (weight: 20%)
        - Role level (weight: 10%)
        """
        response_score = min(self.total_responses * 10, 400)  # Max 400 points
        
        success_rate = (self.successful_responses / self.total_responses * 100) if self.total_responses > 0 else 0
        success_score = success_rate * 3  # Max 300 points
        
        # Lower response time is better
        time_score = max(200 - (self.average_response_time_minutes * 2), 0)  # Max 200 points
        
        role_multiplier = {'general': 1.0, 'first_aid': 1.5, 'medical': 2.0}
        role_score = role_multiplier.get(self.role_level, 1.0) * 100  # Max 200 points
        
        self.impact_score = int(response_score + success_score + time_score + role_score)
        self.save()
        return self.impact_score
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_level_display()} ({self.impact_score} pts)"
    
    class Meta:
        ordering = ['-impact_score', '-created_at']


class AreaSafetyScore(models.Model):
    """
    Community safety score for geographical areas
    Based on volunteer density and average response time
    """
    area_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius_km = models.IntegerField(default=2)
    
    # Metrics
    volunteer_count = models.IntegerField(default=0)
    average_response_time_minutes = models.FloatField(default=0.0)
    total_emergencies = models.IntegerField(default=0)
    resolved_emergencies = models.IntegerField(default=0)
    
    # Score (0-100)
    safety_score = models.IntegerField(default=50)
    score_color = models.CharField(max_length=20, default='yellow')  # green, yellow, orange, red
    
    last_calculated = models.DateTimeField(auto_now=True)
    
    def calculate_safety_score(self):
        """
        Calculate safety score based on:
        - Volunteer density (weight: 50%)
        - Average response time (weight: 30%)
        - Resolution rate (weight: 20%)
        """
        # Volunteer density (assume 1 volunteer per km² is ideal)
        area_sq_km = 3.14159 * (self.radius_km ** 2)
        density = self.volunteer_count / area_sq_km if area_sq_km > 0 else 0
        density_score = min(density * 50, 50)  # Max 50 points
        
        # Response time (5 minutes or less is ideal)
        time_score = max(30 - (self.average_response_time_minutes * 3), 0)  # Max 30 points
        
        # Resolution rate
        resolution_rate = (self.resolved_emergencies / self.total_emergencies * 100) if self.total_emergencies > 0 else 50
        resolution_score = resolution_rate * 0.2  # Max 20 points
        
        self.safety_score = int(density_score + time_score + resolution_score)
        
        # Assign color
        if self.safety_score >= 75:
            self.score_color = 'green'
        elif self.safety_score >= 50:
            self.score_color = 'yellow'
        elif self.safety_score >= 25:
            self.score_color = 'orange'
        else:
            self.score_color = 'red'
        
        self.save()
        return self.safety_score
    
    def __str__(self):
        return f"{self.area_name} - Score: {self.safety_score} ({self.score_color})"
    
    class Meta:
        ordering = ['-safety_score']


class ResponderStats(models.Model):
    """
    Track volunteer/responder performance metrics for enhanced dashboard
    """
    responder = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responder_stats'
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
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_stats(self):
        """Recalculate all statistics"""
        from emergencies.models import Emergency, EmergencyResponse
        from django.utils import timezone
        
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
        from django.utils import timezone
        
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
    
    def earn_badge(self, badge_id, points=0):
        """Award a badge to the responder"""
        if badge_id not in self.badges:
            self.badges.append(badge_id)
            self.total_points += points
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
