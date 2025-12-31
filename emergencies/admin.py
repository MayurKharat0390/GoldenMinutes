from django.contrib import admin
from .models import Emergency, EmergencyResponse, EmergencyTimeline, BystanderGuidance


class EmergencyTimelineInline(admin.TabularInline):
    """Inline timeline for emergencies"""
    model = EmergencyTimeline
    extra = 0
    readonly_fields = ['event_type', 'description', 'actor', 'timestamp']
    can_delete = False


class EmergencyResponseInline(admin.TabularInline):
    """Inline responses for emergencies"""
    model = EmergencyResponse
    extra = 0
    readonly_fields = ['responder', 'status', 'distance_km', 'notified_at']


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    """
    Admin interface for emergency management
    """
    list_display = [
        'emergency_id',
        'victim',
        'emergency_type',
        'severity',
        'status',
        'primary_responder',
        'triggered_at',
        'bystander_mode_active'
    ]
    list_filter = ['emergency_type', 'severity', 'status', 'bystander_mode_active']
    search_fields = ['emergency_id', 'victim__username', 'primary_responder__username', 'location_address']
    readonly_fields = [
        'emergency_id', 
        'triggered_at', 
        'responder_accepted_at', 
        'responder_arrived_at', 
        'resolved_at',
        'bystander_mode_activated_at',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Emergency Details', {
            'fields': ('emergency_id', 'victim', 'emergency_type', 'severity', 'status')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'location_address')
        }),
        ('Context', {
            'fields': ('description', 'voice_note')
        }),
        ('Response', {
            'fields': ('primary_responder', 'bystander_mode_active')
        }),
        ('Timeline', {
            'fields': (
                'triggered_at',
                'responder_accepted_at',
                'responder_arrived_at',
                'resolved_at',
                'bystander_mode_activated_at'
            )
        }),
    )
    
    inlines = [EmergencyResponseInline, EmergencyTimelineInline]
    
    actions = ['activate_bystander_mode', 'mark_resolved']
    
    def activate_bystander_mode(self, request, queryset):
        """Manually activate bystander mode"""
        count = 0
        for emergency in queryset:
            if emergency.activate_bystander_mode():
                count += 1
        self.message_user(request, f"Activated bystander mode for {count} emergencies.")
    activate_bystander_mode.short_description = "Activate bystander mode"
    
    def mark_resolved(self, request, queryset):
        """Mark emergencies as resolved"""
        from django.utils import timezone
        queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, f"Marked {queryset.count()} emergencies as resolved.")
    mark_resolved.short_description = "Mark as resolved"


@admin.register(EmergencyResponse)
class EmergencyResponseAdmin(admin.ModelAdmin):
    """
    Admin interface for emergency responses
    """
    list_display = [
        'emergency',
        'responder',
        'status',
        'distance_km',
        'estimated_arrival_minutes',
        'notified_at'
    ]
    list_filter = ['status']
    search_fields = ['emergency__emergency_id', 'responder__username']
    readonly_fields = ['notified_at', 'viewed_at', 'responded_at', 'arrived_at']


@admin.register(EmergencyTimeline)
class EmergencyTimelineAdmin(admin.ModelAdmin):
    """
    Admin interface for emergency timeline (audit log)
    """
    list_display = ['emergency', 'event_type', 'actor', 'timestamp']
    list_filter = ['event_type']
    search_fields = ['emergency__emergency_id', 'description']
    readonly_fields = ['emergency', 'event_type', 'description', 'actor', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BystanderGuidance)
class BystanderGuidanceAdmin(admin.ModelAdmin):
    """
    Admin interface for bystander guidance instructions
    """
    list_display = ['emergency_type', 'step_number', 'title']
    list_filter = ['emergency_type']
    search_fields = ['title', 'instruction']
    ordering = ['emergency_type', 'step_number']
