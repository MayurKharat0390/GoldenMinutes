/**
 * Golden Minutes - Voice Trigger System
 * Uses Web Audio API for scream detection and Web Speech API for phrase detection.
 * Designed to work in high-stress, muffled environments (e.g., pocket).
 */

class VoiceTrigger {
    constructor() {
        this.isActive = false;
        this.audioContext = null;
        this.analyser = null;
        this.microphone = null;
        this.recognition = null;
        this.processor = null;

        // State
        this.isAlarming = false;
        this.consecutiveLoudFrames = 0;
        this.silenceFrames = 0;

        // Constants
        this.SCREAM_THRESHOLD = 0.45; // RMS Amplitude (0.0 to 1.0).
        this.SCREAM_FRAMES_REQUIRED = 8; // ~200ms of sustained loud noise
        this.TRIGGER_PHRASES = [
            'help me', 'help', 'bachao', 'bachao bachao', 'madat kara',
            'ambulance', 'emergency', 'save me', 'police', 'doctor',
            'accident', 'aag lagi', 'aag'
        ];
        
        this.isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

        // Voice Prep
        if ('speechSynthesis' in window) {
            window.speechSynthesis.getVoices();
        }
    }

    async enable() {
        if (this.isActive) return;
        console.log("Enabling Voice Trigger [Mobile:" + this.isMobile + "]");

        try {
            if (this.isMobile) {
                // ON MOBILE: Do NOT request getUserMedia. 
                // STT needs exclusive mic access on Chrome Android.
                await this.startSpeechRecognition();
                this.speakFeedback("Voice trigger active.");
            } else {
                // ON DESKTOP: We can usually share or sequential access.
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                await this.startSpeechRecognition();
                setTimeout(() => this.startAudioAnalysis(stream), 1000);
                this.speakFeedback("Voice trigger activated.");
            }

            this.isActive = true;
            this.updateStatusUI(true);
            return true;
        } catch (err) {
            console.error("Voice Trigger Error:", err);
            alert("Microphone access required for voice trigger.");
            this.updateStatusUI(false);
            return false;
        }
    }

    disable() {
        if (!this.isActive) return;
        this.isActive = false;

        // Stop Audio Context
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }

        // Stop Recognition
        if (this.recognition) {
            try {
                this.recognition.onend = null; // Prevent restart
                this.recognition.stop();
            } catch (e) {}
            this.recognition = null;
        }

