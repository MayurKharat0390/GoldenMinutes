// Golden Minutes - Main JavaScript

// Geolocation Helper
const GeoLocation = {
    getCurrentPosition: function(successCallback, errorCallback) {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
                successCallback,
                errorCallback,
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        } else {
            console.error('Geolocation not supported');
            if (errorCallback) errorCallback(new Error('Geolocation not supported'));
        }
    },

    watchPosition: function(successCallback, errorCallback) {
        if ('geolocation' in navigator) {
            return navigator.geolocation.watchPosition(
                successCallback,
                errorCallback,
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 30000
                }
            );
        }
        return null;
    }
};

// Update user location periodically
function updateUserLocation() {
    GeoLocation.getCurrentPosition(
        function(position) {
            const data = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };

            fetch('/accounts/update-location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Location updated:', data);
            })
            .catch(error => {
                console.error('Error updating location:', error);
            });
        },
        function(error) {
            console.error('Geolocation error:', error);
        }
    );
}

// Get CSRF token from cookies
function getCookie(name) {
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

// Initialize location tracking on page load
document.addEventListener('DOMContentLoaded', function() {
    // Update location every 5 minutes for authenticated users
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (isAuthenticated) {
        updateUserLocation();
        setInterval(updateUserLocation, 5 * 60 * 1000); // 5 minutes
    }

    // SOS Button confirmation
    const sosButton = document.getElementById('sosButton');
    if (sosButton) {
        sosButton.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to trigger an SOS emergency alert?')) {
                e.preventDefault();
            }
        });
    }
});

// Map Helper Functions
const MapHelper = {
    createMap: function(elementId, center, zoom = 13) {
        const map = L.map(elementId).setView(center, zoom);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        
        return map;
    },

    addEmergencyMarker: function(map, emergency) {
        const iconColor = this.getSeverityColor(emergency.severity);
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${iconColor}; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; border: 3px solid white; box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
                    <i class="bi bi-exclamation-triangle-fill"></i>
                   </div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });

        const marker = L.marker([emergency.latitude, emergency.longitude], { icon: icon })
            .addTo(map);

        const popupContent = `
            <div class="emergency-popup">
                <h6>${emergency.emergency_type_display}</h6>
                <p class="mb-1"><strong>Severity:</strong> <span class="badge severity-${emergency.severity}">${emergency.severity}</span></p>
                <p class="mb-1"><strong>Status:</strong> ${emergency.status_display}</p>
                <p class="mb-0"><small>${emergency.triggered_at}</small></p>
                <a href="/emergencies/${emergency.emergency_id}/" class="btn btn-sm btn-danger mt-2">View Details</a>
            </div>
        `;

        marker.bindPopup(popupContent);
        return marker;
    },

    addResponderMarker: function(map, responder) {
        const icon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: #28a745; width: 25px; height: 25px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                    <i class="bi bi-person-fill"></i>
                   </div>`,
            iconSize: [25, 25],
            iconAnchor: [12, 12]
        });

        return L.marker([responder.latitude, responder.longitude], { icon: icon })
            .addTo(map)
            .bindPopup(`<strong>Responder:</strong> ${responder.name}`);
    },

    getSeverityColor: function(severity) {
        const colors = {
            'critical': '#dc3545',
            'high': '#ff6b6b',
            'moderate': '#ffc107',
            'low': '#28a745'
        };
        return colors[severity] || '#6c757d';
    }
};

// Real-time Emergency Updates
let emergencyUpdateInterval = null;

function startEmergencyUpdates(emergencyId) {
    if (emergencyUpdateInterval) {
        clearInterval(emergencyUpdateInterval);
    }

    emergencyUpdateInterval = setInterval(function() {
        fetch(`/emergencies/api/${emergencyId}/status/`)
            .then(response => response.json())
            .then(data => {
                updateEmergencyUI(data);
            })
            .catch(error => {
                console.error('Error fetching emergency status:', error);
            });
    }, 10000); // Update every 10 seconds
}

function stopEmergencyUpdates() {
    if (emergencyUpdateInterval) {
        clearInterval(emergencyUpdateInterval);
        emergencyUpdateInterval = null;
    }
}

function updateEmergencyUI(data) {
    // Update status badge
    const statusBadge = document.getElementById('emergencyStatus');
    if (statusBadge) {
        statusBadge.className = `badge status-${data.status}`;
        statusBadge.textContent = data.status_display;
    }

    // Update responder info
    const responderInfo = document.getElementById('responderInfo');
    if (responderInfo && data.primary_responder) {
        responderInfo.innerHTML = `
            <div class="alert alert-success">
                <i class="bi bi-person-check-fill"></i>
                <strong>Responder Assigned:</strong> ${data.primary_responder.name}
                <br>
                <small>ETA: ${data.primary_responder.eta} minutes</small>
            </div>
        `;
    }
}

// Offline Support
window.addEventListener('online', function() {
    console.log('Back online');
    const offlineBanner = document.getElementById('offlineBanner');
    if (offlineBanner) {
        offlineBanner.style.display = 'none';
    }
});

window.addEventListener('offline', function() {
    console.log('Gone offline');
    const offlineBanner = document.getElementById('offlineBanner');
    if (offlineBanner) {
        offlineBanner.style.display = 'block';
    }
});

// Export for use in other scripts
window.GoldenMinutes = {
    GeoLocation,
    MapHelper,
    getCookie,
    updateUserLocation,
    startEmergencyUpdates,
    stopEmergencyUpdates
};
