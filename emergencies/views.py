from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
import uuid
from .models import Emergency, EmergencyResponse, EmergencyTimeline, BystanderGuidance


@login_required
def trigger_sos(request):
    """Trigger SOS emergency"""
    if request.method == 'POST':
        emergency_type = request.POST.get('emergency_type')
        description = request.POST.get('description', '')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Create emergency
        emergency = Emergency.objects.create(
            victim=request.user,
            emergency_type=emergency_type,
            description=description,
            latitude=latitude,
            longitude=longitude
        )
        
        # Calculate severity
        emergency.calculate_severity()
        
        # Create timeline entry
        EmergencyTimeline.objects.create(
            emergency=emergency,
            event_type='sos_triggered',
            description=f'SOS triggered by {request.user.username}',
            actor=request.user
        )
        
        messages.success(request, 'SOS triggered! Notifying nearby responders...')
        return redirect('emergencies:emergency_detail', emergency_id=emergency.emergency_id)
    
    return render(request, 'emergencies/trigger_sos.html')


@login_required
def emergency_map(request):
    """Live emergency map"""
    from django.conf import settings
    
    # Get active emergencies
    emergencies = Emergency.objects.filter(
        status__in=['active', 'responder_assigned', 'responder_en_route']
    ).order_by('-triggered_at')
    
    # Role-based filtering
    if request.user.role == 'citizen':
        # Citizens only see their own emergencies
        emergencies = emergencies.filter(victim=request.user)
    # Volunteers and admins see all emergencies
    
    context = {
        'emergencies': emergencies,
        'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN
    }
    return render(request, 'emergencies/map.html', context)


@login_required
def emergency_list(request):
    """List of emergencies"""
    if request.user.role == 'admin':
        emergencies = Emergency.objects.all()
    elif request.user.role == 'volunteer':
        emergencies = Emergency.objects.filter(
            Q(status='active') | Q(primary_responder=request.user)
        )
    else:
        emergencies = Emergency.objects.filter(victim=request.user)
    
    context = {
        'emergencies': emergencies
    }
    return render(request, 'emergencies/list.html', context)


@login_required
def emergency_detail(request, emergency_id):
    """Emergency detail view"""
    emergency = get_object_or_404(Emergency, emergency_id=emergency_id)
    
    # Check permissions
    if request.user.role == 'citizen' and emergency.victim != request.user:
        messages.error(request, 'You do not have permission to view this emergency.')
        return redirect('home')
    
    context = {
        'emergency': emergency,
        'timeline': emergency.timeline.all()
    }
    return render(request, 'emergencies/detail.html', context)


@login_required
def emergency_timeline(request, emergency_id):
    """Emergency timeline view"""
    emergency = get_object_or_404(Emergency, emergency_id=emergency_id)
    timeline = emergency.timeline.all()
    
    context = {
        'emergency': emergency,
        'timeline': timeline
    }
    return render(request, 'emergencies/timeline.html', context)


@login_required
def bystander_guidance(request, emergency_id):
    """Bystander guidance view with multi-language support"""
    emergency = get_object_or_404(Emergency, emergency_id=emergency_id)
    
    # Get language from URL parameter, default to English
    language = request.GET.get('lang', 'en')
    if language not in ['en', 'hi', 'mr']:
        language = 'en'
    
    # Get guidance in the selected language
    guidance = BystanderGuidance.objects.filter(
        emergency_type=emergency.emergency_type,
        language=language
    )
    
    # If no guidance found in selected language, fall back to English
    if not guidance.exists():
        guidance = BystanderGuidance.objects.filter(
            emergency_type=emergency.emergency_type,
            language='en'
        )
    
    context = {
        'emergency': emergency,
        'guidance_steps': guidance,
        'current_language': language,
    }
    return render(request, 'emergencies/bystander_guidance.html', context)


def api_active_emergencies(request):
    """API: Get active emergencies (for map updates)"""
    emergencies = Emergency.objects.filter(
        status__in=['active', 'responder_assigned', 'responder_en_route']
    )
    
    data = []
    for emergency in emergencies:
        data.append({
            'emergency_id': str(emergency.emergency_id),
            'emergency_type': emergency.emergency_type,
            'emergency_type_display': emergency.get_emergency_type_display(),
            'severity': emergency.severity,
            'status': emergency.status,
            'status_display': emergency.get_status_display(),
            'latitude': float(emergency.latitude),
            'longitude': float(emergency.longitude),
            'triggered_at': emergency.triggered_at.isoformat()
        })
    
    return JsonResponse({'emergencies': data})


def api_emergency_status(request, emergency_id):
    """API: Get emergency status"""
    emergency = get_object_or_404(Emergency, emergency_id=emergency_id)
    
    data = {
        'emergency_id': str(emergency.emergency_id),
        'status': emergency.status,
        'status_display': emergency.get_status_display(),
        'bystander_mode_active': emergency.bystander_mode_active
    }
    
    if emergency.primary_responder:
        data['primary_responder'] = {
            'name': emergency.primary_responder.username,
            'eta': 5  # Mock ETA
        }
    
    return JsonResponse(data)


def api_push_subscribe(request):
    """API: Save push notification subscription"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    import json
    from .models import PushSubscription
    
    try:
        data = json.loads(request.body)
        subscription_info = data.get('subscription')
        user_agent = data.get('user_agent', '')
        
        # Create or update subscription
        subscription, created = PushSubscription.objects.update_or_create(
            user=request.user,
            defaults={
                'subscription_info': subscription_info,
                'user_agent': user_agent,
                'is_active': True
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Subscription saved successfully',
            'created': created
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def api_responder_location(request, responder_id):
    """API: Get responder's current location for ETA calculation"""
    from .models import ResponderLocation
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        responder = User.objects.get(id=responder_id)
        location = ResponderLocation.objects.filter(responder=responder).first()
        
        if location:
            return JsonResponse({
                'latitude': float(location.latitude),
                'longitude': float(location.longitude),
                'accuracy': location.accuracy,
                'updated_at': location.updated_at.isoformat()
            })
        else:
            return JsonResponse({'error': 'Location not available'}, status=404)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'Responder not found'}, status=404)


@login_required
def api_update_responder_location(request):
    """API: Update responder's current GPS location"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    from .models import ResponderLocation
    import json
    
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        accuracy = data.get('accuracy')
        
        if not latitude or not longitude:
            return JsonResponse({'error': 'Latitude and longitude required'}, status=400)
        
        # Update or create location
        location, created = ResponderLocation.objects.update_or_create(
            responder=request.user,
            defaults={
                'latitude': latitude,
                'longitude': longitude,
                'accuracy': accuracy
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Location updated successfully'
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