        this.speakFeedback("Voice trigger disabled.");
        this.updateStatusUI(false);
        console.log("Voice Trigger Disabled");
    }

    async startAudioAnalysis(stream) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) throw new Error("AudioContext not supported");

        this.audioContext = new AudioContext();
        
        // Resume context
        if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
        }

        this.microphone = this.audioContext.createMediaStreamSource(stream);
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 512;

        this.processor = this.audioContext.createScriptProcessor(2048, 1, 1);

        this.microphone.connect(this.analyser);
        this.analyser.connect(this.processor);
        this.processor.connect(this.audioContext.destination);

        this.processor.onaudioprocess = (e) => {
            if (!this.isActive || this.isAlarming) return;

            const input = e.inputBuffer.getChannelData(0);
            let sum = 0;

            for (let i = 0; i < input.length; i++) {
                sum += input[i] * input[i];
            }
            const rms = Math.sqrt(sum / input.length);

            // Scream Logic
            if (rms > this.SCREAM_THRESHOLD) {
                this.consecutiveLoudFrames++;
                if (this.consecutiveLoudFrames > this.SCREAM_FRAMES_REQUIRED) {
                    console.log(`Volume Trigger! RMS: ${rms.toFixed(2)}`);
                    this.triggerEmergencySequence('High Volume Detected');
                    this.consecutiveLoudFrames = 0;
                }
            } else {
                this.consecutiveLoudFrames = Math.max(0, this.consecutiveLoudFrames - 0.5);
            }
        };
        console.log("Audio Analysis (Scream Detection) started.");
    }

    startSpeechRecognition() {
        return new Promise((resolve, reject) => {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            
            if (!SpeechRecognition) {
                console.warn("Speech Recognition not supported.");
                resolve();
                return;
            }

            this.recognition = new SpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true; // Use interim for faster response
            this.recognition.lang = 'en-IN'; // Better for Indian accents (Hindi/English mix)

            this.recognition.onstart = () => {
                console.log("STT Service Active.");
                resolve();
            };

            this.recognition.onresult = (event) => {
                if (!this.isActive || this.isAlarming) return;
                const lastResultIndex = event.results.length - 1;
                const transcript = event.results[lastResultIndex][0].transcript.trim().toLowerCase();
                console.log("Heard:", transcript);

                if (this.TRIGGER_PHRASES.some(phrase => transcript.includes(phrase))) {
                    this.triggerEmergencySequence(`Voice Phrase: "${transcript}"`);
                }
            };

            this.recognition.onerror = (event) => {
                console.error("STT Error:", event.error);
                if (event.error === 'not-allowed' || event.error === 'service-busy') {
                    console.warn("STT Engine busy/blocked.");
                }
            };

            this.recognition.onend = () => {
                if (this.isActive && !this.isAlarming) {
                    try { this.recognition.start(); } catch (e) {}
                }
            };

            try {
                this.recognition.start();
            } catch (e) {
                console.error("STT Start Error:", e);
                resolve(); // Don't block
            }
        });
    }

    triggerEmergencySequence(source) {
        if (this.isAlarming) return;
        this.isAlarming = true;

        console.warn(`🚨 SOS TRIGGERED VIA VOICE: ${source}`);

        if (navigator.vibrate) {
            navigator.vibrate([200, 100, 200, 100, 500]);
        }

        if (window.GoldenMinutes && window.GoldenMinutes.fallDetector) {
            const fd = window.GoldenMinutes.fallDetector;

            const title = document.getElementById('fall-modal-title');
            if (title) title.innerHTML = '<i class="bi bi-mic-fill text-danger me-2"></i>Voice Trigger';

            const body = document.getElementById('fall-modal-body');
            if (body) body.innerHTML = `<h3>${source}</h3><p>Triggering SOS in 5 seconds...</p>`;

            fd.showFallModal('alarm'); 
            fd.state = 'ALARM';

            this.speakFeedback("Emergency detected. Triggering S O S in five seconds. Tap to cancel.");

            setTimeout(() => {
                if (fd.state === 'ALARM') {
                    fd.triggerSOS();
                    this.isAlarming = false;
                }
            }, 5000);

        } else {
            this.speakFeedback("Emergency triggered. Press O K to send S O S.");
            if (confirm(`EMERGENCY TRIGGERED: ${source}\nPress OK to send SOS, Cancel to stop.`)) {
                window.location.href = "/emergencies/sos/";
            } else {
                this.isAlarming = false;
            }
        }
    }

    speakFeedback(text) {
        if (!('speechSynthesis' in window)) return;

        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        
        // Pick English voice if available
        const voices = window.speechSynthesis.getVoices();
        const enVoice = voices.find(v => v.lang.startsWith('en'));
        if (enVoice) utterance.voice = enVoice;

        window.speechSynthesis.speak(utterance);
    }

    updateStatusUI(enabled) {
        const toggleBtn = document.getElementById('voiceTriggerToggle');
        if (toggleBtn) toggleBtn.checked = enabled;

        const badge = document.getElementById('voice-trigger-badge');
        if (badge) badge.style.display = enabled ? 'inline-block' : 'none';
    }
}

// Global initialization safety
if (typeof window.GoldenMinutes === 'undefined') {
    window.GoldenMinutes = {};
}

const voiceTrigger = new VoiceTrigger();
window.GoldenMinutes.voiceTrigger = voiceTrigger;
