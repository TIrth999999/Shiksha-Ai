// Speech-to-Text and Text-to-Speech for ShikshaAI
// Uses Web Speech API for both recognition and synthesis

document.addEventListener('DOMContentLoaded', function() {
    const micBtn = document.getElementById('mic-btn');
    const questionInput = document.getElementById('question-input');
    const ttsBtn = document.getElementById('tts-btn');
    let recognizing = false;
    let recognition;

    // --- Speech Recognition (STT) ---
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = window.language === 'hi' ? 'hi-IN' : 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        micBtn && micBtn.addEventListener('click', function() {
            if (recognizing) {
                recognition.stop();
                return;
            }
            recognition.lang = window.language === 'hi' ? 'hi-IN' : 'en-US';
            recognition.start();
        });

        recognition.onstart = function() {
            recognizing = true;
            document.getElementById('mic-icon').textContent = '🔴';
        };
        recognition.onend = function() {
            recognizing = false;
            document.getElementById('mic-icon').textContent = '🎤';
        };
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            questionInput.value = transcript;
        };
        recognition.onerror = function(event) {
            recognizing = false;
            document.getElementById('mic-icon').textContent = '🎤';
            alert(window.language === 'hi' ? 'माइक काम नहीं कर रहा है।' : 'Mic is not working.');
        };
    } else {
        micBtn && (micBtn.disabled = true);
    }

    // --- Text-to-Speech (TTS) ---
    if (ttsBtn) {
        ttsBtn.addEventListener('click', function() {
            const text = window.answerText || '';
            if (!text) return;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = window.language === 'hi' ? 'hi-IN' : 'en-US';
            utter.rate = 0.95;
            utter.pitch = 1.1;
            window.speechSynthesis.speak(utter);
        });
    }
}); 