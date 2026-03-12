default_settings = {
    "theme": "light",
    "notifications": True,
    "language": "English"
}

user_settings = {
    "theme": "dark",
    "language": "Urdu"
}

updated_settings = {**default_settings, **user_settings}

print(updated_settings)

# Output:
# {'theme': 'dark', 'notifications': True, 'language': 'Urdu'}