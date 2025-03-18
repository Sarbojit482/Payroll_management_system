import tkinter as tk
from tkinter import ttk, messagebox
from Admin.db_connection import get_db_connection
from Admin.add_employee import open_add_employee
from Admin.employee_management import open_employee_management
from Admin.Profile import admin_profile_page
from Admin.leave_request import open_leave_requests
from Admin.setting import open_settings
from Admin.support import open_help_support
from Admin.view_attendance import open_admin_attendance
from Admin.leave import open_leave_request


def open_logout():
    """Logout Function."""
    confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if confirm:
        exit()


def open_dashboard(admin_id):
    """Admin Dashboard."""
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("1000x600")

    # Navigation Frame
    nav_frame = tk.Frame(root, bg="lightgray", width=200)
    nav_frame.pack(side="left", fill="y")

    # Main Content Frame
    global main_frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side="right", expand=True, fill="both")

    # Placeholder Content
    def clear_and_add_placeholder():
        for widget in main_frame.winfo_children():
            widget.destroy()
        placeholder_label = tk.Label(main_frame, text="Main Content Area", font=("Helvetica", 16), bg="white")
        placeholder_label.pack(pady=20)

    clear_and_add_placeholder()

    # Scrollable Navigation
    canvas = tk.Canvas(nav_frame, bg="lightgray", width=200)
    scrollbar = ttk.Scrollbar(nav_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="lightgray")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="y", expand=True)
    scrollbar.pack(side="right", fill="y")

    def add_nav_button(frame, text, command):
        """Add navigation button."""
        tk.Button(frame, text=text, command=command, width=20).pack(pady=5)

    # Navigation Buttons
    add_nav_button(scrollable_frame,"Home",lambda:clear_and_add_placeholder())
    add_nav_button(scrollable_frame, "Add New Employee", lambda: open_add_employee(admin_id,main_frame))
    add_nav_button(scrollable_frame, "View Attendance", lambda: open_admin_attendance(admin_id,main_frame))
    add_nav_button(scrollable_frame, "View Leave Requests", lambda: open_leave_requests(admin_id, main_frame))
    add_nav_button(scrollable_frame, "Employee Management", lambda: open_employee_management(admin_id, main_frame))
    add_nav_button(scrollable_frame,"Leave",lambda :open_leave_request(admin_id,main_frame))
    add_nav_button(scrollable_frame, "Profile", lambda: admin_profile_page(admin_id,main_frame))
    add_nav_button(scrollable_frame, "Help/Support",lambda :open_help_support(main_frame))
    add_nav_button(scrollable_frame, "Logout", open_logout)

    root.mainloop()


if __name__ == "__main__":
    open_dashboard(admin_id="1")  # Replace "1" with actual admin_id
