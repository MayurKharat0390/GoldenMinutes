// Golden Minutes - Push Notifications Manager

class NotificationManager {
    constructor() {
        this.swRegistration = null;
        this.isSubscribed = false;
    }

    async init() {
        // Check if service worker and notifications are supported
        if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
            console.warn('Push notifications not supported');
            return false;
        }

        try {
            // Wait for service worker to be ready
            this.swRegistration = await navigator.serviceWorker.ready;
            console.log('Service Worker ready for push notifications');

            // Check current subscription status
            const subscription = await this.swRegistration.pushManager.getSubscription();
            this.isSubscribed = subscription !== null;

            // Request permission if not already granted
            if (Notification.permission === 'default') {
                await this.requestPermission();
            }

            return true;
        } catch (error) {
            console.error('Error initializing notifications:', error);
            return false;
        }
    }

    async requestPermission() {
        const permission = await Notification.permission;

        if (permission === 'denied') {
            console.warn('Notification permission denied');
            return false;
        }

        if (permission === 'granted') {
            await this.subscribe();
            return true;
        }

        // Show custom UI to explain why we need permission
        const result = await Notification.requestPermission();
        if (result === 'granted') {
            await this.subscribe();
            return true;
        }

        return false;
    }

    async subscribe() {
        try {
            const subscription = await this.swRegistration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: this.urlBase64ToUint8Array(
                    'BAY1faI3PrR8PO_iTaixQDBwfdvcPn5M0stHsSs0dADbZzWdtsOmeM3BA--_G6tV0Q2xZCuhMXxgi3U7ZIwQ9Lc'
                )
            });

            console.log('Push subscription successful:', subscription);

            // Send subscription to backend
            await this.sendSubscriptionToBackend(subscription);
            this.isSubscribed = true;

            return subscription;
        } catch (error) {
            console.error('Failed to subscribe:', error);
            return null;
        }
    }

    async sendSubscriptionToBackend(subscription) {
        try {
            const response = await fetch('/api/push-subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    subscription: subscription.toJSON(),
                    user_agent: navigator.userAgent
                })
            });

            if (!response.ok) {
                throw new Error('Failed to send subscription to server');
            }

            console.log('Subscription sent to backend successfully');
        } catch (error) {
            console.error('Error sending subscription:', error);
        }
    }

    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');

        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Show a test notification
    async showTestNotification() {
        if (Notification.permission === 'granted' && this.swRegistration) {
            await this.swRegistration.showNotification('Golden Minutes Test', {
                body: 'Push notifications are working! 🚨',
                icon: '/static/images/icon-192.png',
                badge: '/static/images/badge-72.png',
                vibrate: [200, 100, 200]
            });
        }
    }
}

// Initialize on page load
const notificationManager = new NotificationManager();

document.addEventListener('DOMContentLoaded', async () => {
    const initialized = await notificationManager.init();

    if (initialized) {
        console.log('✓ Push notifications ready');

        // Show permission request after 3 seconds if not already granted
        if (Notification.permission === 'default') {
            setTimeout(() => {
                showNotificationPrompt();
            }, 3000);
        }
    }
});

// Show a nice UI prompt for notification permission
function showNotificationPrompt() {
    // Check if we should show the prompt (don't spam users)
    const lastPrompt = localStorage.getItem('lastNotificationPrompt');
    if (lastPrompt) {
        const daysSinceLastPrompt = (Date.now() - parseInt(lastPrompt)) / (1000 * 60 * 60 * 24);
        if (daysSinceLastPrompt < 7) {
            return; // Don't show more than once per week
        }
    }

    // Create a nice banner
    const banner = document.createElement('div');
    banner.className = 'notification-prompt';
    banner.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        max-width: 90%;
        animation: slideUp 0.3s ease;
    `;

    banner.innerHTML = `
        <div class="d-flex align-items-center gap-3">
            <i class="bi bi-bell-fill fs-3"></i>
            <div class="flex-grow-1">
                <strong>Get Emergency Alerts</strong>
                <p class="mb-0 small">Be notified of emergencies near you</p>
            </div>
            <button class="btn btn-light btn-sm fw-bold" onclick="enableNotifications()">Enable</button>
            <button class="btn btn-link text-white btn-sm" onclick="dismissNotificationPrompt()">Later</button>
        </div>
    `;

    document.body.appendChild(banner);
    localStorage.setItem('lastNotificationPrompt', Date.now().toString());
}

async function enableNotifications() {
    const success = await notificationManager.requestPermission();
    if (success) {
        dismissNotificationPrompt();
        // Show success message
        alert('✓ Notifications enabled! You\'ll be alerted of nearby emergencies.');
    }
}

function dismissNotificationPrompt() {
    const prompt = document.querySelector('.notification-prompt');
    if (prompt) {
        prompt.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => prompt.remove(), 300);
    }
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from { transform: translateX(-50%) translateY(100px); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    @keyframes slideDown {
        from { transform: translateX(-50%) translateY(0); opacity: 1; }
        to { transform: translateX(-50%) translateY(100px); opacity: 0; }
    }
`;
document.head.appendChild(style);
