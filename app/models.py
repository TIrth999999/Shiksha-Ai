from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuestionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('hi', 'Hindi'), ('gu', 'Gujarati')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question[:30]}... ({self.language})"

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('hi', 'Hindi'), ('gu', 'Gujarati')])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.language})"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.course.name})"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_image = models.ImageField(upload_to='badges/', blank=True, null=True)

    def __str__(self):
        return self.name

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # For anonymous users
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session_key', 'lesson')

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session_key', 'achievement')
