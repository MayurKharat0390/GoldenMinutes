import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule, QuizQuestion

def populate_first_aid():
    print("🚑 Updating First Aid 101...")
    
    # 1. Update Module Details
    fa, created = TrainingModule.objects.get_or_create(slug='first-aid-101')
    
    fa.title = 'First Aid 101: Bleeding & Burns'
    fa.description = 'Learn how to treat severe bleeding, burns, and fractures while waiting for emergency services.'
    # Wikimedia Commons: Bandaging a bleeding wound (MP4 H.264)
    fa.video_url = 'https://upload.wikimedia.org/wikipedia/commons/transcoded/d/d6/Bandaging_a_bleeding_wound.webm/Bandaging_a_bleeding_wound.webm.480p.h264.mp4'
    fa.content = """**1. Severe Bleeding**
- **Apply direct pressure** on the wound with a sterile bandage or clean cloth.
- **Elevate** the injured part above the heart if possible.
- **Do not remove** the cloth if it soaks through; add more layers on top.

**2. Burns**
- **Cool the burn** under cool (not cold) running water for at least 10 minutes.
- **Cover** loosely with a sterile, non-stick bandage.
- **Do not** apply ice, butter, or ointments to a severe burn.

**3. Fractures**
- **Immobilize** the injured area. Do not try to realign the bone.
- **Apply ice packs** wrapped in a cloth to reduce swelling.
- **Treat for shock**: lay the person down and keep them warm."""
    fa.badge_id_reward = 'first_aid_expert'
    fa.points_reward = 150
    fa.duration_minutes = 20
    fa.save()
    
    print("✅ Content Updated.")

    # 2. Add Questions (Clear existing first)
    fa.questions.all().delete()
    
    questions = [
        {
            'text': 'What is the first step to control severe bleeding?',
            'a': 'Apply a tourniquet immediately',
            'b': 'Apply direct pressure with a clean cloth',
            'c': 'Wash the wound with soap',
            'd': 'Apply ice directly to the wound',
            'correct': 'B'
        },
        {
            'text': 'How should you treat a minor burn immediately?',
            'a': 'Apply butter or oil',
            'b': 'Cover it with ice',
            'c': 'Run cool water over it for 10 minutes',
            'd': 'Pop any blisters that form',
            'correct': 'C'
        },
        {
            'text': 'If a bandage soaks through with blood, what should you do?',
            'a': 'Remove it and put a fresh one on',
            'b': 'Add more layers on top of it',
            'c': 'Wash the wound',
            'd': 'Stop applying pressure',
            'correct': 'B'
        }
    ]
    
    for idx, q in enumerate(questions):
        QuizQuestion.objects.create(
            module=fa,
            text=q['text'],
            option_a=q['a'],
            option_b=q['b'],
            option_c=q['c'],
            option_d=q['d'],
            correct_option=q['correct'],
            order=idx
        )
        
    print(f"✅ Added {len(questions)} quiz questions.")

if __name__ == '__main__':
    populate_first_aid()
