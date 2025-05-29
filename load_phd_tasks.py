import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Ensure the 'tasks' table exists with required fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        deadline TEXT,
        priority TEXT DEFAULT 'Medium',
        progress INTEGER DEFAULT 0,
        completed BOOLEAN DEFAULT 0
    )
''')

# Define the task list with description, deadline, priority, progress
phd_tasks = [
    # Year 1
    ("Attend PhD Orientation Week", "2023-10-10", "High", 100),
    ("Finalize PhD registration and administrative formalities", "2023-10-20", "High", 100),
    ("Define research area and choose supervisor(s)", "2023-11-01", "High", 100),
    ("Complete literature review", "2024-01-31", "High", 70),
    ("Attend research methodology course", "2024-02-15", "Medium", 100),
    ("Submit initial research proposal draft", "2024-03-01", "High", 80),
    ("Present proposal at internal seminar", "2024-03-15", "Medium", 60),
    ("Collect feedback from supervisor", "2024-03-25", "Medium", 50),
    ("Attend university workshops (academic writing, publishing, etc.)", "2024-04-15", "Medium", 30),
    ("Register for required coursework (if applicable)", "2024-04-30", "Low", 100),
    ("Complete ethics training (if required)", "2024-05-15", "Medium", 100),
    ("Refine and submit final research proposal", "2024-06-01", "High", 40),
    ("Create data collection plan and timeline", "2024-07-01", "Medium", 20),
    ("Attend at least one academic conference or seminar", "2024-08-15", "Medium", 0),
    ("Prepare for Year 1 review (progress report and presentation)", "2024-09-15", "High", 0),

    # Year 2
    ("Conduct data collection / experimental work", "2024-10-15", "High", 0),
    ("Begin regular supervisor meetings", "2024-11-01", "High", 10),
    ("Analyze preliminary data", "2025-01-10", "High", 0),
    ("Write and submit first conference paper", "2025-02-01", "High", 0),
    ("Present paper at conference", "2025-03-15", "Medium", 0),
    ("Apply for research funding / travel grants", "2025-04-01", "Low", 0),
    ("Attend a publishing workshop", "2025-04-15", "Low", 0),
    ("Continue data collection and refinement", "2025-06-01", "Medium", 0),
    ("Begin drafting core chapters of the thesis", "2025-07-01", "High", 0),
    ("Write and submit journal article", "2025-08-15", "High", 0),
    ("Continue attending seminars or workshops", "2025-09-01", "Low", 0),
    ("Prepare for mid-term evaluation", "2025-09-30", "High", 0),

    # Year 3
    ("Complete final round of data collection/analysis", "2025-10-15", "High", 0),
    ("Finish full draft of thesis", "2026-01-15", "High", 0),
    ("Submit draft to supervisor", "2026-02-01", "High", 0),
    ("Revise based on supervisor comments", "2026-03-01", "High", 0),
    ("Write abstract, introduction, and conclusion", "2026-03-15", "High", 0),
    ("Format thesis according to university guidelines", "2026-04-01", "Medium", 0),
    ("Submit thesis for preliminary review", "2026-05-15", "High", 0),
    ("Prepare for PhD defense", "2026-06-15", "High", 0),
    ("Defend PhD thesis", "2026-07-01", "High", 0),
    ("Submit final corrected thesis", "2026-08-01", "High", 0),
    ("Publish thesis to institutional repository", "2026-09-01", "Low", 0),
    ("Apply for graduation", "2026-09-15", "Medium", 0),
    ("Update CV and apply for postdoc/jobs", "2026-09-30", "Medium", 0),
]

# Insert the tasks into the database
for desc, deadline, priority, progress in phd_tasks:
    cursor.execute(
        '''
        INSERT INTO tasks (description, deadline, priority, progress)
        VALUES (?, ?, ?, ?)
        ''',
        (desc, deadline, priority, progress)
    )

# Save and close
conn.commit()
conn.close()

print("PhD training tasks loaded successfully.")
