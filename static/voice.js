// Speech-to-Text and Text-to-Speech for ShikshaAI
// Uses Web Speech API for both recognition and synthesis

document.addEventListener('DOMContentLoaded', function() {
    const micBtn = document.getElementById('mic-btn');
    const questionInput = document.getElementById('question-input');
    const ttsBtn = document.getElementById('tts-btn');
    const micIcon = document.getElementById('mic-icon');
    let recognizing = false;
    let recognition;

    // Debug: Check for required elements
    if (!micBtn) console.error('Mic button (mic-btn) not found!');
    if (!questionInput) console.error('Question input (question-input) not found!');
    if (!micIcon) console.error('Mic icon (mic-icon) not found!');

    // --- Speech Recognition (STT) ---
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        // Add Gujarati support
        let lang = 'en-US';
        if (window.language === 'hi') lang = 'hi-IN';
        else if (window.language === 'gu') lang = 'gu-IN';
        recognition.lang = lang;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        if (micBtn) {
            micBtn.addEventListener('click', function() {
                if (recognizing) {
                    recognition.stop();
                    return;
                }
                // Update language on each click
                let lang = 'en-US';
                if (window.language === 'hi') lang = 'hi-IN';
                else if (window.language === 'gu') lang = 'gu-IN';
                recognition.lang = lang;
                recognition.start();
            });
        }

        recognition.onstart = function() {
            recognizing = true;
            if (micIcon) micIcon.textContent = '🔴';
        };
        recognition.onend = function() {
            recognizing = false;
            if (micIcon) micIcon.textContent = '🎤';
        };
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            if (questionInput) questionInput.value = transcript;
            else console.error('questionInput is null, cannot set value.');
        };
        recognition.onerror = function(event) {
            recognizing = false;
            if (micIcon) micIcon.textContent = '🎤';
            alert((window.language === 'hi' ? 'माइक काम नहीं कर रहा है।' : (window.language === 'gu' ? 'માઇક કામ કરતો નથી.' : 'Mic is not working.')) + '\nError: ' + event.error);
            console.error('Speech recognition error:', event);
        };
    } else {
        if (micBtn) micBtn.disabled = true;
        console.error('SpeechRecognition API not supported in this browser.');
    }

    // --- Text-to-Speech (TTS) ---
    if (ttsBtn) {
        ttsBtn.addEventListener('click', function() {
            const text = window.answerText || '';
            if (!text) return;
            const utter = new SpeechSynthesisUtterance(text);
            let lang = 'en-US';
            if (window.language === 'hi') lang = 'hi-IN';
            else if (window.language === 'gu') lang = 'gu-IN';
            utter.lang = lang;
            utter.rate = 0.95;
            utter.pitch = 1.1;
            window.speechSynthesis.speak(utter);
        });
    }
}); 