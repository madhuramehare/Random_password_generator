import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = string.punctuation

AMBIGUOUS = "0Ol1I"

def generate_password():
    try:
        length = length_var.get()

        selected_sets = []

        if uppercase_var.get():
            selected_sets.append(UPPERCASE)

        if lowercase_var.get():
            selected_sets.append(LOWERCASE)

        if numbers_var.get():
            selected_sets.append(NUMBERS)

        if symbols_var.get():
            selected_sets.append(SYMBOLS)

        if len(selected_sets) < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least 2 character types."
            )
            return

        if length < len(selected_sets):
            messagebox.showerror(
                "Invalid Length",
                "Password length is too short for the selected character types."
            )
            return

        filtered_sets = []

        for char_set in selected_sets:
            if ambiguous_var.get():
                char_set = "".join(
                    char for char in char_set
                    if char not in AMBIGUOUS
                )

            filtered_sets.append(char_set)

        for char_set in filtered_sets:
            if not char_set:
                messagebox.showerror(
                    "Error",
                    "A selected character type has no available characters."
                )
                return

        character_pool = "".join(filtered_sets)

        password_characters = []

        for char_set in filtered_sets:
            password_characters.append(
                secrets.choice(char_set)
            )

        for _ in range(length - len(password_characters)):
            password_characters.append(
                secrets.choice(character_pool)
            )

        for i in range(len(password_characters) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_characters[i], password_characters[j] = (
                password_characters[j],
                password_characters[i]
            )

        password = "".join(password_characters)

        password_var.set(password)

        pyperclip.copy(password)

        update_strength(length, len(selected_sets))

        add_to_history(password)

        status_var.set("Password generated and copied to clipboard!")

    except Exception as error:
        messagebox.showerror("Error", str(error))

def update_strength(length, diversity):
    score = 0

    if length >= 8:
        score += 1

    if length >= 12:
        score += 1

    if length >= 16:
        score += 1

    if diversity >= 2:
        score += 1

    if diversity >= 3:
        score += 1

    if diversity == 4:
        score += 1

    if score <= 2:
        strength = "Weak"
        strength_label.config(text="Strength: Weak")
        strength_bar.config(width=100)

    elif score <= 4:
        strength = "Medium"
        strength_label.config(text="Strength: Medium")
        strength_bar.config(width=180)

    else:
        strength = "Strong"
        strength_label.config(text="Strength: Strong")
        strength_bar.config(width=260)

history = []

def add_to_history(password):
    history.insert(0, password)

    if len(history) > 5:
        history.pop()

    history_list.delete(0, tk.END)

    for item in history:
        history_list.insert(tk.END, item)

def copy_password():
    password = password_var.get()

    if password:
        pyperclip.copy(password)
        status_var.set("Password copied to clipboard!")
    else:
        messagebox.showwarning(
            "No Password",
            "Please generate a password first."
        )
root = tk.Tk()

root.title("Advanced Random Password Generator")
root.geometry("600x700")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Random Password Generator",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=15)

length_frame = tk.Frame(root)
length_frame.pack(pady=10)

tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 12)
).pack(side=tk.LEFT, padx=5)

length_var = tk.IntVar(value=12)

length_spinbox = tk.Spinbox(
    length_frame,
    from_=8,
    to=50,
    textvariable=length_var,
    width=5,
    font=("Arial", 12)
)
length_spinbox.pack(side=tk.LEFT)

type_frame = tk.LabelFrame(
    root,
    text="Character Types",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=10
)
type_frame.pack(pady=10, padx=30, fill="x")

uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    type_frame,
    text="Uppercase (A-Z)",
    variable=uppercase_var
).pack(anchor="w")

tk.Checkbutton(
    type_frame,
    text="Lowercase (a-z)",
    variable=lowercase_var
).pack(anchor="w")

tk.Checkbutton(
    type_frame,
    text="Numbers (0-9)",
    variable=numbers_var
).pack(anchor="w")

tk.Checkbutton(
    type_frame,
    text="Symbols (!@#$%)",
    variable=symbols_var
).pack(anchor="w")

security_frame = tk.LabelFrame(
    root,
    text="Security Options",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=10
)
security_frame.pack(pady=10, padx=30, fill="x")

ambiguous_var = tk.BooleanVar(value=False)

tk.Checkbutton(
    security_frame,
    text="Exclude ambiguous characters (0, O, l, 1, I)",
    variable=ambiguous_var
).pack(anchor="w")

password_var = tk.StringVar()

password_entry = tk.Entry(
    root,
    textvariable=password_var,
    font=("Arial", 16),
    justify="center",
    width=38
)
password_entry.pack(pady=15)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

generate_button = tk.Button(
    button_frame,
    text="Generate Password",
    command=generate_password,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
)
generate_button.pack(side=tk.LEFT, padx=5)

copy_button = tk.Button(
    button_frame,
    text="Copy to Clipboard",
    command=copy_password,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
)
copy_button.pack(side=tk.LEFT, padx=5)

strength_label = tk.Label(
    root,
    text="Strength: Not Generated",
    font=("Arial", 12, "bold")
)
strength_label.pack(pady=10)

strength_bar = tk.Label(
    root,
    text="",
    bg="green",
    width=0,
    height=1
)
strength_bar.pack()

history_frame = tk.LabelFrame(
    root,
    text="Last 5 Generated Passwords",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)
history_frame.pack(
    pady=15,
    padx=30,
    fill="both"
)

history_list = tk.Listbox(
    history_frame,
    height=5,
    width=50,
    font=("Courier", 11)
)
history_list.pack()

status_var = tk.StringVar(
    value="Ready to generate a password."
)

status_label = tk.Label(
    root,
    textvariable=status_var,
    font=("Arial", 10)
)
status_label.pack(pady=10)

root.mainloop()