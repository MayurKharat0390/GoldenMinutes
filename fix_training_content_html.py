import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule

def fix_content():
    # 1. Fix CPR
    try:
        cpr = TrainingModule.objects.get(slug='cpr-basics')
        cpr.content = """
        <p class="lead">Cardiopulmonary resuscitation (CPR) is a lifesaving technique useful in many emergencies, including a heart attack or near drowning, in which someone's breathing or heartbeat has stopped.</p>
        
        <ol class="list-group list-group-numbered list-group-flush mb-3">
            <li class="list-group-item">
                <strong>Check the scene</strong> for safety, form an initial impression, and use personal protective equipment (PPE).
            </li>
            <li class="list-group-item">
                If the person appears unresponsive, <strong>check for responsiveness</strong>, breathing, life-threatening bleeding or other life-threatening conditions using shout-tap-shout.
            </li>
            <li class="list-group-item">
                If the person generally does not respond and is not breathing or only gasping, <strong>CALL 9-1-1</strong> (or local emergency) and get equipment, or tell someone to do so.
            </li>
            <li class="list-group-item">
                <strong>Give 30 Chest Compressions</strong>. <br>
                <small class="text-muted">Hand position: Two hands centered on the chest. Body position: Shoulders directly over hands; elbows locked. Depth: At least 2 inches. Rate: 100 to 120 per minute.</small>
            </li>
            <li class="list-group-item">
                <strong>Give 2 Breaths</strong>. <br>
                <small class="text-muted">Open the airway to a past-neutral position using the head-tilt/chin-lift technique. Ensure each breath lasts about 1 second and makes the chest rise; allow air to exit before giving the next breath.</small>
            </li>
        </ol>
        """
        cpr.save()
        print("✅ CPR Content converted to HTML.")
    except TrainingModule.DoesNotExist:
        pass

    # 2. Fix First Aid
    try:
        fa = TrainingModule.objects.get(slug='first-aid-101')
        fa.content = """
        <div class="vstack gap-4">
            <div>
                <h4 class="text-danger"><i class="bi bi-droplet-fill me-2"></i>1. Severe Bleeding</h4>
                <ul class="mb-0">
                    <li><strong>Apply direct pressure</strong> on the wound with a sterile bandage or clean cloth.</li>
                    <li><strong>Elevate</strong> the injured part above the heart if possible.</li>
                    <li><strong>Do not remove</strong> the cloth if it soaks through; add more layers on top.</li>
                </ul>
            </div>

            <div>
                <h4 class="text-warning"><i class="bi bi-fire me-2"></i>2. Burns</h4>
                <ul class="mb-0">
                    <li><strong>Cool the burn</strong> under cool (not cold) running water for at least 10 minutes.</li>
                    <li><strong>Cover</strong> loosely with a sterile, non-stick bandage.</li>
                    <li><strong>Do not</strong> apply ice, butter, or ointments to a severe burn.</li>
                </ul>
            </div>

            <div>
                <h4 class="text-primary"><i class="bi bi-bandaid mb-2 me-2"></i>3. Fractures</h4>
                <ul class="mb-0">
                    <li><strong>Immobilize</strong> the injured area. Do not try to realign the bone.</li>
                    <li><strong>Apply ice packs</strong> wrapped in a cloth to reduce swelling.</li>
                    <li><strong>Treat for shock</strong>: lay the person down and keep them warm.</li>
                </ul>
            </div>
        </div>
        """
        fa.save()
        print("✅ First Aid Content converted to HTML.")
    except TrainingModule.DoesNotExist:
        pass

if __name__ == '__main__':
    fix_content()
