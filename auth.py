import hashlib
import hmac


# ============================================================
# AUTHORIZED USERS
# ============================================================

USERS = {
    "admin": {
        "role": "Admin",
        "salt": b"ehr_admin_salt",
        "password_hash": "09e2a2560bedfa2dc90753cdd39967f52bcfa03f32e0c1dc366c8ab80c091e6c"
    },
    #admin123---admin password
    #doctor123--doctor password 
    
    "doctor": {
        "role": "Doctor",
        "salt": b"ehr_doctor_salt",
        "password_hash": "03a030c7a207f0a50d450076ba25b49f9bfefb5b3b20062204ad51aa1fb590de"
    }
}


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(username, password):
    """Verify the password of an authorized user."""

    if username not in USERS:
        return False

    user = USERS[username]

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        user["salt"],
        100000
    ).hex()

    return hmac.compare_digest(
        password_hash,
        user["password_hash"]
    )


# ============================================================
# USER AUTHENTICATION
# ============================================================

def authenticate_user(username, password):
    """Authenticate a user and return their role."""

    if verify_password(username, password):
        return USERS[username]["role"]

    return None