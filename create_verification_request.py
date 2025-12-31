import os
import django
from django.core.files.base import ContentFile
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from django.contrib.auth import get_user_model
from responders.models import VolunteerProfile

User = get_user_model()

def create_request():
    username = "candidate_jane"
    email = "jane@example.com"
    
    # 1. Create User
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password("password123")
        user.save()
        print(f"👤 Created user: {username}")
    else:
        print(f"👤 User {username} exists.")

    # 2. Update Profile
    profile, _ = VolunteerProfile.objects.get_or_create(user=user)
    
    # Simulate pending request
    profile.verification_status = 'pending'
    profile.role_level = 'medical_professional'
    
    # Create fake ID image
    if not profile.id_document:
        # A simple 1x1 pixel image
        profile.id_document.save('fake_id_card.jpg', ContentFile(b'\x00'), save=False)
    
    # Create fake Cert image
    if not profile.certification:
         profile.certification.save('fake_cert.jpg', ContentFile(b'\x00'), save=False)
         
    profile.save()
    print("✅ Created PENDING verification request for Jane.")
    
    # Another one
    username2 = "medic_mike"
    user2, _ = User.objects.get_or_create(username=username2, defaults={'email': 'mike@example.com'})
    user2.set_password("password123")
    user2.save()
    
    prof2, _ = VolunteerProfile.objects.get_or_create(user=user2)
    prof2.verification_status = 'pending'
    prof2.role_level = 'EMT'
    prof2.save()
    print("✅ Created PENDING verification request for Mike (No Docs).")

if __name__ == '__main__':
    create_request()
