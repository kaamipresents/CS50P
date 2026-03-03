"""
logic.py — Pure business logic, zero Flask dependency.
This file is intentionally framework-agnostic so the same
functions work identically in the CLI and in the Flask app.
"""

import json
import os
import csv
from datetime import datetime

# ─────────────────────────────────────────────
# File paths (relative to project root)
# ─────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
GREETINGS_FILE = os.path.join(DATA_DIR, "greetings.json")
GREETINGS_CSV = os.path.join(DATA_DIR, "greetings.csv")


# ─────────────────────────────────────────────
# Data helpers
# ─────────────────────────────────────────────

def ensure_data_dir():
    """Create the data/ directory if it does not exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_greetings():
    """
    Load all past greetings from JSON.
    Returns a list of dicts:
      [{"name": "Alice", "message": "...", "timestamp": "..."}]
    Returns empty list if file is missing or corrupt.
    """
    ensure_data_dir()
    if not os.path.exists(GREETINGS_FILE):
        return []
    try:
        with open(GREETINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Defensive check: must be a list
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_greetings(greetings):
    """
    Persist the full greetings list back to disk as JSON.
    Raises IOError on write failure.
    """
    ensure_data_dir()
    with open(GREETINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(greetings, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────

def validate_name(name):
    """
    Validate a visitor name.

    Rules:
      - Must not be empty or whitespace-only.
      - Must be between 2 and 50 characters.
      - Must contain only letters, spaces, hyphens, apostrophes.

    Returns (True, None) on success.
    Returns (False, error_message) on failure.
    """
    if not name or not name.strip():
        return False, "Name cannot be empty."

    name = name.strip()

    if len(name) < 2:
        return False, "Name must be at least 2 characters long."

    if len(name) > 50:
        return False, "Name must be 50 characters or fewer."

    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'")
    invalid_chars = [ch for ch in name if ch not in allowed]
    if invalid_chars:
        return False, f"Name contains invalid characters: {', '.join(set(invalid_chars))}"

    return True, None


# ─────────────────────────────────────────────
# Core greeting logic
# ─────────────────────────────────────────────

def build_greeting(name):
    """
    Construct a personalised greeting message.
    Returns the greeting string.
    """
    name = name.strip().title()
    hour = datetime.now().hour

    if 5 <= hour < 12:
        time_greeting = "Good morning"
    elif 12 <= hour < 17:
        time_greeting = "Good afternoon"
    elif 17 <= hour < 21:
        time_greeting = "Good evening"
    else:
        time_greeting = "Good night"

    return f"{time_greeting}, {name}! Welcome to the Hello App."


def record_greeting(name):
    """
    Validate the name, build the greeting, persist it, then return it.

    Returns:
      On success: (True, greeting_string, cleaned_name)
      On failure: (False, error_message, None)
    """
    valid, error = validate_name(name)
    if not valid:
        return False, error, None

    clean_name = name.strip().title()
    greeting = build_greeting(clean_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "name": clean_name,
        "message": greeting,
        "timestamp": timestamp,
    }

    try:
        greetings = load_greetings()
        greetings.append(entry)
        save_greetings(greetings)
    except IOError as e:
        # Storage failure is non-fatal; greeting still shown to user
        print(f"[WARN] Could not save greeting: {e}")

    return True, greeting, clean_name


def get_all_greetings():
    """
    Return all past greetings, newest first.
    """
    greetings = load_greetings()
    return list(reversed(greetings))


def get_visitor_count():
    """Return the total number of recorded greetings."""
    return len(load_greetings())


def export_greetings_csv():
    """
    Export greetings to a CSV file.
    Returns the file path on success, None on failure.
    """
    greetings = load_greetings()
    if not greetings:
        return None

    try:
        ensure_data_dir()
        with open(GREETINGS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "message", "timestamp"])
            writer.writeheader()
            writer.writerows(greetings)
        return GREETINGS_CSV
    except IOError:
        return None


def delete_all_greetings():
    """Wipe all stored greetings. Returns True on success."""
    try:
        save_greetings([])
        return True
    except IOError:
        return False
