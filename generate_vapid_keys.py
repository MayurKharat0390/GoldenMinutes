from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate private key
private_key = ec.generate_private_key(ec.SECP256R1())

# Get public key
public_key = private_key.public_key()

# Serialize private key
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize public key  
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

# Base64 encode for web push
public_key_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')

print("=" * 70)
print("VAPID KEYS GENERATED FOR PUSH NOTIFICATIONS")
print("=" * 70)
print("\nAdd these to golden_minutes/settings.py:\n")
print(f"VAPID_PUBLIC_KEY = '{public_key_b64}'")
print(f"\nVAPID_PRIVATE_KEY = '''")
print(private_bytes.decode('utf-8'), end='')
print("'''")
print("\nVAPID_CLAIMS = {'sub': 'mailto:admin@goldenminutes.com'}")
print("\n" + "=" * 70)
print("\nAlso update static/js/notifications.js:")
print(f"Replace the placeholder key with: '{public_key_b64}'")
print("=" * 70)
