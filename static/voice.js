// Speech-to-Text and Text-to-Speech for ShikshaAI
// Uses Web Speech API for both recognition and synthesis

document.addEventListener('DOMContentLoaded', function() {
    const micBtn = document.getElementById('mic-btn');
    const micIcon = document.getElementById('mic-icon');
    const questionInput = document.getElementById('question-input');
    const ttsBtn = document.getElementById('tts-btn');
    let recognizing = false;
    let recognition = null;

    // --- Speech Recognition (STT) ---
    function getLangCode() {
        if (window.language === 'hi') return 'hi-IN';
        if (window.language === 'gu') return 'gu-IN';
        return 'en-US';
    }

    function setMicIcon(listening) {
        if (micIcon) {
            micIcon.textContent = listening ? '🔴' : '🎤';
        }
    }

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = getLangCode();
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        micBtn && micBtn.addEventListener('click', function() {
            if (recognizing) {
                recognition.stop();
                return;
            }
            recognition.lang = getLangCode();
            try {
                recognition.start();
                setMicIcon(true);
                console.log('Mic: Recognition started, lang:', recognition.lang);
            } catch (e) {
                setMicIcon(false);
                alert('Could not start microphone.');
                console.error('Mic: Error starting recognition', e);
            }
        });

        recognition.onstart = function() {
            recognizing = true;
            setMicIcon(true);
            console.log('Mic: Listening...');
        };
        recognition.onend = function() {
            recognizing = false;
            setMicIcon(false);
            console.log('Mic: Recognition ended.');
        };
        recognition.onresult = function(event) {
            if (event.results && event.results[0] && event.results[0][0]) {
                const transcript = event.results[0][0].transcript;
                if (questionInput) questionInput.value = transcript;
                console.log('Mic: Transcript:', transcript);
            }
        };
        recognition.onerror = function(event) {
            recognizing = false;
            setMicIcon(false);
            let msg = 'Mic is not working.';
            if (window.language === 'hi') msg = 'माइक काम नहीं कर रहा है।';
            if (window.language === 'gu') msg = 'માઇક કામ કરતો નથી.';
            alert(msg);
            console.error('Mic: Error', event.error);
        };
    } else {
        if (micBtn) {
            micBtn.disabled = true;
            micBtn.title = 'Speech recognition not supported in this browser.';
        }
        if (micIcon) micIcon.textContent = '🚫';
        console.warn('Mic: Speech recognition not supported.');
    }

    // --- Text-to-Speech (TTS) ---
    if (ttsBtn) {
        ttsBtn.addEventListener('click', function() {
            const text = window.answerText || '';
            if (!text) return;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = getLangCode();
            utter.rate = 0.95;
            utter.pitch = 1.1;
            window.speechSynthesis.speak(utter);
        });
    }
}); 