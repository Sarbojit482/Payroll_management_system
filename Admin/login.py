import tkinter as tk
from tkinter import ttk, messagebox
from Admin.dashboard import open_dashboard
from Admin.db_connection import get_db_connection
import hashlib

# Utility Function: Center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (width // 2)
    y_coordinate = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

# Forgot Password Functionality
def forgot_password():
    def reset_password():
        email = entry_email.get()
        new_password = entry_new_password.get()
        confirm_password = entry_confirm_password.get()

        if email and new_password and confirm_password:
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT admin_id FROM admin WHERE email=%s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                update_query = "UPDATE admin SET password=%s WHERE email=%s"
                cursor.execute(update_query, (hashed_password, email))
                conn.commit()
                messagebox.showinfo("Success", "Password reset successfully!")
                forgot_password_window.destroy()
            else:
                messagebox.showerror("Error", "Email not found!")
            conn.close()
        else:
            messagebox.showerror("Error", "All fields are required.")

    forgot_password_window = tk.Toplevel()
    forgot_password_window.title("Forgot Password")
    center_window(forgot_password_window, 400, 300)

    frame = ttk.Frame(forgot_password_window, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Forgot Password", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
    ttk.Label(frame, text="Email:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
    entry_email = ttk.Entry(frame, width=30)
    entry_email.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="New Password:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=5)
    entry_new_password = ttk.Entry(frame, show="*", width=30)
    entry_new_password.grid(row=2, column=1, pady=5)

    ttk.Label(frame, text="Confirm Password:", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w", pady=5)
    entry_confirm_password = ttk.Entry(frame, show="*", width=30)
    entry_confirm_password.grid(row=3, column=1, pady=5)

    reset_button = ttk.Button(frame, text="Reset Password", command=reset_password)
    reset_button.grid(row=4, column=0, columnspan=2, pady=20)


#Login Functionality
def login():
    def authenticate():
        username = entry_username.get()
        password = entry_password.get()

        if username and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "SELECT admin_id FROM admin WHERE username=%s AND password=%s"
            cursor.execute(query, (username, hashed_password))
            result = cursor.fetchone()

            if result:
                admin_id = result[0]
                messagebox.showinfo("Success", "Login Successful!")
                root.destroy()
                open_dashboard(admin_id)  # Pass the admin_id to the dashboard
            else:
                messagebox.showerror("Error", "Invalid credentials")
            conn.close()
        else:
            messagebox.showerror("Error", "All fields are required.")

    root = tk.Tk()
    root.title("Admin Login")
    center_window(root, 400, 400)
    root.configure(bg="#2C3E50")

    frame = ttk.Frame(root, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Admin Login", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
    ttk.Label(frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
    entry_username = ttk.Entry(frame, width=30)
    entry_username.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=5)
    entry_password = ttk.Entry(frame, show="*", width=30)
    entry_password.grid(row=2, column=1, pady=5)

    login_button = ttk.Button(frame, text="Login", command=authenticate)
    login_button.grid(row=3, column=0, columnspan=2, pady=20)

    forgot_password_button = ttk.Button(frame, text="Forgot Password", command=forgot_password)
    forgot_password_button.grid(row=4, column=0, columnspan=2)

    root.mainloop()

# Run the login screen
if __name__ == "__main__":
    login()
