from django.db import models
from django.conf import settings
# from responders.models import badge_choices  <-- Removed

class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    video_url = models.URLField(help_text="YouTube embed link or similar", blank=True, null=True)
    video_file = models.FileField(upload_to='training_videos/', help_text="Upload MP4/WebM file directly (Recommended)", blank=True, null=True)
    content = models.TextField(help_text="Text content/study material")
    
    # Reward
    badge_id_reward = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Badge ID to award upon completion (e.g., 'cpr_certified')"
    )
    points_reward = models.IntegerField(default=100)
    
    # Metadata
    duration_minutes = models.IntegerField(default=15)
    order = models.IntegerField(default=0, help_text="Ordering in the list")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_video_embed_url(self):
        """
        Intelligently converts YouTube watch links to embed links.
        """
        if not self.video_url:
            return ""
            
        url = self.video_url
        
        # Case 1: Already an embed link
        if "embed/" in url:
            return url
            
        # Case 2: Standard Watch Link (youtube.com/watch?v=ID)
        if "watch?v=" in url:
            return url.replace("watch?v=", "embed/").split("&")[0]
            
        # Case 3: Short Link (youtu.be/ID)
        if "youtu.be/" in url:
            return url.replace("youtu.be/", "www.youtube.com/embed/")
            
        return url

class QuizQuestion(models.Model):
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField(default=0)
    
    # Options
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    
    # Correct Answer (A, B, C, or D)
    correct_option = models.CharField(
        max_length=1, 
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - Q: {self.text[:30]}"

class UserTrainingProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(help_text="Score percentage")
    
    class Meta:
        unique_together = ['user', 'module']

    def __str__(self):
        return f"{self.user.username} completed {self.module.title}"
