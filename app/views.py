from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from .models import QuestionHistory, Course, Lesson, Achievement, UserProgress, UserAchievement
from .ai_utils import get_gemini_answer
from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate

LANGUAGES = {'en': 'English', 'hi': 'Hindi', 'gu': 'Gujarati'}

@login_required
def home(request):
    return redirect('dashboard')

@login_required
def learn(request):
    lang = request.session.get('language', 'en')
    translation.activate(lang)
    answer = None
    question = None
    # Get last 5 Q&A for context, in chronological order
    history_qs = QuestionHistory.objects.filter(user=request.user, language=lang).order_by('-timestamp')[:5]
    history_list = [
        {'question': h.question, 'answer': h.answer}
        for h in reversed(history_qs)
    ]
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            answer = get_gemini_answer(question, lang, history=history_list)
            QuestionHistory.objects.create(user=request.user, question=question, answer=answer, language=lang)
    # For display, show last 10
    display_history = QuestionHistory.objects.filter(user=request.user, language=lang).order_by('-timestamp')[:10]
    return render(request, 'learn.html', {
        'language': lang,
        'languages': LANGUAGES,
        'answer': answer,
        'question': question,
        'history': display_history,
    })

@login_required
def courses(request):
    lang = request.session.get('language', 'en')
    translation.activate(lang)
    course_list = Course.objects.filter(language=lang).order_by('order')
    user = request.user if request.user.is_authenticated else None
    completed_course_ids = set()
    for course in course_list:
        lessons = list(course.lessons.all())
        if lessons:
            completed_count = UserProgress.objects.filter(user=user, completed=True, lesson__course=course).count()
            if completed_count == len(lessons):
                completed_course_ids.add(course.id)
    return render(request, 'courses.html', {
        'courses': course_list,
        'language': lang,
        'languages': LANGUAGES,
        'completed_course_ids': completed_course_ids,
    })

@login_required
def course_detail(request, course_id):
    lang = request.session.get('language', 'en')
    translation.activate(lang)
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    user = request.user if request.user.is_authenticated else None
    completed_ids = set(UserProgress.objects.filter(user=user, lesson__course=course, completed=True).values_list('lesson_id', flat=True))
    return render(request, 'course_detail.html', {
        'course': course,
        'lessons': lessons,
        'completed_ids': completed_ids,
        'language': lang,
        'languages': LANGUAGES,
    })

