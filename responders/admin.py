from django.contrib import admin
from .models import VolunteerProfile, AreaSafetyScore


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for volunteer verification and management
    """
    list_display = [
        'user', 
        'role_level', 
        'verification_status', 
        'is_available', 
        'impact_score',
        'total_responses',
        'created_at'
    ]
    list_filter = ['verification_status', 'role_level', 'is_available']
    search_fields = ['user__username', 'user__email', 'specializations']
    readonly_fields = ['impact_score', 'total_responses', 'successful_responses', 'average_response_time_minutes', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Role & Verification', {
            'fields': ('role_level', 'verification_status', 'id_document', 'certification', 'verified_at', 'verified_by')
        }),
        ('Availability', {
            'fields': ('is_available', 'availability_radius_km')
        }),
        ('Impact Metrics', {
            'fields': ('total_responses', 'successful_responses', 'average_response_time_minutes', 'impact_score')
        }),
        ('Profile', {
            'fields': ('bio', 'specializations')
        }),
    )
    
    actions = ['approve_volunteers', 'reject_volunteers', 'recalculate_scores']
    
    def approve_volunteers(self, request, queryset):
        """Bulk approve volunteers"""
        from django.utils import timezone
        queryset.update(verification_status='approved', verified_at=timezone.now(), verified_by=request.user)
        self.message_user(request, f"{queryset.count()} volunteers approved.")
    approve_volunteers.short_description = "Approve selected volunteers"
    
    def reject_volunteers(self, request, queryset):
        """Bulk reject volunteers"""
        queryset.update(verification_status='rejected')
        self.message_user(request, f"{queryset.count()} volunteers rejected.")
    reject_volunteers.short_description = "Reject selected volunteers"
    
    def recalculate_scores(self, request, queryset):
        """Recalculate impact scores"""
        for volunteer in queryset:
            volunteer.calculate_impact_score()
        self.message_user(request, f"Recalculated scores for {queryset.count()} volunteers.")
    recalculate_scores.short_description = "Recalculate impact scores"


@admin.register(AreaSafetyScore)
class AreaSafetyScoreAdmin(admin.ModelAdmin):
    """
    Admin interface for area safety scores
    """
    list_display = [
        'area_name',
        'safety_score',
        'score_color',
        'volunteer_count',
        'average_response_time_minutes',
        'last_calculated'
    ]
    list_filter = ['score_color']
    search_fields = ['area_name']
    readonly_fields = ['safety_score', 'score_color', 'last_calculated']
    
    actions = ['recalculate_safety_scores']
    
    def recalculate_safety_scores(self, request, queryset):
        """Recalculate safety scores for selected areas"""
        for area in queryset:
            area.calculate_safety_score()
        self.message_user(request, f"Recalculated safety scores for {queryset.count()} areas.")
    recalculate_safety_scores.short_description = "Recalculate safety scores"
