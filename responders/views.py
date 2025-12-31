from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import VolunteerProfile, AreaSafetyScore, ResponderStats
from emergencies.models import Emergency, EmergencyResponse, EmergencyTimeline
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def volunteer_register(request):
    """Volunteer registration/profile creation"""
    # Check if already has volunteer profile
    try:
        profile = request.user.volunteer_profile
        messages.info(request, 'You already have a volunteer profile.')
        return redirect('responders:volunteer_dashboard')
    except VolunteerProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        role_level = request.POST.get('role_level', 'general')
        bio = request.POST.get('bio', '')
        specializations = request.POST.get('specializations', '')
        availability_radius_km = request.POST.get('availability_radius_km', 5)
        
        # Create volunteer profile
        profile = VolunteerProfile.objects.create(
            user=request.user,
            role_level=role_level,
            bio=bio,
            specializations=specializations,
            availability_radius_km=availability_radius_km,
            verification_status='pending'
        )
        
        # Update user role
        request.user.role = 'volunteer'
        request.user.save()
        
        messages.success(request, 'Volunteer profile created! Awaiting admin verification.')
        return redirect('responders:volunteer_dashboard')
    
    return render(request, 'responders/volunteer_register.html')


@login_required
def volunteer_dashboard(request):
    """Volunteer dashboard"""
    if request.user.role != 'volunteer':
        messages.error(request, 'You must be a registered volunteer to access this page.')
        return redirect('home')
    
    try:
        profile = request.user.volunteer_profile
    except VolunteerProfile.DoesNotExist:
        return redirect('responders:volunteer_register')
    
    # Get nearby active emergencies
    active_emergencies = Emergency.objects.filter(
        status='active'
    )[:10]  # Limit to 10 for demo
    
    # Get user's emergency responses
    my_responses = EmergencyResponse.objects.filter(
        responder=request.user
    ).order_by('-notified_at')[:10]
    
    context = {
        'profile': profile,
        'active_emergencies': active_emergencies,
        'my_responses': my_responses
    }
    return render(request, 'responders/dashboard.html', context)


@login_required
def volunteer_profile(request, pk):
    """View volunteer profile"""
    profile = get_object_or_404(VolunteerProfile, pk=pk)
    
    context = {
        'profile': profile
    }
    return render(request, 'responders/profile.html', context)


@login_required
@require_POST
def accept_emergency(request, emergency_id):
    """Accept an emergency"""
    emergency = get_object_or_404(Emergency, emergency_id=emergency_id)
    
    if request.user.role != 'volunteer':
        return JsonResponse({'success': False, 'message': 'Only volunteers can accept emergencies'}, status=403)
    
    # Check if emergency is still active
    if emergency.status != 'active':
        # If I am already the responder, just redirect back
        if emergency.primary_responder == request.user:
             messages.info(request, 'You have already accepted this emergency.')
             return redirect('emergencies:emergency_detail', emergency_id=emergency.emergency_id)
             
        return JsonResponse({'success': False, 'message': 'Emergency is no longer active'}, status=400)
    
    # Assign responder
    emergency.primary_responder = request.user
    emergency.status = 'responder_assigned'
    emergency.responder_accepted_at = timezone.now()
    emergency.save()
    
    # Create or update response
    response, created = EmergencyResponse.objects.get_or_create(
        emergency=emergency,
        responder=request.user,
        defaults={'status': 'accepted'}
    )
    if not created:
        response.status = 'accepted'
        response.responded_at = timezone.now()
        response.save()
    
    # Create timeline entry
    EmergencyTimeline.objects.create(
        emergency=emergency,
        event_type='responder_accepted',
        description=f'{request.user.username} accepted the emergency',
        actor=request.user
    )
    
    messages.success(request, 'Emergency accepted! Please proceed to the location.')
    return redirect('emergencies:emergency_detail', emergency_id=emergency.emergency_id)


@login_required
@require_POST
def decline_emergency(request, emergency_id):
    """Decline an emergency"""
    emergency = get_object_or_404(Emergency, emergency_id=emergency_id)
    
    # Create or update response
    response, created = EmergencyResponse.objects.get_or_create(
        emergency=emergency,
        responder=request.user,
        defaults={'status': 'declined'}
    )
    if not created:
        response.status = 'declined'
        response.responded_at = timezone.now()
        response.save()
    
    # Create timeline entry
    EmergencyTimeline.objects.create(
        emergency=emergency,
        event_type='responder_declined',
        description=f'{request.user.username} declined the emergency',
        actor=request.user
    )
    
    messages.info(request, 'Emergency declined.')
    return redirect('responders:volunteer_dashboard')


