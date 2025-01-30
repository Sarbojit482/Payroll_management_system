import tkinter as tk
from tkinter import ttk, messagebox
from Admin.db_connection import get_db_connection
import hashlib
from datetime import datetime

# Utility Function: Center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (width // 2)
    y_coordinate = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def register_admin():
    def register():
        username = entry_username.get()
        contact = entry_contact.get()
        password = entry_password.get()
        email = entry_email.get()

        def hash_password(password):
            """Hashes the password using SHA-256."""
            return hashlib.sha256(password.encode()).hexdigest()

        def generate_emp_id(contact, current_date):
            """Generates a unique Emp_id."""
            # Extract the last 4 digits of the contact number
            contact_last4 = contact[-4:] if len(contact) >= 4 else contact
            # Format the date as YYYYMMDD
            date_str = current_date.strftime('%Y%m%d')
            # Combine date and contact's last 4 digits
            return f"{date_str}{contact_last4}"

        if username and contact and password and email:
            try:
                # Hash the password
                hashed_password = hash_password(password)

                # Generate admin_id and date_of_creation
                current_date = datetime.now()
                admin_id = generate_emp_id(contact, current_date)
                date_of_creation = current_date.strftime('%Y-%m-%d %H:%M:%S')

                # Insert data into the database
                conn = get_db_connection()
                cursor = conn.cursor()
                query = """
                    INSERT INTO Admin (admin_id, username, contact, password, email, date_of_creation)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (admin_id, username, contact, hashed_password, email, date_of_creation))
                conn.commit()

                messagebox.showinfo("Success", "Registration Successful!")
                root.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "All fields are required.")

    root = tk.Tk()
    root.title("Admin Registration")
    center_window(root, 400, 500)
    root.configure(bg="#2C3E50")

    frame = ttk.Frame(root, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(frame, text="Admin Registration", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
    ttk.Label(frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
    entry_username = ttk.Entry(frame, width=30)
    entry_username.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="Contact:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=5)
    entry_contact = ttk.Entry(frame, width=30)
    entry_contact.grid(row=2, column=1, pady=5)

    ttk.Label(frame, text="Password:", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w", pady=5)
    entry_password = ttk.Entry(frame, show="*", width=30)
    entry_password.grid(row=3, column=1, pady=5)

    ttk.Label(frame, text="Email:", font=("Helvetica", 12)).grid(row=4, column=0, sticky="w", pady=5)
    entry_email = ttk.Entry(frame, width=30)
    entry_email.grid(row=4, column=1, pady=5)

    register_button = ttk.Button(frame, text="Register", command=register)
    register_button.grid(row=5, column=0, columnspan=2, pady=20)

    root.mainloop()
