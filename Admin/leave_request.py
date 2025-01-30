import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_db_connection  # Ensure this function is implemented to connect to the database

def open_leave_requests(admin_id, main_frame):
    def fetch_leave_requests():
        """Fetch leave requests for employees under the specific admin_id."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT lr.leave_id, lr.employee_id, lr.leave_type, lr.start_date, lr.end_date, lr.status, lr.request_date
                FROM leaverequests lr
                INNER JOIN Employees e ON lr.employee_id = e.Emp_id
                WHERE e.admin_id = %s
            """, (admin_id,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch data: {e}")
            return []
        finally:
            conn.close()

    def update_leave_status(request_id, new_status):
        """Update the status of a leave request."""
        try:
            if not request_id:
                messagebox.showwarning("Warning", "Please select a leave request.")
                return

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE leaverequests
                SET status = %s, approval_date = NOW()
                WHERE leave_id = %s
            """, (new_status, request_id))
            conn.commit()
            messagebox.showinfo("Success", f"Leave request {request_id} has been {new_status.lower()}.")
            refresh_table()  # Refresh the table to reflect the updated status
        except Exception as e:
            messagebox.showerror("Error", f"Could not update status: {e}")
        finally:
            conn.close()

    def on_tree_select(event):
        """Handle the selection of a row in the Treeview."""
        selected_item = tree.selection()
        if selected_item:
            return tree.item(selected_item[0], "values")[0]  # Return the Request ID
        return None

    def refresh_table():
        """Reload the leave request data into the Treeview."""
        for row in tree.get_children():
            tree.delete(row)  # Clear existing data
        leave_requests = fetch_leave_requests()
        for request in leave_requests:
            tree.insert("", "end", values=request)

    # Clear existing widgets in the main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Title label
    tk.Label(main_frame, text="Employee Leave Requests", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Define Treeview columns
    columns = ("Request ID", "Employee ID", "Leave Type", "From Date", "To Date", "Status", "Request Date")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Bind selection event
    tree.bind("<<TreeviewSelect>>", lambda event: None)  # No direct action needed for now

    # Action buttons
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Approve", bg="green", fg="white", font=("Arial", 12),
              command=lambda: update_leave_status(on_tree_select(None), "Approved")).grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Reject", bg="red", fg="white", font=("Arial", 12),
              command=lambda: update_leave_status(on_tree_select(None), "Rejected")).grid(row=0, column=1, padx=5)

    # Populate the Treeview with data
    refresh_table()
