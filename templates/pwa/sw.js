// Golden Minutes - Service Worker
const CACHE_NAME = 'golden-minutes-v4';
const OFFLINE_URL = '/offline.html';

const CACHE_URLS = [
    '/',
    '/static/css/main.css',
    '/static/js/main.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
];

// Install event - cache essential files
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Caching essential files');
                return cache.addAll(CACHE_URLS);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
    // Skip non-GET requests
    if (event.request.method !== 'GET') {
        return;
    }

    // Special handling for SOS requests - always try network first
    if (event.request.url.includes('/emergencies/sos/')) {
        event.respondWith(
            fetch(event.request)
                .catch(() => {
                    // If offline, store SOS data in IndexedDB for later sync
                    return storePendingSOS(event.request);
                })
        );
        return;
    }

    // 1. HTML Pages (Navigation) -> NETWORK FIRST, then OFFLINE PAGE
    // We do NOT cache HTML pages to avoid "stale auth state" (login issues)
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .catch(() => {
                    return caches.match(OFFLINE_URL);
                })
        );
        return;
    }

    // 2. API calls -> Network First, then Cache
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    return caches.match(event.request);
                })
        );
        return;
    }

    // 3. Static Assets (CSS, JS, Images) -> Cache First, then Network
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});

// Store pending SOS for later sync
function storePendingSOS(request) {
    return request.clone().json().then(data => {
        return openDB().then(db => {
            const tx = db.transaction('pending_sos', 'readwrite');
            const store = tx.objectStore('pending_sos');
            store.add({
                data: data,
                timestamp: Date.now()
            });
            return tx.complete;
        }).then(() => {
            return new Response(JSON.stringify({
                success: true,
                offline: true,
                message: 'SOS stored for sync when online'
            }), {
                headers: { 'Content-Type': 'application/json' }
            });
        });
    });
}

// IndexedDB helper
function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('golden_minutes_db', 1);

        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);

        request.onupgradeneeded = event => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('pending_sos')) {
                db.createObjectStore('pending_sos', { autoIncrement: true });
            }
        };
    });
}

// Background sync for pending SOS
self.addEventListener('sync', event => {
    if (event.tag === 'sync-sos') {
        event.waitUntil(syncPendingSOS());
    }
});

function syncPendingSOS() {
    return openDB().then(db => {
        const tx = db.transaction('pending_sos', 'readonly');
        const store = tx.objectStore('pending_sos');
        return store.getAll();
    }).then(pendingItems => {
        return Promise.all(
            pendingItems.map(item => {
                return fetch('/emergencies/sos/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(item.data)
                }).then(() => {
                    // Remove from IndexedDB after successful sync
                    return openDB().then(db => {
                        const tx = db.transaction('pending_sos', 'readwrite');
                        const store = tx.objectStore('pending_sos');
                        store.delete(item.id);
                        return tx.complete;
                    });
                });
            })
        );
    }

// Push Notification Event Handler
self.addEventListener('push', event => {
        console.log('Push notification received:', event);

        let notificationData = {
            title: 'Emergency Alert',
            body: 'New emergency nearby',
            icon: '/static/images/icon-192.png',
            badge: '/static/images/badge-72.png',
            tag: 'emergency-alert',
            requireInteraction: true,
            data: {
                url: '/emergencies/map/'
            }
        };

        if (event.data) {
            try {
                const data = event.data.json();
                notificationData = {
                    title: `🚨 ${data.emergency_type || 'Emergency Alert'}`,
                    body: `${data.distance || 'Nearby'} • ${data.severity || 'High'} Priority\nTap to respond`,
                    icon: '/static/images/icon-192.png',
                    badge: '/static/images/badge-72.png',
                    tag: `emergency-${data.emergency_id}`,
                    requireInteraction: true,
                    vibrate: [200, 100, 200, 100, 200],
                    data: {
                        url: `/emergencies/${data.emergency_id}/`,
                        emergency_id: data.emergency_id
                    }
                };
            } catch (e) {
                console.error('Error parsing push data:', e);
            }
        }

        event.waitUntil(
            self.registration.showNotification(notificationData.title, notificationData)
        );
    });

    // Notification Click Handler
    self.addEventListener('notificationclick', event => {
        console.log('Notification clicked:', event);
        event.notification.close();

        const urlToOpen = event.notification.data?.url || '/emergencies/map/';

        event.waitUntil(
            clients.matchAll({ type: 'window', includeUncontrolled: true })
                .then(windowClients => {
                    // Check if there's already a window open
                    for (let client of windowClients) {
                        if (client.url.includes(urlToOpen) && 'focus' in client) {
                            return client.focus();
                        }
                    }
                    // Open new window if none found
                    if (clients.openWindow) {
                        return clients.openWindow(urlToOpen);
                    }
                })
        );
    });

    console.log('Golden Minutes Service Worker loaded with Push Notifications');
