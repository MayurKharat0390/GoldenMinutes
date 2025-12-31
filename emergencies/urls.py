from django.urls import path
from . import views

app_name = 'emergencies'

urlpatterns = [
    # SOS & Emergency Management
    path('sos/', views.trigger_sos, name='trigger_sos'),
    path('map/', views.emergency_map, name='emergency_map'),
    path('list/', views.emergency_list, name='emergency_list'),
    path('<uuid:emergency_id>/', views.emergency_detail, name='emergency_detail'),
    path('<uuid:emergency_id>/timeline/', views.emergency_timeline, name='emergency_timeline'),
    
    # Bystander Mode
    path('<uuid:emergency_id>/bystander/', views.bystander_guidance, name='bystander_guidance'),
    
    # API endpoints for real-time updates
    path('api/active/', views.api_active_emergencies, name='api_active_emergencies'),
    path('api/<uuid:emergency_id>/status/', views.api_emergency_status, name='api_emergency_status'),
    
    # Push Notifications API
    path('api/push-subscribe/', views.api_push_subscribe, name='api_push_subscribe'),
    
    # Responder Location API (for ETA)
    path('api/responder-location/<int:responder_id>/', views.api_responder_location, name='api_responder_location'),
    path('api/update-location/', views.api_update_responder_location, name='api_update_responder_location'),
]
