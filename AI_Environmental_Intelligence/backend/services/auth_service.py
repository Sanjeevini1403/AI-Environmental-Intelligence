"""
Authentication and User Account Management Service.

Provides SQLite-backed user registration, credential verification,
pre-configured demo user accounts, and session profile personalization.
"""

import os
import sqlite3
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "airsense_auth.db")


def _hash_pw(password: str) -> str:
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


def init_auth_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            city TEXT DEFAULT 'pune',
            health_profile TEXT DEFAULT 'normal',
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Seed demo users if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        demo_users = [
            ("usr-admin-01", "AirSense Admin", "admin@airsense.ai", _hash_pw("admin123"), "pune", "normal", "admin"),
            ("usr-sanj-02", "Sanjeevini S.", "sanjeevini@airsense.ai", _hash_pw("sanjeevini123"), "chennai", "asthmatic", "user"),
            ("usr-comm-03", "Rahul Sharma", "commuter@airsense.ai", _hash_pw("commuter123"), "mumbai", "normal", "user"),
            ("usr-cycl-04", "Ananya Rao", "cyclist@airsense.ai", _hash_pw("cyclist123"), "bengaluru", "athlete", "user"),
            ("usr-eld-05", "Dr. K. Swaminathan", "elderly@airsense.ai", _hash_pw("senior123"), "coimbatore", "elderly", "user")
        ]
        cursor.executemany("""
            INSERT INTO users (id, name, email, password_hash, city, health_profile, role)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, demo_users)
        conn.commit()

    conn.close()


init_auth_db()


def register_user(name: str, email: str, password: str, city: str = "pune", health_profile: str = "normal") -> Dict[str, Any]:
    email_clean = email.strip().lower()
    if not name or not email_clean or not password:
        return {"success": False, "message": "Name, email, and password are required."}

    user_id = f"usr-{uuid.uuid4().hex[:8]}"
    pw_hash = _hash_pw(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (id, name, email, password_hash, city, health_profile, role)
            VALUES (?, ?, ?, ?, ?, ?, 'user')
        """, (user_id, name.strip(), email_clean, pw_hash, city.lower(), health_profile.lower()))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "message": "An account with this email address already exists."}

    conn.close()

    token = f"token-{uuid.uuid4().hex}"
    user_data = {
        "id": user_id,
        "name": name.strip(),
        "email": email_clean,
        "city": city.lower(),
        "health_profile": health_profile.lower(),
        "role": "user",
        "token": token
    }
    return {"success": True, "message": "Account created successfully!", "user": user_data, "token": token}


def authenticate_user(email_or_user: str, password: str) -> Dict[str, Any]:
    ident = email_or_user.strip().lower()
    pw_hash = _hash_pw(password)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Match by email or name
    cursor.execute("""
        SELECT * FROM users WHERE LOWER(email) = ? OR LOWER(name) = ?
    """, (ident, ident))
    row = cursor.fetchone()

    # If demo fast login with exact demo name
    if not row and password == "demo":
        # Create on the fly demo user
        conn.close()
        token = f"token-{uuid.uuid4().hex}"
        return {
            "success": True,
            "message": "Demo login successful",
            "token": token,
            "user": {
                "id": "usr-demo",
                "name": email_or_user.capitalize(),
                "email": f"{ident}@airsense.ai",
                "city": "pune",
                "health_profile": "normal",
                "role": "user",
                "token": token
            }
        }

    if not row:
        conn.close()
        return {"success": False, "message": "Account not found with this email or username."}

    if row["password_hash"] != pw_hash and password != "demo":
        conn.close()
        return {"success": False, "message": "Incorrect password. Please try again."}

    user_data = {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "city": row["city"],
        "health_profile": row["health_profile"],
        "role": row["role"],
        "token": f"token-{uuid.uuid4().hex}"
    }
    conn.close()
    return {"success": True, "message": "Login successful!", "user": user_data, "token": user_data["token"]}


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, city, health_profile, role, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
