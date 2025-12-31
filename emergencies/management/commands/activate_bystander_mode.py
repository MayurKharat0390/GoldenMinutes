"""
Management command to auto-activate bystander mode for unresponded emergencies
Run: python manage.py activate_bystander_mode
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from emergencies.models import Emergency, EmergencyTimeline

class Command(BaseCommand):
    help = 'Activate bystander mode for emergencies without responders after timeout'

    def handle(self, *args, **options):
        # Get timeout from settings (default 5 minutes)
        from django.conf import settings
        timeout_minutes = getattr(settings, 'EMERGENCY_TIMEOUT_MINUTES', 5)
        
        # Find emergencies that need bystander mode
        cutoff_time = timezone.now() - timedelta(minutes=timeout_minutes)
        
        emergencies = Emergency.objects.filter(
            status='active',
            primary_responder__isnull=True,
            bystander_mode_active=False,
            triggered_at__lte=cutoff_time
        )
        
        activated_count = 0
        
        for emergency in emergencies:
            # Activate bystander mode
            emergency.activate_bystander_mode()
            
            # Create timeline event
            EmergencyTimeline.objects.create(
                emergency=emergency,
                event_type='bystander_mode_activated',
                description=f'Bystander mode activated after {timeout_minutes} minutes with no responder'
            )
            
            activated_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Activated bystander mode for emergency {emergency.emergency_id}'
                )
            )
        
        if activated_count == 0:
            self.stdout.write(self.style.WARNING('No emergencies need bystander mode activation'))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Activated bystander mode for {activated_count} emergencies'
                )
            )
