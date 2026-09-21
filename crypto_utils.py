import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_key():
    """Generate a random 256-bit AES key."""
    return AESGCM.generate_key(bit_length=256)


def encrypt_data(data, key):
    """Encrypt data using AES-256-GCM."""
    aes = AESGCM(key)

    # 12-byte random nonce
    nonce = os.urandom(12)

    # Convert text into bytes
    data_bytes = data.encode("utf-8")

    # Encrypt
    encrypted_data = aes.encrypt(nonce, data_bytes, None)

    # Combine nonce + encrypted data
    result = nonce + encrypted_data

    # Convert to readable text
    return base64.b64encode(result).decode("utf-8")


def decrypt_data(encrypted_data, key):
    """Decrypt AES-256 encrypted data."""
    aes = AESGCM(key)

    # Convert back from Base64
    combined = base64.b64decode(encrypted_data)

    # Separate nonce and encrypted data
    nonce = combined[:12]
    ciphertext = combined[12:]

    # Decrypt
    decrypted_data = aes.decrypt(nonce, ciphertext, None)

    return decrypted_data.decode("utf-8")


def calculate_sha256(data):
    """Calculate SHA-256 hash."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()