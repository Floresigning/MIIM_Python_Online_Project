from tabulate import tabulate
from datetime import datetime
import sqlite3

# ANSI escape codes for terminal color
RED = "\033[91m"
RESET = "\033[0m"

# Initialize the database
def initialize_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            deadline TEXT,
            priority TEXT,
            progress TEXT DEFAULT '0',
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Add a new task
def add_task():
    description = input("Enter task description: ").strip()
    deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
    priority = input("Enter priority (Low, Medium, High): ").strip().capitalize()
    progress = input("Enter progress (0–100%): ").strip()
    completed = 1 if progress == "100" else 0

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (description, deadline, priority, progress, completed) VALUES (?, ?, ?, ?, ?)",
        (description, deadline, priority, progress, completed)
    )
    conn.commit()
    conn.close()
    print("✅ Task added successfully.\n")

# View all tasks sorted by deadline and priority
def view_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tasks
        ORDER BY 
            deadline ASC,
            CASE 
                WHEN priority = 'High' THEN 1
                WHEN priority = 'Medium' THEN 2
                WHEN priority = 'Low' THEN 3
                ELSE 4
            END
    """)
    tasks = cursor.fetchall()
    conn.close()

    today = datetime.today().date()
    table_data = []

    for task in tasks:
        task_id, description, deadline, priority, progress, completed = task
        status = "✅" if completed else "❌"

        is_overdue = False
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            is_overdue = (deadline_date < today) and not completed
        except ValueError:
            pass

        overdue_text = f"{RED}⚠️OVERDUE{RESET}" if is_overdue else ""

        table_data.append([
            task_id, description, deadline, priority, f"{progress}%", status, overdue_text
        ])

    headers = ["ID", "Description", "Deadline", "Priority", "Progress", "Done", "Note"]
    print("\n=== PhD PROGRAMME TASK MANAGER  ===")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Search and filter tasks
def search_or_filter_tasks():
    print("\n=== SEARCH / FILTER TASKS ===")
    print("1. Search by keyword")
    print("2. Show overdue tasks")
    print("3. Show completed tasks")
    print("4. Show incomplete tasks")
    print("5. Back to main menu")

    choice = input("Choose an option: ").strip()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    today = datetime.today().date()
    table_data = []

    if choice == "1":
        keyword = input("Enter keyword to search in description: ").strip().lower()
        cursor.execute("SELECT * FROM tasks WHERE LOWER(description) LIKE ?", (f"%{keyword}%",))
    elif choice == "2":
        cursor.execute("SELECT * FROM tasks")
    elif choice == "3":
        cursor.execute("SELECT * FROM tasks WHERE completed = 1")
    elif choice == "4":
        cursor.execute("SELECT * FROM tasks WHERE completed = 0")
    elif choice == "5":
        conn.close()
        return
    else:
        print("❌ Invalid choice.\n")
        conn.close()
        return

    tasks = cursor.fetchall()
    conn.close()

    for task in tasks:
        task_id, description, deadline, priority, progress, completed = task
        status = "✅" if completed else "❌"

        is_overdue = False
        try:
            deadline_date = datetime.strptime(deadline, "YYYY-MM-DD").date()
            is_overdue = (deadline_date < today) and not completed
        except ValueError:
            pass

        if choice == "2" and not is_overdue:
            continue

        overdue_text = f"{RED} ⚠️ OVERDUE{RESET}" if is_overdue else ""

        table_data.append([
            task_id, description, deadline, priority, f"{progress}%", status, overdue_text
        ])

    headers = ["ID", "Description", "Deadline", "Priority", "Progress", "Done", "Note"]
    print("\n=== FILTERED TASKS ===")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Mark task as complete
def mark_complete():
    view_tasks()
    task_id = input("Enter task ID to mark as complete: ").strip()
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1, progress = '100' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("✅ Task marked as complete.\n")

# Edit a task
def edit_task():
    view_tasks()
    task_id = input("Enter task ID to edit: ").strip()
    description = input("New description (leave blank to keep current): ").strip()
    deadline = input("New deadline (YYYY-MM-DD, leave blank to keep current): ").strip()
    priority = input("New priority (Low, Medium, High, leave blank to keep current): ").strip().capitalize()
    progress = input("New progress (0–100%, leave blank to keep current): ").strip()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print("❌ Task not found.\n")
        return

    new_description = description if description else task[1]
    new_deadline = deadline if deadline else task[2]
    new_priority = priority if priority else task[3]
    new_progress = progress if progress else task[4]
    new_completed = 1 if new_progress == "100" else 0

    cursor.execute("""
        UPDATE tasks 
        SET description = ?, deadline = ?, priority = ?, progress = ?, completed = ?
        WHERE id = ?
    """, (new_description, new_deadline, new_priority, new_progress, new_completed, task_id))
    conn.commit()
    conn.close()
    print("✏️ Task updated successfully.\n")


# Update progress
def update_progress():
    view_tasks()
    task_id = input("Enter task ID to update progress: ").strip()
    new_progress = input("Enter new progress (0–100): ").strip()
    if not new_progress.isdigit() or not (0 <= int(new_progress) <= 100):
        print("❌ Invalid progress value.\n")
        return

    new_completed = 1 if new_progress == "100" else 0

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET progress = ?, completed = ?
        WHERE id = ?
    """, (new_progress, new_completed, task_id))
    conn.commit()
    conn.close()
    print("📈 Progress updated.\n")

# Delete a task
def delete_task():
    view_tasks()
    task_id = input("Enter task ID to delete: ").strip()
    confirm = input("Are you sure you want to delete this task? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Deletion canceled.\n")
        return

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("🗑️ Task deleted.\n")

# Main menu
def menu():
    initialize_db()
    while True:
        print("\n=== TASK MANAGER ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Edit Task")
        print("5. Update Progress")
        print("6. Delete Task")
        print("7. Search / Filter Tasks")
        print("8. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_complete()
        elif choice == "4":
            edit_task()
        elif choice == "5":
            update_progress()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            search_or_filter_tasks()
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice, please try again.\n")

# Run the program
if __name__ == "__main__":
    menu()
