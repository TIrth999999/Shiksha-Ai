from django.contrib import admin
from .models import QuestionHistory, Course, Lesson, Achievement, UserProgress, UserAchievement

admin.site.register(QuestionHistory)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Achievement)
admin.site.register(UserProgress)
admin.site.register(UserAchievement)
