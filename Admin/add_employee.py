import tkinter as tk
from tkinter import messagebox
from db_connection import get_db_connection
import datetime
import hashlib  # For password hashing

def open_add_employee(admin_id):
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

    def add_employee():
        first_name = entry_first_name.get().strip()
        last_name = entry_last_name.get().strip()
        department = entry_department.get().strip()
        designation = entry_designation.get().strip()
        salary = entry_salary.get().strip()
        email = entry_email.get().strip()
        phone_number = entry_phone_number.get().strip()
        address = entry_address.get().strip()
        current_date = datetime.datetime.now()

        # Ensure all fields are filled
        if all([first_name, last_name, department, designation, salary, email, phone_number, address]):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Generate Emp_id
                emp_id = generate_emp_id(phone_number, current_date)

                # Hash the password (set as the username here)
                password = hash_password(first_name)

                # Insert into Employees table
                query_employee = """
                    INSERT INTO Employees 
                    (Emp_id, first_name, last_name, department, designation, salary, password, email, contact, address, admin_id,joining_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_employee,
                               (emp_id, first_name, last_name, department, designation, salary, password, email, phone_number, address, admin_id, current_date.strftime('%Y-%m-%d')))

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    f"Employee {first_name} added successfully!\nGenerated Emp_id: {emp_id}"
                )
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Database Error", f"Error adding employee: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "All fields are required.")
    # Create the Tkinter form
    root = tk.Tk()
    root.title("Add New Employee")
    root.geometry("800x800")

    # Form labels and entry fields
    tk.Label(root, text="First Name").pack(pady=10)
    entry_first_name = tk.Entry(root)
    entry_first_name.pack(pady=10)

    tk.Label(root, text="Last Name").pack(pady=10)
    entry_last_name = tk.Entry(root)
    entry_last_name.pack(pady=10)

    tk.Label(root, text="Department").pack(pady=10)
    entry_department = tk.Entry(root)
    entry_department.pack(pady=10)

    tk.Label(root, text="Designation").pack(pady=10)
    entry_designation = tk.Entry(root)
    entry_designation.pack(pady=10)

    tk.Label(root, text="Salary").pack(pady=10)
    entry_salary = tk.Entry(root)
    entry_salary.pack(pady=10)

    tk.Label(root, text="Email").pack(pady=10)
    entry_email = tk.Entry(root)
    entry_email.pack(pady=10)

    tk.Label(root, text="Phone Number").pack(pady=10)
    entry_phone_number = tk.Entry(root)
    entry_phone_number.pack(pady=10)

    tk.Label(root, text="Address").pack(pady=10)
    entry_address = tk.Entry(root)
    entry_address.pack(pady=10)

    # Add Employee button
    tk.Button(root, text="Add Employee", command=add_employee).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    # Example of passing the admin_id to the function
    open_add_employee(admin_id="your_admin_id_here")
