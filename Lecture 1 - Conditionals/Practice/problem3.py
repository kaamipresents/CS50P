# Simple Role Permission System

def main():
    role = input("Enter your role (admin, editor, viewer): ").lower().strip()

    match role:
        case "admin":
            print("You have full access to the system.")
        case "editor":
            print("You can edit content but cannot manage users.")
        case "viewer":
            print("You can view content but cannot edit or manage users.")
        case _:
            print("Invalid role. Please enter admin, editor, or viewer.")

main()
