import tkinter as tk
from logging import root
from tkinter import messagebox, ttk
from Admin.db_connection import get_db_connection
from Admin.add_employee import open_add_employee  # Ensure this is correctly imported


from tkinter import messagebox, ttk
import tkinter as tk
from Admin.db_connection import get_db_connection
from Admin.add_employee import open_add_employee  # Ensure this is correctly imported

def fetch_employee_data(admin_id):
    """Fetch employee data for the admin."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT Emp_id, first_name, last_name, department, designation, salary, email, contact, address, joining_date
            FROM Employees
            WHERE admin_id=%s
            """,
            (admin_id,),
        )
        employees = cursor.fetchall()
        conn.close()
        return employees
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch employees: {e}")
        return []

def remove_selected_employees(tree):
    """Remove selected employees from the database."""
    selected_items = tree.selection()
    ids_to_remove = [tree.item(item, 'values')[0] for item in selected_items]

    if ids_to_remove:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM Employees WHERE Emp_id IN ({})".format(
                ','.join(['%s'] * len(ids_to_remove))
            )
            cursor.execute(query, ids_to_remove)
            conn.commit()
            conn.close()

            for item in selected_items:
                tree.delete(item)

            messagebox.showinfo("Success", "Selected employee(s) removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove employees: {e}")
    else:
        messagebox.showwarning("Warning", "Please select at least one employee to remove.")

def open_employee_management(admin_id, main_frame):
    """Employee Management in the same frame."""
    # Clear the existing content of the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Employee Management", font=("Helvetica", 16)).pack(pady=10)

    columns = [
        'Emp_id', 'First_name', 'Last_name', 'Department', 'Designation',
        'Salary', 'Email', 'Contact', 'Address', 'Joining_Date'
    ]
    tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)

    for column in columns:
        tree.heading(column, text=column.replace('_', ' ').title())
        tree.column(column, anchor='center', width=100)

    employees = fetch_employee_data(admin_id)
    for employee in employees:
        tree.insert('', tk.END, values=employee)

    tree.pack(pady=20, fill="both", expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Employee", command=lambda: open_add_employee(admin_id), width=15).pack(
        side="left", padx=10)
    tk.Button(button_frame, text="Remove Employee", command=lambda: remove_selected_employees(tree), width=15).pack(
        side="left", padx=10)
