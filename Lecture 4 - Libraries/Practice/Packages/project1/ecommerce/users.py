# ==============================
# USER MANAGEMENT
# ==============================

def create_user(username, email):
    return {
        "username": username,
        "email": email,
        "is_active": True
    }

def deactivate_user(user):
    user["is_active"] = False
    return user

def display_user(user):
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Active: {user['is_active']}")
    print("-" * 30)

