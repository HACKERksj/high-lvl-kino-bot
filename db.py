import sqlite3
import asyncio
from datetime import datetime
from config import DATABASE_PATH

# =============================================
# 🗄 DATABASE — db.py
# =============================================

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Barcha jadvallarni yaratadi (birinchi ishga tushganda)."""
    conn = get_connection()
    cursor = conn.cursor()

    # Kinolar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            message_id INTEGER NOT NULL,
            is_premium INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Foydalanuvchilar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            is_premium INTEGER DEFAULT 0,
            referral_count INTEGER DEFAULT 0,
            referred_by INTEGER,
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_active TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # So'rovlar tarixi
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_code TEXT NOT NULL,
            requested_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Kunlik statistika
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            date TEXT PRIMARY KEY,
            request_count INTEGER DEFAULT 0,
            new_users INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized.")


# ──────────────────────────────────────────────
# MOVIE CRUD
# ──────────────────────────────────────────────

def add_movie(code: str, name: str, message_id: int, is_premium: bool = False) -> bool:
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO movies (code, name, message_id, is_premium) VALUES (?, ?, ?, ?)",
            (code.upper(), name, message_id, int(is_premium))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_movie_by_code(code: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM movies WHERE code = ?", (code.upper(),)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def search_movies_by_name(query: str, limit: int = 5) -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM movies WHERE name LIKE ? LIMIT ?",
        (f"%{query}%", limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_movie(code: str) -> bool:
    conn = get_connection()
    cursor = conn.execute("DELETE FROM movies WHERE code = ?", (code.upper(),))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def edit_movie_name(code: str, new_name: str) -> bool:
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE movies SET name = ? WHERE code = ?", (new_name, code.upper())
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def get_all_movies() -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_random_movie():
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM movies ORDER BY RANDOM() LIMIT 1"
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ──────────────────────────────────────────────
# USER CRUD
# ──────────────────────────────────────────────

def get_or_create_user(user_id: int, username: str, full_name: str, referred_by: int = None):
    conn = get_connection()
    existing = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    if not existing:
        conn.execute(
            "INSERT INTO users (id, username, full_name, referred_by) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, referred_by)
        )
        # Referalni hisoblash
        if referred_by:
            conn.execute(
                "UPDATE users SET referral_count = referral_count + 1 WHERE id = ?",
                (referred_by,)
            )
            # Threshold tekshirish
            row = conn.execute(
                "SELECT referral_count FROM users WHERE id = ?", (referred_by,)
            ).fetchone()
            from config import REFERRAL_THRESHOLD
            if row and row["referral_count"] >= REFERRAL_THRESHOLD:
                conn.execute(
                    "UPDATE users SET is_premium = 1 WHERE id = ?", (referred_by,)
                )
        conn.commit()
        conn.close()
        return True  # yangi user
    else:
        conn.execute(
            "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE id = ?", (user_id,)
        )
        conn.commit()
        conn.close()
        return False  # mavjud user


def get_user(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def set_premium(user_id: int, status: bool = True):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET is_premium = ? WHERE id = ?", (int(status), user_id)
    )
    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# STATS
# ──────────────────────────────────────────────

def log_request(user_id: int, movie_code: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO requests (user_id, movie_code) VALUES (?, ?)",
        (user_id, movie_code)
    )
    today = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        """INSERT INTO daily_stats (date, request_count) VALUES (?, 1)
           ON CONFLICT(date) DO UPDATE SET request_count = request_count + 1""",
        (today,)
    )
    conn.commit()
    conn.close()


def get_stats() -> dict:
    conn = get_connection()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_requests = conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    top_movie_row = conn.execute(
        "SELECT movie_code, COUNT(*) as cnt FROM requests GROUP BY movie_code ORDER BY cnt DESC LIMIT 1"
    ).fetchone()
    top_movie = top_movie_row["movie_code"] if top_movie_row else "N/A"

    today = datetime.now().strftime("%Y-%m-%d")
    daily = conn.execute(
        "SELECT request_count FROM daily_stats WHERE date = ?", (today,)
    ).fetchone()
    daily_count = daily["request_count"] if daily else 0
    conn.close()

    return {
        "total_users": total_users,
        "total_requests": total_requests,
        "top_movie": top_movie,
        "daily_requests": daily_count,
    }