@login_required
@require_POST
def update_response_status(request, emergency_id):
    """Update response status (en route, arrived)"""
    emergency = get_object_or_404(Emergency, emergency_id=emergency_id)
    new_status = request.POST.get('status')
    
    if emergency.primary_responder != request.user:
        return JsonResponse({'success': False, 'message': 'You are not the primary responder'}, status=403)
    
    # Update emergency status
    if new_status == 'en_route':
        emergency.status = 'responder_en_route'
        event_type = 'responder_en_route'
        description = f'{request.user.username} is en route'
    elif new_status == 'arrived':
        emergency.status = 'responder_arrived'
        emergency.responder_arrived_at = timezone.now()
        event_type = 'responder_arrived'
        description = f'{request.user.username} has arrived'
    else:
        return JsonResponse({'success': False, 'message': 'Invalid status'}, status=400)
    
    emergency.save()
    
    # Create timeline entry
    EmergencyTimeline.objects.create(
        emergency=emergency,
        event_type=event_type,
        description=description,
        actor=request.user
    )
    
    messages.success(request, f'Status updated to: {new_status}')
    return redirect('emergencies:emergency_detail', emergency_id=emergency.emergency_id)


@login_required
def leaderboard(request):
    """Volunteer leaderboard"""
    volunteers = VolunteerProfile.objects.filter(
        verification_status='approved'
    ).order_by('-impact_score')[:50]
    
    context = {
        'volunteers': volunteers
    }
    return render(request, 'responders/leaderboard.html', context)


@login_required
def safety_scores(request):
    """Area safety scores"""
    areas = AreaSafetyScore.objects.all().order_by('-safety_score')
    
    context = {
        'areas': areas
    }
    return render(request, 'responders/safety_scores.html', context)


@login_required
@require_POST
def api_toggle_availability(request):
    """API: Toggle volunteer availability"""
    try:
        profile = request.user.volunteer_profile
        profile.is_available = not profile.is_available
        profile.save()
        
        return JsonResponse({
            'success': True,
            'is_available': profile.is_available
        })
    except VolunteerProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Volunteer profile not found'
        }, status=404)


@login_required
def enhanced_dashboard(request):
    """Enhanced volunteer dashboard with stats, badges, and gamification"""
    if request.user.role != 'volunteer':
        messages.error(request, 'You must be a registered volunteer to access this page.')
        return redirect('home')
    
    try:
        profile = request.user.volunteer_profile
    except VolunteerProfile.DoesNotExist:
        return redirect('responders:volunteer_register')
    
    # Get or create responder stats
    from .models import ResponderStats, Badge
    stats, created = ResponderStats.objects.get_or_create(responder=request.user)
    
    # Update stats
    stats.update_stats()
    
    # Get all badges
    all_badges = Badge.objects.all()
    earned_badges = Badge.objects.filter(badge_id__in=stats.badges)
    
    # Calculate progress to next level
    current_level_points = (stats.level - 1) * 100
    next_level_points = stats.level * 100
    level_progress = ((stats.total_points - current_level_points) / 100) * 100
    
    # Get leaderboard (top 10)
    leaderboard = ResponderStats.objects.select_related('responder').order_by('-total_points')[:10]
    user_rank = ResponderStats.objects.filter(total_points__gt=stats.total_points).count() + 1
    
    # Get recent emergencies
    active_emergencies = Emergency.objects.filter(status='active')[:5]
    my_emergencies = Emergency.objects.filter(primary_responder=request.user).order_by('-triggered_at')[:5]
    
    # Get recent responses
    my_responses = EmergencyResponse.objects.filter(
        responder=request.user
    ).select_related('emergency').order_by('-notified_at')[:10]
    
    # Calculate badge progress
    badge_progress = []
    for badge in all_badges:
        if badge.badge_id not in stats.badges:
            # Calculate progress towards this badge
            if badge.requirement_type == 'total_responses':
                current = stats.total_responses
                required = badge.requirement_value
            elif badge.requirement_type == 'avg_response_time':
                current = badge.requirement_value - stats.average_response_time
                required = badge.requirement_value
            elif badge.requirement_type == 'lives_saved':
                current = stats.lives_saved
                required = badge.requirement_value
            elif badge.requirement_type == 'current_streak':
                current = stats.current_streak
                required = badge.requirement_value
            else:
                current = 0
                required = 1
            
            progress_pct = min((current / required) * 100, 100) if required > 0 else 0
            
            badge_progress.append({
                'badge': badge,
                'current': current,
                'required': required,
                'progress': progress_pct
            })
    
    # Sort by progress (closest to earning first)
    badge_progress.sort(key=lambda x: x['progress'], reverse=True)
    
    context = {
        'profile': profile,
        'stats': stats,
        'all_badges': all_badges,
        'earned_badges': earned_badges,
        'badge_progress': badge_progress[:5],  # Top 5 closest badges
        'level_progress': level_progress,
        'leaderboard': leaderboard,
        'user_rank': user_rank,
        'active_emergencies': active_emergencies,
        'my_emergencies': my_emergencies,
        'my_responses': my_responses,
    }
    
    return render(request, 'responders/dashboard_enhanced.html', context)


