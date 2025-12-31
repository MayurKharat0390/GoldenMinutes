import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME = 'admin'
EMAIL = 'admin@example.com'
PASSWORD = 'admin123'

try:
    if User.objects.filter(username=USERNAME).exists():
        print(f"User '{USERNAME}' already exists. Updating password...")
        user = User.objects.get(username=USERNAME)
        user.set_password(PASSWORD)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"✅ Password updated to: {PASSWORD}")
    else:
        print(f"Creating new superuser '{USERNAME}'...")
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f"✅ Superuser created successfully!")
        print(f"Username: {USERNAME}")
        print(f"Password: {PASSWORD}")

except Exception as e:
    print(f"❌ Error: {e}")
