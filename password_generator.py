import random
import string

print("======================================")
print("      RANDOM PASSWORD GENERATOR")
print("======================================")

while True:

    while True:
        try:
            length = int(input("\nEnter password length (minimum 8): "))

            if length < 8:
                print("❌ Password length must be at least 8 characters.")
            else:
                break

        except ValueError:
            print("❌ Please enter a valid number.")

    print("\nChoose character types to include:")
    print("1. Uppercase letters (A-Z)")
    print("2. Lowercase letters (a-z)")
    print("3. Numbers (0-9)")
    print("4. Symbols (!@#$%^&*)")

    while True:
        choices = input(
            "\nEnter your choices separated by commas (example: 1,2,3): "
        )

        selected = set(choices.replace(" ", "").split(","))

        if not selected.issubset({"1", "2", "3", "4"}):
            print("❌ Invalid choice. Please select only 1, 2, 3, or 4.")
            continue

        # At least 2 types required
        if len(selected) < 2:
            print("❌ Please select at least 2 character types.")
            continue

        break

    characters = ""

    if "1" in selected:
        characters += string.ascii_uppercase

    if "2" in selected:
        characters += string.ascii_lowercase

    if "3" in selected:
        characters += string.digits

    if "4" in selected:
        characters += string.punctuation

    password = ""

    if "1" in selected:
        password += random.choice(string.ascii_uppercase)

    if "2" in selected:
        password += random.choice(string.ascii_lowercase)

    if "3" in selected:
        password += random.choice(string.digits)

    if "4" in selected:
        password += random.choice(string.punctuation)

    remaining = length - len(password)

    for i in range(remaining):
        password += random.choice(characters)

    password_list = list(password)
    random.shuffle(password_list)
    password = "".join(password_list)

    print("\n======================================")
    print("Generated Password:")
    print(password)
    print("======================================")

    again = input("\nDo you want to generate another password? (yes/no): ")

    if again.lower() not in ["yes", "y"]:
        print("\nThank you for using Random Password Generator!")
        break