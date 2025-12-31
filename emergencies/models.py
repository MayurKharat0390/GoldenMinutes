from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Emergency(models.Model):
    """
    Core Emergency/SOS Event model
    Tracks emergency from trigger to resolution
    """
    EMERGENCY_TYPE_CHOICES = [
        ('accident', 'Accident'),
        ('medical', 'Medical'),
        ('fire', 'Fire'),
        ('personal_safety', 'Personal Safety'),
        ('disaster', 'Disaster'),
    ]
    
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('moderate', 'Moderate'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('responder_assigned', 'Responder Assigned'),
        ('responder_en_route', 'Responder En Route'),
        ('responder_arrived', 'Responder Arrived'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Unique identifier
    emergency_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Who triggered
    victim = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergencies')
    
    # Emergency details
    emergency_type = models.CharField(max_length=20, choices=EMERGENCY_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_address = models.CharField(max_length=255, blank=True)
    
    # Additional context
    description = models.TextField(blank=True)
    voice_note = models.FileField(upload_to='emergencies/voice/', blank=True, null=True)
    
    # Assigned responder
    primary_responder = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_emergencies'
    )
    
    # Timestamps
    triggered_at = models.DateTimeField(auto_now_add=True)
    responder_accepted_at = models.DateTimeField(null=True, blank=True)
    responder_arrived_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Bystander mode activated
    bystander_mode_active = models.BooleanField(default=False)
    bystander_mode_activated_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_severity(self):
        """
        AI-inspired (rule-based) severity classification
        """
        severity_map = {
            'fire': 'critical',
            'disaster': 'critical',
            'medical': 'high',
            'personal_safety': 'high',
            'accident': 'moderate',
        }
        
        # Additional context-based rules could be added here
        # For now, use simple mapping
        self.severity = severity_map.get(self.emergency_type, 'moderate')
        self.save()
        return self.severity
    
    def activate_bystander_mode(self):
        """
        Activate bystander mode if no responder accepts within timeout
        """
        if not self.primary_responder and not self.bystander_mode_active:
            self.bystander_mode_active = True
            self.bystander_mode_activated_at = timezone.now()
            self.save()
            return True
        return False
    
    def get_response_time_minutes(self):
        """
        Calculate response time from trigger to responder acceptance
        """
        if self.responder_accepted_at:
            delta = self.responder_accepted_at - self.triggered_at
            return delta.total_seconds() / 60
        return None
    
    def __str__(self):
        return f"{self.get_emergency_type_display()} - {self.emergency_id} ({self.status})"
    
    class Meta:
        ordering = ['-triggered_at']
        verbose_name_plural = "Emergencies"


class EmergencyResponse(models.Model):
    """
    Tracks responder interactions with emergencies
    Multiple responders may be notified, but only one becomes primary
    """
    STATUS_CHOICES = [
        ('notified', 'Notified'),
        ('viewed', 'Viewed'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('en_route', 'En Route'),
        ('arrived', 'Arrived'),
    ]
    
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_responses')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notified')
    
    # Distance and ETA (can be calculated or mocked)
    distance_km = models.FloatField(null=True, blank=True)
    estimated_arrival_minutes = models.IntegerField(null=True, blank=True)
    
    # Timestamps
    notified_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.responder.username} -> {self.emergency.emergency_id} ({self.status})"
    
    class Meta:
        ordering = ['distance_km', '-notified_at']
        unique_together = ['emergency', 'responder']


class EmergencyTimeline(models.Model):
    """
    Audit log for emergency events
    Tracks every status change and action
    """
    EVENT_TYPE_CHOICES = [
        ('sos_triggered', 'SOS Triggered'),
        ('responder_notified', 'Responder Notified'),
        ('responder_accepted', 'Responder Accepted'),
        ('responder_declined', 'Responder Declined'),
        ('responder_en_route', 'Responder En Route'),
        ('responder_arrived', 'Responder Arrived'),
        ('bystander_mode_activated', 'Bystander Mode Activated'),
        ('status_updated', 'Status Updated'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ]
    
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE, related_name='timeline')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    description = models.TextField()
    
    # Optional: who performed the action
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.emergency.emergency_id} - {self.get_event_type_display()} at {self.timestamp}"
    
    class Meta:
        ordering = ['timestamp']


class BystanderGuidance(models.Model):
    """
    Guided instructions for bystanders
    Pre-populated with first-aid and emergency response steps
    Supports multiple languages for accessibility
    """
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
    ]
    
    emergency_type = models.CharField(max_length=20, choices=Emergency.EMERGENCY_TYPE_CHOICES)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    title = models.CharField(max_length=200)
    step_number = models.IntegerField()
    instruction = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="CSS class for icon")
    warning = models.TextField(blank=True, help_text="Important warnings or don'ts")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_emergency_type_display()} ({self.get_language_display()}) - Step {self.step_number}: {self.title}"
    
    class Meta:
        ordering = ['emergency_type', 'language', 'step_number']
        unique_together = ['emergency_type', 'language', 'step_number']


class PushSubscription(models.Model):
    """
    Store web push notification subscriptions
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_subscriptions')
    subscription_info = models.JSONField(help_text="Push subscription object from browser")
    user_agent = models.CharField(max_length=255, blank=True)
    
    # Location preferences for notifications
    notification_radius_km = models.FloatField(default=5.0, help_text="Radius in km for emergency notifications")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Push Subscription"
    
    class Meta:
        ordering = ['-created_at']


class ResponderLocation(models.Model):
    """
    Store real-time GPS locations of responders for ETA calculation
    """
    responder = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='current_location'
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accuracy = models.FloatField(null=True, blank=True, help_text="GPS accuracy in meters")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.responder.username} - Location ({self.latitude}, {self.longitude})"
    
    class Meta:
        verbose_name_plural = "Responder Locations"
