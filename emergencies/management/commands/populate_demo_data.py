"""
Management command to populate demo data for Golden Minutes
Run with: python manage.py populate_demo_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with demo data for presentation'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating demo data...')
        
        # Import models here to avoid circular imports
        from responders.models import VolunteerProfile, AreaSafetyScore
        from emergencies.models import Emergency, EmergencyResponse, BystanderGuidance
        
        # Create demo users
        self.stdout.write('Creating demo users...')
        
        # Citizens
        citizens = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'citizen{i}',
                defaults={
                    'email': f'citizen{i}@example.com',
                    'role': 'citizen',
                    'phone_number': f'+91 98765{i:05d}',
                    'terms_accepted': True,
                    'terms_accepted_at': timezone.now(),
                    'latitude': Decimal('19.0760') + Decimal(random.uniform(-0.1, 0.1)),
                    'longitude': Decimal('72.8777') + Decimal(random.uniform(-0.1, 0.1)),
                    'location_updated_at': timezone.now()
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
            citizens.append(user)
        
        # Volunteers
        volunteers = []
        volunteer_data = [
            ('volunteer1', 'medical', 'Dr. Rajesh Kumar', 'Cardiology, Emergency Medicine'),
            ('volunteer2', 'first_aid', 'Priya Sharma', 'First Aid, CPR Certified'),
            ('volunteer3', 'medical', 'Dr. Anjali Patel', 'General Physician'),
            ('volunteer4', 'first_aid', 'Amit Singh', 'First Aid, Fire Safety'),
            ('volunteer5', 'general', 'Neha Gupta', 'Community Volunteer'),
        ]
        
        for username, role_level, full_name, specs in volunteer_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'role': 'volunteer',
                    'phone_number': f'+91 98765{random.randint(10000, 99999)}',
                    'first_name': full_name.split()[0],
                    'last_name': ' '.join(full_name.split()[1:]),
                    'terms_accepted': True,
                    'terms_accepted_at': timezone.now(),
                    'latitude': Decimal('19.0760') + Decimal(random.uniform(-0.1, 0.1)),
                    'longitude': Decimal('72.8777') + Decimal(random.uniform(-0.1, 0.1)),
                    'location_updated_at': timezone.now()
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
            
            # Create volunteer profile
            profile, created = VolunteerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role_level': role_level,
                    'verification_status': 'approved',
                    'verified_at': timezone.now(),
                    'is_available': True,
                    'availability_radius_km': random.randint(3, 10),
                    'total_responses': random.randint(10, 50),
                    'successful_responses': random.randint(8, 45),
                    'average_response_time_minutes': random.uniform(2.0, 8.0),
                    'bio': f'Experienced volunteer specializing in {specs}',
                    'specializations': specs
                }
            )
            if created:
                profile.calculate_impact_score()
            
            volunteers.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(citizens)} citizens and {len(volunteers)} volunteers'))
        
        # Create bystander guidance
        self.stdout.write('Creating bystander guidance...')
        
        guidance_data = [
            # Medical emergencies
            ('medical', 1, 'Check Responsiveness', 'Gently shake the person and ask "Are you okay?" loudly.', 'bi-person-check', 'Do not move the person if spinal injury is suspected'),
            ('medical', 2, 'Call for Help', 'Call 112 immediately. Ask someone nearby to call if possible.', 'bi-telephone', ''),
            ('medical', 3, 'Check Breathing', 'Look for chest movement, listen for breath sounds.', 'bi-lungs', 'Do not give food or water'),
            ('medical', 4, 'Recovery Position', 'If breathing, place in recovery position (on their side).', 'bi-arrow-right', 'Only if no spinal injury suspected'),
            
            # Accident
            ('accident', 1, 'Ensure Safety', 'Make sure the area is safe. Turn on hazard lights.', 'bi-shield-check', 'Do not move vehicles unless absolutely necessary'),
            ('accident', 2, 'Call Emergency Services', 'Call 112 for ambulance and police.', 'bi-telephone', ''),
            ('accident', 3, 'Check for Injuries', 'Look for bleeding, broken bones, or unconsciousness.', 'bi-bandaid', 'Do not remove helmets unless necessary for breathing'),
            ('accident', 4, 'Control Bleeding', 'Apply direct pressure with clean cloth.', 'bi-droplet', 'Do not remove objects embedded in wounds'),
            
            # Fire
            ('fire', 1, 'Alert Others', 'Shout "FIRE!" to alert everyone nearby.', 'bi-megaphone', 'Do not waste time gathering belongings'),
            ('fire', 2, 'Call Fire Department', 'Call 112 immediately.', 'bi-telephone', ''),
            ('fire', 3, 'Evacuate Safely', 'Use stairs, not elevators. Stay low if there is smoke.', 'bi-arrow-down', 'Do not go back inside for any reason'),
            ('fire', 4, 'Stop, Drop, Roll', 'If clothes catch fire: Stop, Drop to ground, Roll to extinguish.', 'bi-arrow-repeat', ''),
        ]
        
        for emergency_type, step, title, instruction, icon, warning in guidance_data:
            BystanderGuidance.objects.get_or_create(
                emergency_type=emergency_type,
                step_number=step,
                defaults={
                    'title': title,
                    'instruction': instruction,
                    'icon_class': icon,
                    'warning': warning
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Created bystander guidance'))
        
        # Create area safety scores
        self.stdout.write('Creating area safety scores...')
        
        areas = [
            ('Andheri West, Mumbai', 19.1136, 72.8697, 15, 3.5),
            ('Bandra, Mumbai', 19.0596, 72.8295, 20, 2.8),
            ('Powai, Mumbai', 19.1176, 72.9060, 12, 4.2),
            ('Thane West', 19.2183, 72.9781, 10, 5.1),
            ('Navi Mumbai', 19.0330, 73.0297, 8, 6.5),
        ]
        
        for area_name, lat, lon, vol_count, avg_time in areas:
            area, created = AreaSafetyScore.objects.get_or_create(
                area_name=area_name,
                defaults={
                    'latitude': Decimal(str(lat)),
                    'longitude': Decimal(str(lon)),
                    'radius_km': 2,
                    'volunteer_count': vol_count,
                    'average_response_time_minutes': avg_time,
                    'total_emergencies': random.randint(20, 100),
                    'resolved_emergencies': random.randint(18, 95)
                }
            )
            if created:
                area.calculate_safety_score()
        
        self.stdout.write(self.style.SUCCESS('Created area safety scores'))
        
        self.stdout.write(self.style.SUCCESS('Demo data populated successfully!'))
        self.stdout.write(self.style.WARNING('Login credentials:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Citizens: citizen1-5 / demo123')
        self.stdout.write('  Volunteers: volunteer1-5 / demo123')