@staff_member_required
def admin_analytics(request):
    """
    Analytics dashboard for admins to view system performance
    """
    import json
    from django.db.models.functions import ExtractHour
    
    # 1. Key Metrics
    total_emergencies = Emergency.objects.count()
    total_volunteers = VolunteerProfile.objects.count()
    total_lives_saved = ResponderStats.objects.aggregate(total=Sum('lives_saved'))['total'] or 0
    avg_response_time = ResponderStats.objects.aggregate(avg=Avg('average_response_time'))['avg'] or 0
    
    # 2. Daily Emergency Trends (Last 30 days)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    
    daily_stats = Emergency.objects.filter(
        triggered_at__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('triggered_at')
    ).values('date').annotate(
        count=Count('emergency_id')
    ).order_by('date')
    
    dates = [stat['date'].strftime('%Y-%m-%d') for stat in daily_stats]
    counts = [stat['count'] for stat in daily_stats]
    
    # 3. Emergency Types Distribution
    type_stats = Emergency.objects.values('emergency_type').annotate(
        count=Count('emergency_id')
    ).order_by('-count')
    
    type_labels = [stat['emergency_type'].replace('_', ' ').title() for stat in type_stats]
    type_counts = [stat['count'] for stat in type_stats]
    
    # 4. Peak Hours Analysis (0-23)
    peak_stats = Emergency.objects.annotate(
        hour=ExtractHour('triggered_at')
    ).values('hour').annotate(
        count=Count('emergency_id')
    ).order_by('hour')
    
    hours_data = {stat['hour']: stat['count'] for stat in peak_stats}
    peak_labels = [f"{h:02d}:00" for h in range(24)]
    peak_counts = [hours_data.get(h, 0) for h in range(24)]
    
    # 5. Efficiency Funnel
    funnel_triggered = total_emergencies
    funnel_accepted = EmergencyResponse.objects.filter(status='accepted').count()
    funnel_arrived = EmergencyResponse.objects.filter(status='arrived').count()
    funnel_resolved = Emergency.objects.filter(status='resolved').count()
    
    funnel_data = [funnel_triggered, funnel_accepted, funnel_arrived, funnel_resolved]
    
    # 6. Heatmap Data (Lat/Long)
    heatmap_raw = list(Emergency.objects.values('latitude', 'longitude', 'severity'))
    # Convert Decimal/float to simple float for JSON
    heatmap_data = [{'x': float(h['longitude']), 'y': float(h['latitude'])} for h in heatmap_raw]

    context = {
        'total_emergencies': total_emergencies,
        'total_volunteers': total_volunteers,
        'total_lives_saved': total_lives_saved,
        'avg_response_time': round(avg_response_time, 1),
        
        # Serialize lists to JSON strings for safe JS usage
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
        'type_labels': json.dumps(type_labels),
        'type_counts': json.dumps(type_counts),
        'peak_labels': json.dumps(peak_labels),
        'peak_counts': json.dumps(peak_counts),
        'funnel_data': json.dumps(funnel_data),
        'heatmap_data': json.dumps(heatmap_data),
    }
    
    return render(request, 'responders/analytics.html', context)

