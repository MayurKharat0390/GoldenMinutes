from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrainingModule, QuizQuestion, UserTrainingProgress
from responders.models import ResponderStats

@login_required
def training_list(request):
    modules = TrainingModule.objects.all()
    # Check progress for each
    completed_ids = UserTrainingProgress.objects.filter(user=request.user).values_list('module_id', flat=True)
    
    return render(request, 'training/list.html', {
        'modules': modules,
        'completed_ids': completed_ids
    })

@login_required
def training_detail(request, slug):
    module = get_object_or_404(TrainingModule, slug=slug)
    
    # Check if already completed
    progress = UserTrainingProgress.objects.filter(user=request.user, module=module).first()
    
    questions = module.questions.all()
    
    return render(request, 'training/detail.html', {
        'module': module,
        'questions': questions,
        'progress': progress
    })

@login_required
def submit_quiz(request, slug):
    if request.method != 'POST':
        return redirect('training:detail', slug=slug)
        
    module = get_object_or_404(TrainingModule, slug=slug)
    questions = module.questions.all()
    total_questions = questions.count()
    
    if total_questions == 0:
        messages.error(request, "This module has no quiz questions.")
        return redirect('training:list')
        
    score = 0
    
    for q in questions:
        user_answer = request.POST.get(f'question_{q.id}')
        if user_answer == q.correct_option:
            score += 1
            
    percentage = (score / total_questions) * 100
    PASSING_SCORE = 70.0
    
    if percentage >= PASSING_SCORE:
        # Save Progress
        obj, created = UserTrainingProgress.objects.get_or_create(
            user=request.user,
            module=module,
            defaults={'score': int(percentage)}
        )
        
        if created or obj.score < percentage:
            obj.score = int(percentage)
            obj.save()
            
        # Award Badge if applicable
        if module.badge_id_reward:
            stats, _ = ResponderStats.objects.get_or_create(responder=request.user)
            awarded = stats.earn_badge(module.badge_id_reward, module.points_reward)
            
            if awarded:
                messages.success(request, f"🎉 You passed! Badge earned: {module.badge_id_reward}")
            else:
                messages.success(request, f"🎉 You passed with {int(percentage)}%!")
        else:
            messages.success(request, f"🎉 You passed with {int(percentage)}%!")
            
    else:
        messages.warning(request, f"You got {int(percentage)}%. You need {int(PASSING_SCORE)}% to pass. Try again!")
        
    return redirect('training:detail', slug=slug)
