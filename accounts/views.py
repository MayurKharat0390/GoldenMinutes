from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from .models import User


def register(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role', 'citizen')
        phone_number = request.POST.get('phone_number', '')
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone_number=phone_number,
            terms_accepted=True,
            terms_accepted_at=timezone.now()
        )
        
        # Auto-login
        login(request, user)
        messages.success(request, f'Welcome to Golden Minutes, {username}!')
        
        # Redirect based on role
        if role == 'volunteer':
            return redirect('responders:volunteer_register')
        else:
            return redirect('home')
    
    return render(request, 'accounts/register.html')


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next or home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """User profile view"""
    context = {
        'user': request.user
    }
    
    # Add volunteer profile if exists
    if request.user.role == 'volunteer':
        try:
            context['volunteer_profile'] = request.user.volunteer_profile
        except:
            pass
    
    return render(request, 'accounts/profile.html', context)


@login_required
@require_POST
def update_location(request):
    """Update user's current location (AJAX endpoint)"""
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude and longitude:
            request.user.latitude = latitude
            request.user.longitude = longitude
            request.user.location_updated_at = timezone.now()
            request.user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Location updated successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid location data'
            }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
