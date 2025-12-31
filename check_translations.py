import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from emergencies.models import BystanderGuidance

print("=" * 60)
print("CHECKING BYSTANDER GUIDANCE TRANSLATIONS")
print("=" * 60)

# Check English
english_steps = BystanderGuidance.objects.filter(emergency_type='medical', language='en')
print(f"\n✓ English steps: {english_steps.count()}")
if english_steps.exists():
    print(f"  Example: {english_steps.first().title}")

# Check Hindi
hindi_steps = BystanderGuidance.objects.filter(emergency_type='medical', language='hi')
print(f"\n✓ Hindi steps: {hindi_steps.count()}")
if hindi_steps.exists():
    print(f"  Example: {hindi_steps.first().title}")
else:
    print("  ⚠️ NO HINDI TRANSLATIONS FOUND!")

# Check Marathi
marathi_steps = BystanderGuidance.objects.filter(emergency_type='medical', language='mr')
print(f"\n✓ Marathi steps: {marathi_steps.count()}")
if marathi_steps.exists():
    print(f"  Example: {marathi_steps.first().title}")
else:
    print("  ⚠️ NO MARATHI TRANSLATIONS FOUND!")

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("=" * 60)

if hindi_steps.count() == 0:
    print("\n❌ PROBLEM: No Hindi translations in database!")
    print("   SOLUTION: Run 'python add_bystander_translations.py'")
elif hindi_steps.count() < 6:
    print(f"\n⚠️ WARNING: Only {hindi_steps.count()} Hindi steps (should be 6)")
else:
    print("\n✅ Hindi translations exist in database")
    print("\nIf voice is still in English, the issue is:")
    print("1. Browser doesn't have Hindi voice installed")
    print("2. Browser is using English voice to read Hindi text")
    print("\nTo fix:")
    print("- Chrome: Settings → Languages → Add Hindi")
    print("- Windows: Settings → Time & Language → Speech → Add Hindi voice")

print("\n" + "=" * 60)