def get_lesson_content(lesson, lang):
    # Language-aware content for alphabets and numbers
    if lesson.title.lower() == 'alphabets':
        if lang == 'hi':
            return """
<b>क्या हैं वर्णमाला?</b><br>
वर्णमाला वे अक्षर हैं जिनसे शब्द बनते हैं। हिंदी में 13 स्वर (अ, आ, इ, ई, ...) और 33 व्यंजन (क, ख, ग, घ, ...) होते हैं।<br><br>
<b>कैसे बोलें?</b><br>
हर अक्षर का उच्चारण अलग होता है: <br>
अ (a), आ (aa), इ (i), ई (ee), ...<br><br>
<b>कैसे दिखते हैं?</b><br>
अ, आ, इ, ई, उ, ऊ, ऋ, ए, ऐ, ओ, औ, क, ख, ग, घ, ...<br><br>
<b>मज़ेदार तथ्य:</b> हिंदी वर्णमाला में कुल 46 अक्षर होते हैं!
"""
        elif lang == 'gu':
            return """
<b>અક્ષરો શું છે?</b><br>
અક્ષરો એ એવા ચિહ્નો છે, જેનાથી શબ્દો બને છે. ગુજરાતી ભાષામાં 13 સ્વર (અ, આ, ઇ, ઈ, ...) અને 36 વ્યંજન (ક, ખ, ગ, ઘ, ...) છે.<br><br>
<b>કેવી રીતે બોલવું?</b><br>
દરેક અક્ષરનો ઉચ્ચાર અલગ છે:<br>
અ (a), આ (aa), ઇ (i), ઈ (ee), ...<br><br>
<b>કેવી રીતે દેખાય છે?</b><br>
અ, આ, ઇ, ઈ, ઉ, ઊ, ઋ, એ, ઐ, ઓ, ઔ, ક, ખ, ગ, ઘ, ...<br><br>
<b>મજા ની વાત:</b> ગુજરાતી લિપિમાં કુલ 49 અક્ષરો છે!
"""
        else:
            return """
<b>What are Alphabets?</b><br>
Alphabets are the letters we use to make words. In English, there are 26 letters: A, B, C, ... Z.<br><br>
<b>How to pronounce?</b><br>
Each letter has its own sound: <br>
A (ay), B (bee), C (see), ...<br><br>
<b>What do they look like?</b><br>
A, B, C, D, E, F, G, ... Z<br><br>
<b>Fun Fact:</b> The English alphabet has 5 vowels (A, E, I, O, U) and 21 consonants!
"""
    elif lesson.title.lower() == 'numbers':
        if lang == 'hi':
            return """
<b>संख्या क्या हैं?</b><br>
संख्या वे अंक हैं जिनसे हम गिनती और गणना करते हैं।<br><br>
<b>कैसे गिनें?</b><br>
० (शून्य), १ (एक), २ (दो), ३ (तीन), ४ (चार), ५ (पाँच), ६ (छह), ७ (सात), ८ (आठ), ९ (नौ)<br><br>
<b>मूल गणित:</b><br>
- <b>जोड़ना</b>: २ + ३ = ५<br>
- <b>घटाना</b>: ५ - २ = ३<br>
- <b>गुणा</b>: २ × ३ = ६<br>
- <b>भाग</b>: ६ ÷ २ = ३<br><br>
<b>मज़ेदार तथ्य:</b> ० (शून्य) भारत की देन है!
"""
        elif lang == 'gu':
            return """
<b>સંખ્યા શું છે?</b><br>
સંખ્યા એ અંક છે, જેના દ્વારા આપણે ગણતરી કરીએ છીએ.<br><br>
<b>કેવી રીતે ગણવું?</b><br>
૦ (શૂન્ય), ૧ (એક), ૨ (બે), ૩ (ત્રણ), ૪ (ચાર), ૫ (પાંચ), ૬ (છ), ૭ (સાત), ૮ (આઠ), ૯ (નવ)<br><br>
<b>મૂળભૂત ગણિત:</b><br>
- <b>ઉમેરો</b>: ૨ + ૩ = ૫<br>
- <b>બાદબાકી</b>: ૫ - ૨ = ૩<br>
- <b>ગુણાકાર</b>: ૨ × ૩ = ૬<br>
- <b>ભાગાકાર</b>: ૬ ÷ ૨ = ૩<br><br>
<b>મજા ની વાત:</b> ૦ (શૂન્ય) ભારતે શોધ્યું હતું!
"""
        else:
            return """
<b>What are Numbers?</b><br>
Numbers are the digits we use to count and do math.<br><br>
<b>How to count?</b><br>
0 (zero), 1 (one), 2 (two), 3 (three), 4 (four), 5 (five), 6 (six), 7 (seven), 8 (eight), 9 (nine)<br><br>
<b>Basic Math:</b><br>
- <b>Addition</b>: 2 + 3 = 5<br>
- <b>Subtraction</b>: 5 - 2 = 3<br>
- <b>Multiplication</b>: 2 × 3 = 6<br>
- <b>Division</b>: 6 ÷ 2 = 3<br><br>
<b>Fun Fact:</b> The number 0 (zero) was invented in India!
"""
    else:
        return lesson.content

