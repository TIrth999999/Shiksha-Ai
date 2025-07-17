// Speech-to-Text and Text-to-Speech for ShikshaAI
// Uses Web Speech API for both recognition and synthesis

document.addEventListener('DOMContentLoaded', function() {
    const micBtn = document.getElementById('mic-btn');
    const questionInput = document.getElementById('question-input');
    const ttsBtn = document.getElementById('tts-btn');
    const micIcon = document.getElementById('mic-icon');
    let recognizing = false;
    let recognition;

    // Add a visible error message area
    function ensureErrorArea() {
        let errorArea = document.getElementById('mic-error-area');
        if (!errorArea) {
            errorArea = document.createElement('div');
            errorArea.id = 'mic-error-area';
            errorArea.style.color = 'red';
            errorArea.style.marginTop = '10px';
            errorArea.style.fontWeight = 'bold';
            if (micBtn && micBtn.parentNode) {
                micBtn.parentNode.appendChild(errorArea);
            } else {
                document.body.appendChild(errorArea);
            }
        }
        return errorArea;
    }

    // Debug: Check for required elements
    if (!micBtn) console.error('Mic button (mic-btn) not found!');
    if (!questionInput) console.error('Question input (question-input) not found!');
    if (!micIcon) console.error('Mic icon (mic-icon) not found!');
    const errorArea = ensureErrorArea();

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
                errorArea.textContent = '';
                console.log('[Mic] Starting recognition with lang:', lang);
                recognition.start();
            });
        }

        recognition.onstart = function() {
            recognizing = true;
            if (micIcon) micIcon.textContent = '🔴';
            console.log('[Mic] Recognition started');
        };
        recognition.onend = function() {
            recognizing = false;
            if (micIcon) micIcon.textContent = '🎤';
            console.log('[Mic] Recognition ended');
        };
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            console.log('[Mic] Transcript:', transcript);
            if (questionInput) questionInput.value = transcript;
            else console.error('questionInput is null, cannot set value.');
        };
        recognition.onerror = function(event) {
            recognizing = false;
            if (micIcon) micIcon.textContent = '🎤';
            let msg = (window.language === 'hi' ? 'माइक काम नहीं कर रहा है।' : (window.language === 'gu' ? 'માઇક કામ કરતો નથી.' : 'Mic is not working.')) + '\nError: ' + event.error;
            errorArea.textContent = msg;
            alert(msg);
            console.error('[Mic] Speech recognition error:', event);
        };
    } else {
        if (micBtn) micBtn.disabled = true;
        let msg = 'SpeechRecognition API not supported in this browser.';
        errorArea.textContent = msg;
        console.error(msg);
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