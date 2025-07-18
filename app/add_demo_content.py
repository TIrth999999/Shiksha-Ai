import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShikshaAi.settings')
django.setup()

from app.models import Course, Lesson, Achievement

# Data for all languages
languages = ['en', 'hi', 'gu']
course_name = "First Step"
course_desc = "Your first course to get started!"

alphabets_content = {
    'en': '''<b>What are Alphabets?</b><br>
Alphabets are the letters we use to make words. In English, there are 26 letters: A, B, C, ... Z.<br><br>
<b>How to pronounce?</b><br>
Each letter has its own sound: <br>
A (ay), B (bee), C (see), ...<br><br>
<b>What do they look like?</b><br>
A, B, C, D, E, F, G, ... Z<br><br>
<b>Fun Fact:</b> The English alphabet has 5 vowels (A, E, I, O, U) and 21 consonants!''',
    'hi': '''<b>क्या हैं वर्णमाला?</b><br>
वर्णमाला वे अक्षर हैं जिनसे शब्द बनते हैं। हिंदी में 13 स्वर (अ, आ, इ, ई, ...) और 33 व्यंजन (क, ख, ग, घ, ...) होते हैं।<br><br>
<b>कैसे बोलें?</b><br>
हर अक्षर का उच्चारण अलग होता है: <br>
अ (a), आ (aa), इ (i), ई (ee), ...<br><br>
<b>कैसे दिखते हैं?</b><br>
अ, आ, इ, ई, उ, ऊ, ऋ, ए, ऐ, ओ, औ, क, ख, ग, घ, ...<br><br>
<b>मज़ेदार तथ्य:</b> हिंदी वर्णमाला में कुल 46 अक्षर होते हैं!''',
    'gu': '''<b>અક્ષરો શું છે?</b><br>
અક્ષરો એ એવા ચિહ્નો છે, જેનાથી શબ્દો બને છે. ગુજરાતી ભાષામાં 13 સ્વર (અ, આ, ઇ, ઈ, ...) અને 36 વ્યંજન (ક, ખ, ગ, ઘ, ...) છે.<br><br>
<b>કેવી રીતે બોલવું?</b><br>
દરેક અક્ષરનો ઉચ્ચાર અલગ છે:<br>
અ (a), આ (aa), ઇ (i), ઈ (ee), ...<br><br>
<b>કેવી રીતે દેખાય છે?</b><br>
અ, આ, ઇ, ઈ, ઉ, ઊ, ઋ, એ, ઐ, ઓ, ઔ, ક, ખ, ગ, ઘ, ...<br><br>
<b>મજા ની વાત:</b> ગુજરાતી લિપિમાં કુલ 49 અક્ષરો છે!'''
}

numbers_content = {
    'en': '''<b>What are Numbers?</b><br>
Numbers are the digits we use to count and do math.<br><br>
<b>How to count?</b><br>
0 (zero), 1 (one), 2 (two), 3 (three), 4 (four), 5 (five), 6 (six), 7 (seven), 8 (eight), 9 (nine)<br><br>
<b>Basic Math:</b><br>
- <b>Addition</b>: 2 + 3 = 5<br>
- <b>Subtraction</b>: 5 - 2 = 3<br>
- <b>Multiplication</b>: 2 × 3 = 6<br>
- <b>Division</b>: 6 ÷ 2 = 3<br><br>
<b>Fun Fact:</b> The number 0 (zero) was invented in India!''',
    'hi': '''<b>संख्या क्या हैं?</b><br>
संख्या वे अंक हैं जिनसे हम गिनती और गणना करते हैं।<br><br>
<b>कैसे गिनें?</b><br>
० (शून्य), १ (एक), २ (दो), ३ (तीन), ४ (चार), ५ (पाँच), ६ (छह), ७ (सात), ८ (आठ), ९ (नौ)<br><br>
<b>मूल गणित:</b><br>
- <b>जोड़ना</b>: २ + ३ = ५<br>
- <b>घटाना</b>: ५ - २ = ३<br>
- <b>गुणा</b>: २ × ३ = ६<br>
- <b>भाग</b>: ६ ÷ २ = ३<br><br>
<b>मज़ेदार तथ्य:</b> ० (शून्य) भारत की देन है!''',
    'gu': '''<b>સંખ્યા શું છે?</b><br>
સંખ્યા એ અંક છે, જેના દ્વારા આપણે ગણતરી કરીએ છીએ.<br><br>
<b>કેવી રીતે ગણવું?</b><br>
૦ (શૂન્ય), ૧ (એક), ૨ (બે), ૩ (ત્રણ), ૪ (ચાર), ૫ (પાંચ), ૬ (છ), ૭ (સાત), ૮ (આઠ), ૯ (નવ)<br><br>
<b>મૂળભૂત ગણિત:</b><br>
- <b>ઉમેરો</b>: ૨ + ૩ = ૫<br>
- <b>બાદબાકી</b>: ૫ - ૨ = ૩<br>
- <b>ગુણાકાર</b>: ૨ × ૩ = ૬<br>
- <b>ભાગાકાર</b>: ૬ ÷ ૨ = ૩<br><br>
<b>મજા ની વાત:</b> ૦ (શૂન્ય) ભારતે શોધ્યું હતું!'''
}

# Achievements
achievements = [
    ("First Lesson Complete", "Completed your first lesson!"),
    ("Course Finisher", "Completed all lessons in a course!"),
    ("First Time Asks", "Asked your first question to the AI!"),
    ("Streak Starter", "Completed lessons on two consecutive days!")
]

# Create courses and lessons
for lang in languages:
    course, _ = Course.objects.get_or_create(name=course_name, language=lang, defaults={"description": course_desc, "order": 1})
    Lesson.objects.get_or_create(course=course, title="Alphabets", defaults={"content": alphabets_content[lang], "order": 1})
    Lesson.objects.get_or_create(course=course, title="Numbers", defaults={"content": numbers_content[lang], "order": 2})

# Create achievements
for name, desc in achievements:
    Achievement.objects.get_or_create(name=name, defaults={"description": desc})

print("Demo content added for all languages.") 