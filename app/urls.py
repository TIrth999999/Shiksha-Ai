from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('learn/', views.learn, name='learn'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('achievements/', views.achievements, name='achievements'),
    path('award-badge/', views.award_badge, name='award_badge'),
    path('delete-history/<int:pk>/', views.delete_history, name='delete_history'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
]