@login_required
def lesson_detail(request, lesson_id):
    lang = request.session.get('language', 'en')
    translation.activate(lang)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    answer = None
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key or request.session.save() or request.session.session_key
    lessons = list(course.lessons.all())
    idx = lessons.index(lesson)
    if idx > 0:
        prev_lesson = lessons[idx-1]
        prev_completed = UserProgress.objects.filter(
            user=user, session_key=None, lesson=prev_lesson, completed=True
        ).exists()
        if not user:
            prev_completed = UserProgress.objects.filter(
                user=None, session_key=session_key, lesson=prev_lesson, completed=True
            ).exists()
        if not prev_completed:
            return redirect('lesson_detail', lesson_id=prev_lesson.id)
    else:
        prev_lesson = None
    next_lesson = lessons[idx+1] if idx+1 < len(lessons) else None
    achievement_unlocked = None
    if request.method == 'POST':
        if 'complete' in request.POST:
            up, created = UserProgress.objects.get_or_create(
                user=user, session_key=None if user else session_key, lesson=lesson,
                defaults={'completed': True, 'timestamp': timezone.now()}
            )
            if created:
                up.completed = True
                up.save()
            total = course.lessons.count()
            done = UserProgress.objects.filter(
                user=user, session_key=None if user else session_key, lesson__course=course, completed=True
            ).count()
            if total == done:
                ach = Achievement.objects.filter(name__icontains='Course Finisher').first()
                print(f'Checking Course Finisher achievement for user={user}, session={session_key}, ach={ach}')
                if ach:
                    ua, created = UserAchievement.objects.get_or_create(user=user, session_key=None if user else session_key, achievement=ach)
                    print(f'Course Finisher achievement created={created}')
                    if created:
                        request.session['achievement_unlocked'] = ach.name
        elif 'ask_ai' in request.POST:
            question = request.POST.get('question')
            if question:
                answer = get_gemini_answer(question, lang)
                ach = Achievement.objects.filter(name__icontains='First Time Asks').first()
                print(f'Checking First Time Asks achievement for user={user}, session={session_key}, ach={ach}')
                if ach and not UserAchievement.objects.filter(user=user, session_key=None if user else session_key, achievement=ach).exists():
                    UserAchievement.objects.create(user=user, session_key=None if user else session_key, achievement=ach)
                    print('First Time Asks achievement created')
                    request.session['achievement_unlocked'] = ach.name
    # Check for achievement unlocked in session
    if 'achievement_unlocked' in request.session:
        achievement_unlocked = request.session['achievement_unlocked']
        del request.session['achievement_unlocked']
    lesson_content = get_lesson_content(lesson, lang)
    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'lesson_content': lesson_content,
        'answer': answer,
        'language': lang,
        'languages': LANGUAGES,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'achievement_unlocked': achievement_unlocked,
    })

@login_required
def achievements(request):
    lang = request.session.get('language', 'en')
    translation.activate(lang)
    # Show all achievements and user's earned ones
    all_achievements = Achievement.objects.all()
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key or request.session.save() or request.session.session_key
    user_achievements = UserAchievement.objects.filter(user=user, session_key=None)
    if not user:
        user_achievements = UserAchievement.objects.filter(user=None, session_key=session_key)
    earned_ids = set(ua.achievement_id for ua in user_achievements)
    return render(request, 'achievements.html', {
        'achievements': all_achievements,
        'earned_ids': earned_ids,
        'language': lang,
        'languages': LANGUAGES,
    })

@login_required
def dashboard(request):
    lang = request.session.get('language', 'en')
    translation.activate(lang)
    return render(request, 'dashboard.html', {'language': lang, 'languages': LANGUAGES})

@login_required
def profile(request):
    lang = request.session.get('language', 'en')
    if request.method == 'POST':
        new_lang = request.POST.get('language', lang)
        request.session['language'] = new_lang
        translation.activate(new_lang)
        return redirect('profile')
    translation.activate(lang)
    return render(request, 'profile.html', {'language': lang, 'languages': LANGUAGES})

def award_badge(request):
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        data = json.loads(request.body.decode('utf-8'))
        badge_name = (data.get('badge') or '').strip().lower()
        print('Award badge request for:', badge_name)
        session_key = request.session.session_key or request.session.save() or request.session.session_key
        user = request.user if request.user.is_authenticated else None
        ach = Achievement.objects.filter(name__iexact=badge_name).first() or Achievement.objects.filter(name__icontains=badge_name).first()
        print('Achievement found:', ach)
        if ach and not UserAchievement.objects.filter(user=user, session_key=None if user else session_key, achievement=ach).exists():
            UserAchievement.objects.create(user=user, session_key=None if user else session_key, achievement=ach)
            print('Achievement created for user/session')
            return JsonResponse({'status': 'awarded'})
        print('Achievement already earned or not found')
        return JsonResponse({'status': 'already-earned'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_history(request, pk):
    lang = request.session.get('language', 'en')
    session_key = request.session.session_key or request.session.save() or request.session.session_key
    # Only allow deletion of user's/session's own history
    try:
        entry = QuestionHistory.objects.get(pk=pk, language=lang)
        entry.delete()
    except QuestionHistory.DoesNotExist:
        pass
    return redirect('learn')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('courses')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    lang = request.session.get('language', 'en')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('courses')
    else:
        form = AuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form, 'language': lang, 'languages': LANGUAGES})