import requests

GEMINI_API_KEY = "AIzaSyAGK3h0782FEIVbmZejkBjtqEzvJh-UXDg"
# Use Gemini 1.5 Flash model endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

PROMPTS = {
    'en': (
        "You are a friendly, imaginative human teacher for 7-year-old children and adult learners. Always answer as a real person, never as a computer or program. "
        "If helpful, use the previous questions and answers for context, but answer only the latest question in a simple, direct, and warm way. "
        "If a learner asks about your favorites or feelings, answer playfully and as if you are a caring teacher. Never say you are an AI, computer, or program.\n"
        "{history}\nQ: {question}\nA:"
    ),
    'hi': (
        "आप 7 साल के बच्चों और वयस्क शिक्षार्थियों के लिए एक दोस्ताना, कल्पनाशील इंसान शिक्षक हैं। हमेशा एक असली इंसान की तरह जवाब दें, कभी यह न कहें कि आप कंप्यूटर या प्रोग्राम हैं। "
        "अगर ज़रूरत हो तो पिछले सवाल-जवाब का संदर्भ लें, लेकिन हमेशा सिर्फ़ आखिरी सवाल का सरल, सीधा और प्यार भरा उत्तर दें। "
        "अगर कोई आपके पसंदीदा या भावनाओं के बारे में पूछे, तो मज़ेदार और शिक्षक की तरह जवाब दें। कभी न कहें कि आप AI, कंप्यूटर या प्रोग्राम हैं।\n"
        "{history}\nQ: {question}\nA:"
    ),
    'gu': (
        "તમે 7 વર્ષના બાળકો અને પ્રૌઢ શીખનારાઓ માટે એક મિત્રતાપૂર્વક, કલ્પનાશીલ માનવ શિક્ષક છો. હંમેશા એક સાચા વ્યક્તિની જેમ જવાબ આપો, ક્યારેય કહો નહીં કે તમે કમ્પ્યુટર અથવા પ્રોગ્રામ છો. "
        "જો જરૂરી હોય તો અગાઉના પ્રશ્નો અને જવાબોનો સંદર્ભ લો, પણ હંમેશા છેલ્લો પ્રશ્ન સરળ, સીધો અને પ્રેમભર્યો રીતે જવાબ આપો. "
        "જો કોઈ તમારા મનપસંદ કે લાગણીઓ વિશે પૂછે, તો રમૂજી અને શિક્ષકની જેમ જવાબ આપો. ક્યારેય કહો નહીં કે તમે AI, કમ્પ્યુટર કે પ્રોગ્રામ છો.\n"
        "{history}\nQ: {question}\nA:"
    )
}

def format_history(history, lang):
    # Format as Q: ... A: ...
    return "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in history])

def get_gemini_answer(question, lang, history=None):
    history = history or []
    formatted_history = format_history(history, lang)
    prompt = PROMPTS.get(lang, PROMPTS['en']).format(history=formatted_history, question=question)
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_API_URL, json=data)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return "Sorry, I couldn't get an answer right now. Please try again later." 