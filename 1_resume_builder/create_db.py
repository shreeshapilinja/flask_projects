import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('resume_app.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS resume_app_employee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        designation TEXT NOT NULL,
        name TEXT NOT NULL,
        professional_summary TEXT NOT NULL,
        technical_skill_set TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS resume_app_project (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        title VARCHAR(100) NOT NULL,
        employee_id BIGINT NOT NULL,
        role_responsibilities TEXT NOT NULL,
        technology_used VARCHAR(100) NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES resume_app_employee (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS resume_app_employeeproject (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id BIGINT NOT NULL,
        project_id BIGINT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES resume_app_employee (id),
        FOREIGN KEY (project_id) REFERENCES resume_app_project (id)
    )
''')

# Sample employee data
employee_data = [
    ('Software Developer L2', 'Shreesha B', 'Having 4.3 years total and relevant experience on Development of Web Applications. A team player with good communication skills and eagerness to share and gain knowledge. Experience in working with Web Applications Using Laravel and Django. Working Knowledge on Linux and Windows. GIT for code management and version control. integrated Google apis/tools like Geolocation.', 'Programming and Scripting : JavaScript, PHP, HTML 5, CSS 3 \nFrameworks : Vue js, Laravel, Django \nDevelopment Tools : VsCode \nWeb API Tools : Postman \nOperating System : Linux, Windows 7/8/10, MacOS'),
    ('UI/UX Designer', 'Alexandra S', 'Passionate UI/UX designer with a keen eye for creating visually appealing and user-friendly interfaces. Proficient in Adobe Creative Suite and Sketch. Experienced in wireframing, prototyping, and conducting user research to inform design decisions.', 'Design Tools : Adobe XD, Sketch \nPrototyping : InVision \nGraphic Design : Adobe Photoshop, Illustrator \nUser Research : Surveys, Interviews')
]

# Insert employee data into the database
cursor.executemany('INSERT INTO resume_app_employee (designation, name, professional_summary, technical_skill_set) VALUES (?, ?, ?, ?)', employee_data)
conn.commit()

# Sample project data
project_data = [
    ('Time tag is a website used to fill employee timesheets. Also, the admin has an option to check all employees timesheets, filtering employees timesheets based on filters and exporting timesheets.', 'Time tag', 1, 'Laravel developer.,Developed different panels based on user role.,Timesheet filtration based on date.,Export timesheet.,CRUD operations.,UI implementation.', 'Laravel,Mysql,Javascript,Jquery,Ajax,Html,Css,Bootstrap'),
    ('Market Analysis Dashboard', 'Market Insights', 3, 'Created interactive dashboards to visualize market trends and analyze customer behavior.,Designed and developed the user interface for the online store.,Implemented responsive design and optimized user flows.', 'Data Visualization, Python, Pandas, Matplotlib, Tableau,Javascript,Jquery')
]

# Insert project data into the database
cursor.executemany('INSERT INTO resume_app_project (description, title, employee_id, role_responsibilities, technology_used) VALUES (?, ?, ?, ?, ?)', project_data)
conn.commit()

# Sample employeeproject data
employeeproject_data = [
    (1,1),
    (2,2)
]

# Link employee to project data
cursor.executemany('INSERT INTO resume_app_employeeproject (employee_id, project_id) VALUES (?, ?)', employeeproject_data)
conn.commit()

# Close the database connection
conn.close()
