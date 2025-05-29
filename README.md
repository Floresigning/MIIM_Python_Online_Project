# PhD Programme Task Manager (CLI Version)

A simple command-line interface (CLI) task manager designed to help PhD students organize, track, and manage their PhD tasks effectively.  
The application stores tasks in an SQLite database and supports adding, viewing, editing, deleting, and filtering tasks, with visual indicators for task completion and overdue status.

---

## Features

- Add new tasks with description, deadline, priority, progress, and completion status.
- View all tasks sorted by deadline and priority.
- Mark tasks as completed.
- Edit task details and update progress.
- Delete tasks.
- Search and filter tasks by keyword, completion status, and overdue status.
- Overdue tasks are clearly marked in red.
- Stores data persistently using a local SQLite database (`tasks.db`).

---

## Prerequisites

- Python 3.6 or higher installed  
- `tabulate` library for pretty-printing tables  
- SQLite (included in Python's standard library)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/floresigning/MIIM_Python_Online_Project.git
   cd MIIM_Python_Online_Project
   ```

2. **(Optional but recommended) Create a virtual environment and activate it:**

  
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python load_phd_tasks.py      # Load initial PhD tasks (run only once)
   python UALG_PhD_Programme_Task_Manager.py
   ```

---

## Usage

* Follow the on-screen menu to add, view, edit, delete, and search/filter your tasks.
* Use the progress field (0–100%) to track task completion; tasks marked 100% are automatically set as completed.
* Overdue tasks (past their deadline and not completed) will be highlighted in red for easy identification.

---

## Database

* The app uses a SQLite database file named `tasks.db` located in the project directory.
* The database is created automatically on the first run if it does not exist.

---

## Contributing

Contributions are welcome! Feel free to fork the repository, create feature branches, and submit pull requests.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or feedback, please contact **Jeannine Flore Signing Mananfouet** at [floresigning@yahoo.fr](mailto:floresigning@yahoo.fr).