@staff_member_required
def admin_approvals(request):
    """
    Admin Hub to verify volunteer documents and approve/reject profiles.
    """
    # Handle Actions
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')
        
        profile = get_object_or_404(VolunteerProfile, id=profile_id)
        
        if action == 'approve':
            profile.verification_status = 'approved'
            profile.verified_by = request.user
            profile.verified_at = timezone.now()
            # Determine role based on certs (logic can be manual or auto)
            # keeping current role or upgrading if requested
            profile.save()
            messages.success(request, f"✅ Approved {profile.user.username} as {profile.get_role_level_display()}!")
            
        elif action == 'reject':
            profile.verification_status = 'rejected'
            profile.save()
            messages.warning(request, f"❌ Rejected application for {profile.user.username}.")
            
        return redirect('responders:admin_approvals')

    # Get Pending Requests
    pending_volunteers = VolunteerProfile.objects.filter(
        verification_status='pending'
    ).select_related('user').order_by('-created_at')
    
    return render(request, 'responders/admin_approvals.html', {
        'pending_volunteers': pending_volunteers
    })

from django.http import JsonResponse

@login_required
def check_new_emergencies(request):
    """
    Lightweight API for the frontend to poll for new alerts.
    """
    # Using 'last_checked' timestamp from session, or default to now
    last_checked_str = request.session.get('last_alert_check')
    
    # Check for emergencies created in the last 5 minutes that are active
    # In a real app, you would filter by geospatial distance here.
    # For now, we alert on ANY active emergency the user hasn't responded to.
    
    from emergencies.models import Emergency, EmergencyResponse
    
    # Get active emergencies
    active_emergencies = Emergency.objects.filter(
        status='active'
    ).exclude(
        primary_responder=request.user # Don't alert if I'm already the primary
    ).exclude(
        responses__responder=request.user # Don't alert if I already responded
    )
    
    # If we have a timestamp, only newer than that
    # But actually, simpler is: Just get the latest one I haven't seen?
    # Let's just return the latest active one to show as a popup
    
    if active_emergencies.exists():
        latest = active_emergencies.latest('created_at')
        
        # Avoid showing the same alert repeatedly in the same session instantly
        # Check if we just showed this ID
        last_alert_id = request.session.get('last_alert_id')
        
        # We send emergency_id to frontend, so we must compare against that
        if str(latest.emergency_id) != str(last_alert_id):
            # NEW ALERT!
            data = {
                'has_new': True,
                'id': str(latest.emergency_id), # Use emergency_id uuid field? Or id logic?
                'location': latest.location_address or f"{latest.latitude}, {latest.longitude}",
                'type': latest.get_emergency_type_display(),
                'distance': "Calculating...", # Frontend can calc dist if it has user loc
                'timestamp': latest.created_at.isoformat()
            }
            return JsonResponse(data)
    
    return JsonResponse({'has_new': False})

@login_required
def ack_alert(request):
    """
    Endpoint to acknowledge an alert so it stops popping up.
    """
    if request.method == 'POST':
        emergency_id = request.POST.get('emergency_id')
        request.session['last_alert_id'] = str(emergency_id)
        # print(f"✅ ACK ALERT: {emergency_id} saved to session.")
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
@login_required
def responder_profile_public(request, username):
    """
    Public profile view for a responder (Read-only).
    Shows stats, badges, and role. Hides private contact info.
    """
    target_user = get_object_or_404(User, username=username)
    
    # Get Profile & Stats
    try:
        profile = target_user.volunteer_profile
        stats = target_user.responder_stats
    except:
        messages.error(request, "This user is not a registered responder.")
        return redirect('responders:volunteer_dashboard')
        
    # Enrich Badges
    badge_data = []
    if stats.badges:
        icons = {
            'cpr_certified': 'bi-heart-pulse-fill',
            'first_aid_expert': 'bi-bandaid-fill',
            'speed_demon': 'bi-lightning-charge-fill',
            'first_response': 'bi-star-fill',
            'week_warrior': 'bi-calendar-check-fill',
            'community_hero': 'bi-people-fill'
        }
        for b_id in stats.badges:
            badge_data.append({
                'id': b_id,
                'name': b_id.replace('_', ' ').title(),
                'icon': icons.get(b_id, 'bi-award-fill')
            })
    
    context = {
        'target_user': target_user,
        'profile': profile,
        'stats': stats,
        'badges': badge_data,
        'is_me': (request.user == target_user)
    }
    return render(request, 'responders/profile_public.html', context)
