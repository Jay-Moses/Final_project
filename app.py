import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import hashlib
import csv
import subprocess

# File to store user credentials
USER_CREDENTIALS_FILE = "user_credentials.csv"

# Function to hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if the CSV file exists, if not create one
def initialize_user_db():
    if not os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])  # Header row

# Function to sign up a new user
def sign_up():
    username = entry_new_user.get()
    password = entry_new_pass.get()
    confirm_password = entry_confirm_pass.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty!")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    hashed_pass = hash_password(password)

    # Check if the username already exists
    with open(USER_CREDENTIALS_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                messagebox.showerror("Error", "Username already exists!")
                return

    # Store new user credentials
    with open(USER_CREDENTIALS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, hashed_pass])

    messagebox.showinfo("Success", "Account created successfully! Please log in.")
    sign_up_window.destroy()

# Function to log in
def login():
    username = entry_user.get()
    password = entry_pass.get()

    hashed_pass = hash_password(password)

    with open(USER_CREDENTIALS_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username and row[1] == hashed_pass:
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                root.destroy()  # Close login window
                open_main_application()  # Open main app
                return

    messagebox.showerror("Error", "Invalid username or password!")
def forgot_password():
    global reset_window, entry_reset_user, entry_new_password, entry_confirm_new_password
    
    reset_window = tk.Toplevel(root)
    reset_window.title("Reset Password")
    reset_window.geometry("400x300")
    reset_window.configure(bg="#2D1E3E")

    tk.Label(reset_window, text="Enter Username", bg="#2D1E3E", fg="white").pack(pady=5)
    entry_reset_user = tk.Entry(reset_window)
    entry_reset_user.pack(pady=5)

    tk.Label(reset_window, text="New Password", bg="#2D1E3E", fg="white").pack(pady=5)
    entry_new_password = tk.Entry(reset_window, show="*")
    entry_new_password.pack(pady=5)

    tk.Label(reset_window, text="Confirm New Password", bg="#2D1E3E", fg="white").pack(pady=5)
    entry_confirm_new_password = tk.Entry(reset_window, show="*")
    entry_confirm_new_password.pack(pady=5)

    tk.Button(reset_window, text="Reset Password", command=reset_password, bg="#5A3D6E", fg="white").pack(pady=10)

def reset_password():
    username = entry_reset_user.get()
    new_password = entry_new_password.get()
    confirm_password = entry_confirm_new_password.get()

    if not username or not new_password:
        messagebox.showerror("Error", "Username and password cannot be empty!")
        return

    if new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    hashed_pass = hash_password(new_password)

    users = []
    found = False

    with open(USER_CREDENTIALS_FILE, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                row[1] = hashed_pass  # Update password
                found = True
            users.append(row)

    if not found:
        messagebox.showerror("Error", "Username not found!")
        return

    with open(USER_CREDENTIALS_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(users)

    messagebox.showinfo("Success", "Password reset successfully! You can now log in.")
    reset_window.destroy()


import tkinter as tk

# Function to open sign-up window
def open_sign_up():
    global sign_up_window, entry_new_user, entry_new_pass, entry_confirm_pass
    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("400x300")

    # Set background color to a dark purple-black shade
    sign_up_window.configure(bg="#2D1E3E")  # Adjust the hex code if needed

    tk.Label(sign_up_window, text="Create Username", bg="#2D1E3E", fg="white").pack(pady=5)
    entry_new_user = tk.Entry(sign_up_window)
    entry_new_user.pack(pady=5)

    tk.Label(sign_up_window, text="Create Password", bg="#2D1E3E", fg="white").pack(pady=5)
    entry_new_pass = tk.Entry(sign_up_window, show="*")
    entry_new_pass.pack(pady=5)

    tk.Label(sign_up_window, text="Confirm Password", bg="#2D1E3E", fg="white").pack(pady=5)
    entry_confirm_pass = tk.Entry(sign_up_window, show="*")
    entry_confirm_pass.pack(pady=5)

    tk.Button(sign_up_window, text="Sign Up", command=sign_up, bg="#5A3D6E", fg="white").pack(pady=10)



# Function to open the main attendance application after login
def open_main_application():
    attendance_script = "attendance.py"
    
    if os.path.exists(attendance_script):
        try:
            subprocess.Popen(["python", attendance_script])  # Opens attendance.py
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open main application: {e}")
    else:
        messagebox.showerror("Error", f"File {attendance_script} not found!")

# Initialize user database
initialize_user_db()

# Create main login GUI
root = tk.Tk()
root.title("Login System")
root.state("zoomed")  # Set window to full screen

# Get full-screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and display image (left side)
image_path = r"C:/Users/USERR/OneDrive/Desktop/Attendance-Management_system_using_face_recognition/Project Snap/me12.png"  # Change this to your image path

if os.path.exists(image_path):
    img = Image.open(image_path)
    img = img.resize((screen_width // 2, screen_height), Image.LANCZOS)  # Half of the screen width
    img = ImageTk.PhotoImage(img)
    
    bg_label = tk.Label(root, image=img)
    bg_label.place(x=0, y=0, width=screen_width // 2, height=screen_height)  # Fixing to left side
else:
    messagebox.showerror("Error", f"Image file not found: {image_path}")

# Login Form (Right side)
frame = tk.Frame(root, bg="#1E1E2E")
frame.place(x=screen_width // 2, y=0, width=screen_width // 2, height=screen_height)  # Right half of the screen

tk.Label(frame, text="Welcome to Automated attendance", font=("Arial", 24, "bold"), bg="#1E1E2E", fg="white").pack(pady=30)
tk.Label(frame, text="")
tk.Label(frame, text="")
tk.Label(frame, text="")
tk.Label(frame, text="")
tk.Label(frame, text="")
tk.Label(frame, text="login", font=("Arial", 24, "bold"), bg="#1E1E2E", fg="white").pack(pady=30)
tk.Label(frame, text="Username", font=("Arial", 14), bg="#1E1E2E", fg="white").pack(pady=5)
entry_user = tk.Entry(frame, font=("Arial", 14))
entry_user.pack(pady=5, ipadx=10, ipady=5)

tk.Label(frame, text="Password", font=("Arial", 14), bg="#1E1E2E", fg="white").pack(pady=5)
entry_pass = tk.Entry(frame, font=("Arial", 14), show="*")
entry_pass.pack(pady=5, ipadx=10, ipady=5)

tk.Button(frame, text="Login", font=("Arial", 14), bg="#332763", fg="white", command=login).pack(pady=15, ipadx=20, ipady=5)
tk.Button(frame, text="Sign Up", font=("Arial", 14), bg="#2196F3", fg="white", command=open_sign_up).pack(pady=5, ipadx=20, ipady=5)
tk.Button(frame, text="Forgot Password?", font=("Arial", 12), bg="#FF9800", fg="white", command=forgot_password).pack(pady=5, ipadx=20, ipady=5)
root.mainloop()
