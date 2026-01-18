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
        this.SCREAM_THRESHOLD = 0.5; // RMS Amplitude (0.0 to 1.0). Adjusted for high sensitivity.
        this.SCREAM_FRAMES_REQUIRED = 10; // ~200-300ms of sustained loud noise
        this.TRIGGER_PHRASES = [
            'help me', 'help', 'bachao', 'madat kara',
            'call ambulance', 'call doctor', 'ambulance',
            'emergency', 'save me'
        ];
    }

    async enable() {
        if (this.isActive) return;

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.startAudioAnalysis(stream);
            this.startSpeechRecognition();

            this.isActive = true;
            this.updateStatusUI(true);
            console.log("Voice Trigger Enabled");
            return true;
        } catch (err) {
            console.error("Microphone access denied or error:", err);
            alert("Microphone permission required for Voice Trigger.");
            this.updateStatusUI(false);
            return false;
        }
    }

    disable() {
        this.isActive = false;

        // Stop Audio Context
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }

        // Stop Recognition
        if (this.recognition) {
            this.recognition.stop();
            this.recognition = null;
        }

        // Stop updates
        this.updateStatusUI(false);
        console.log("Voice Trigger Disabled");
    }

    startAudioAnalysis(stream) {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.microphone = this.audioContext.createMediaStreamSource(stream);
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 512;

        // ScriptProcessor (Deprecated but widely supported for simple real-time RMS)
        // or AudioWorklet (Better, but more setup). Using ScriptProcessor for simplicity in this prototype.
        this.processor = this.audioContext.createScriptProcessor(2048, 1, 1);

        this.microphone.connect(this.analyser);
        this.analyser.connect(this.processor);
        this.processor.connect(this.audioContext.destination);

        this.processor.onaudioprocess = (e) => {
            if (!this.isActive || this.isAlarming) return;

            const input = e.inputBuffer.getChannelData(0);
            let sum = 0;

            // Calculate RMS (Root Mean Square) volume
            for (let i = 0; i < input.length; i++) {
                sum += input[i] * input[i];
            }
            const rms = Math.sqrt(sum / input.length);

            // Scream Logic: Sudden, sustained loud volume
            // Threshold 0.5 is quite loud. Pocket muffling reduces high freq but bass/volume often remains high.
            // We might effectively need a lower threshold if we detect muffling, but 0.4-0.5 is a safe "Scream" baseline.
            if (rms > 0.4) {
                this.consecutiveLoudFrames++;
                if (this.consecutiveLoudFrames > this.SCREAM_FRAMES_REQUIRED) {
                    console.log(`Scream Detected! RMS: ${rms.toFixed(2)}`);
                    this.triggerEmergencySequence('Scream Detected');
                    this.consecutiveLoudFrames = 0; // Reset
                }
            } else {
                this.consecutiveLoudFrames = Math.max(0, this.consecutiveLoudFrames - 1); // Decay
            }
        };
    }

    startSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn("Speech Recognition not supported in this browser.");
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = false; // We want final results for accuracy
        this.recognition.lang = 'en-US'; // Default, captures "Help" well.

        this.recognition.onresult = (event) => {
            if (!this.isActive || this.isAlarming) return;

            const lastResultIndex = event.results.length - 1;
            const transcript = event.results[lastResultIndex][0].transcript.trim().toLowerCase();
            console.log("Heard:", transcript);

            // Check against phrases
            if (this.TRIGGER_PHRASES.some(phrase => transcript.includes(phrase))) {
                console.log("Trigger Phrase Detected:", transcript);
                this.triggerEmergencySequence(`Voice Phrase: "${transcript}"`);
            }
        };

        this.recognition.onerror = (event) => {
            // console.log("Speech recognition error", event.error);
        };

        this.recognition.onend = () => {
            if (this.isActive) {
                // Restart if it stopped (it does this periodically)
                try {
                    this.recognition.start();
                } catch (e) { }
            }
        };

        try {
            this.recognition.start();
        } catch (e) { }
    }

    triggerEmergencySequence(source) {
        if (this.isAlarming) return;
        this.isAlarming = true;

        console.log(`Triggering Voice Emergency via ${source}`);

        // 1. Vibrate to confirm trigger (Tactile feedback in pocket)
        if (navigator.vibrate) {
            navigator.vibrate([200, 100, 200, 100, 500]);
        }

        // 2. Reuse Fall Detection Modal for the countdown UI
        // We assume fall_detection.js is loaded and has showFallModal
        // If not, we fall back to direct SOS or alert
        if (window.GoldenMinutes && window.GoldenMinutes.fallDetector) {
            // Hijack the fall detector's alarm flow
            // Set state to WAITING to trigger the UI flow
            const fd = window.GoldenMinutes.fallDetector;

            // Update Title for context
            const title = document.getElementById('fall-modal-title');
            if (title) title.innerHTML = '<i class="bi bi-mic-fill text-danger me-2"></i>Voice Trigger';

            const body = document.getElementById('fall-modal-body');
            if (body) body.innerHTML = `<h3>${source}</h3><p>Triggering SOS in 5 seconds...</p>`;

            fd.showFallModal('alarm'); // Show red mode immediately
            fd.state = 'ALARM';

            // Custom short timer for voice (5 seconds only)
            // Voice implies immediate danger usually
            setTimeout(() => {
                if (fd.state === 'ALARM') { // If not cancelled
                    fd.triggerSOS();
                    this.isAlarming = false; // Reset my internal lock, let FD handle the rest
                }
            }, 5000);

        } else {
            // Fallback if FD not present
            if (confirm(`EMERGENCY TRIGGERED: ${source}\nPress OK to send SOS, Cancel to stop.`)) {
                window.location.href = "/emergencies/sos/";
            } else {
                this.isAlarming = false;
            }
        }
    }

    updateStatusUI(enabled) {
        const toggleBtn = document.getElementById('voiceTriggerToggle');
        if (toggleBtn) {
            toggleBtn.checked = enabled;
        }

        const badge = document.getElementById('voice-trigger-badge');
        if (badge) {
            badge.style.display = enabled ? 'inline-block' : 'none';
        }
    }
}

// Initialize
const voiceTrigger = new VoiceTrigger();
window.GoldenMinutes.voiceTrigger = voiceTrigger;
