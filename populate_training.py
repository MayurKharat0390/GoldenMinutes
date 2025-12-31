import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

from training.models import TrainingModule, QuizQuestion

def create_training_content():
    # 1. CPR Basics
    print("Creating CPR Basics Module...")
    cpr, created = TrainingModule.objects.get_or_create(
        slug='cpr-basics',
        defaults={
            'title': 'CPR Basics Certification',
            'description': 'Learn the fundamentals of Cardiopulmonary Resuscitation (CPR) and how to save a life during cardiac arrest.',
            'video_url': 'https://www.youtube.com/embed/-Xc8v2183eA', # Random placeholder or real CPR video
            'content': """Cardiopulmonary resuscitation (CPR) is a lifesaving technique useful in many emergencies, including a heart attack or near drowning, in which someone's breathing or heartbeat has stopped.

1. **Check the scene** for safety, form an initial impression, and use personal protective equipment (PPE).
2. If the person appears unresponsive, **check for responsiveness**, breathing, life-threatening bleeding or other life-threatening conditions using shout-tap-shout.
3. If the person generally does not respond and is not breathing or only gasping, **CALL 9-1-1** and get equipment, or tell someone to do so.
4. **Give 30 Chest Compressions**. Hand position: Two hands centered on the chest. Body position: Shoulders directly over hands; elbows locked. Depth: At least 2 inches. Rate: 100 to 120 per minute.
5. **Give 2 Breaths**. Open the airway to a past-neutral position using the head-tilt/chin-lift technique. Ensure each breath lasts about 1 second and makes the chest rise; allow air to exit before giving the next breath.
""",
            'badge_id_reward': 'cpr_certified',
            'points_reward': 200,
            'duration_minutes': 15
        }
    )
    
    if created:
        print("✅ Module Created!")
        
        # Questions
        questions = [
            {
                'text': 'What is the correct ratio of chest compressions to breaths in CPR?',
                'a': '15 compressions : 1 breath',
                'b': '30 compressions : 2 breaths',
                'c': '50 compressions : 5 breaths',
                'd': '10 compressions : 2 breaths',
                'correct': 'B'
            },
            {
                'text': 'What is the recommended rate of chest compressions per minute?',
                'a': '60-80',
                'b': '80-100',
                'c': '100-120',
                'd': '120-140',
                'correct': 'C'
            },
            {
                'text': 'How deep should you compress the chest for an adult?',
                'a': 'At least 1 inch',
                'b': 'At least 2 inches',
                'c': 'Exactly 3 inches',
                'd': 'Depth does not matter',
                'correct': 'B'
            }
        ]
        
        for idx, q in enumerate(questions):
            QuizQuestion.objects.create(
                module=cpr,
                text=q['text'],
                option_a=q['a'],
                option_b=q['b'],
                option_c=q['c'],
                option_d=q['d'],
                correct_option=q['correct'],
                order=idx
            )
        print(f"✅ Added {len(questions)} questions.")
    else:
        print("ℹ️ Module already exists.")

    # 2. First Aid 101 (Placeholder)
    fa, created = TrainingModule.objects.get_or_create(
        slug='first-aid-101',
        defaults={
            'title': 'First Aid 101',
            'description': 'Essential first aid skills for treating bleeding, burns, and fractures.',
            'content': 'Coming soon...',
            'badge_id_reward': 'first_aid_expert',
            'points_reward': 150,
            'duration_minutes': 20
        }
    )
    if created:
        print("✅ First Aid Module Created!")

if __name__ == '__main__':
    create_training_content()
