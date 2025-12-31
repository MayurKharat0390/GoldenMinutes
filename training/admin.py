from django.contrib import admin
from .models import TrainingModule, QuizQuestion, UserTrainingProgress

class QuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1

@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'badge_id_reward', 'points_reward', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [QuestionInline]

@admin.register(UserTrainingProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'score', 'completed_at')
    list_filter = ('module', 'completed_at')
