from django.urls import path
from . import views

app_name = 'responders'

urlpatterns = [
    # Volunteer Registration & Dashboard
    path('register/', views.volunteer_register, name='volunteer_register'),
    path('dashboard/', views.enhanced_dashboard, name='volunteer_dashboard'),  # New enhanced is now default
    path('dashboard/basic/', views.volunteer_dashboard, name='volunteer_dashboard_basic'),  # Old basic version
    path('dashboard/enhanced/', views.enhanced_dashboard, name='enhanced_dashboard'),  # Keep for compatibility
    path('profile/<int:pk>/', views.volunteer_profile, name='volunteer_profile'),
    
    # Emergency Response Actions
    path('emergency/<uuid:emergency_id>/accept/', views.accept_emergency, name='accept_emergency'),
    path('emergency/<uuid:emergency_id>/decline/', views.decline_emergency, name='decline_emergency'),
    path('emergency/<uuid:emergency_id>/update-status/', views.update_response_status, name='update_response_status'),
    
    # Leaderboard & Community
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('safety-scores/', views.safety_scores, name='safety_scores'),
    
    # API endpoints
    path('api/toggle-availability/', views.api_toggle_availability, name='api_toggle_availability'),
    path('api/check-alerts/', views.check_new_emergencies, name='check_new_emergencies'),
    path('api/ack-alert/', views.ack_alert, name='ack_alert'),
    
    # Analytics (Admin Only)
    path('analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-approvals/', views.admin_approvals, name='admin_approvals'),
    # Community
    path('profile/<str:username>/', views.responder_profile_public, name='responder_profile_public'),
]
