from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    employee_identifier = request.form['employee_identifier']

    # Fetch employee details from the database based on employee ID or name
    conn = sqlite3.connect('resume_app.db')
    cursor = conn.cursor()

    query = '''
        SELECT e.id, e.name, e.designation, e.professional_summary, e.technical_skill_set
        FROM resume_app_employee e
        WHERE e.id = ? OR e.name = ?
    '''
    cursor.execute(query, (employee_identifier, employee_identifier))
    employee = cursor.fetchone()

    if employee:
        employee_id = employee[0]
        # Fetch projects related to the employee
        cursor.execute('SELECT * FROM resume_app_employeeproject WHERE employee_id = ?', (employee_id,))
        employeeprojects = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", 'B', size=14)  # Set bold font style for headings
        pdf.cell(200, 10, "PACE WISDOM SOLUTIONS PVT. LTD.", ln=True, align='C')
        pdf.ln(8)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Name: {employee[1]}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Designation: {employee[2]}", ln=True)
        pdf.ln(6)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Professional Summary:", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 10, employee[3])
        pdf.ln(6)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Technical Skill Set", ln=True)
        pdf.set_font("Arial", size=11)

        techskills = employee[4].split('\n')
        for skill in techskills:
            pdf.cell(13)
            pdf.cell(0, 10, f"- {skill}", ln=True)
        pdf.ln(6)

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Professional Projects", ln=True)
        pdf.set_font("Arial", size=12)
        i = 1
        for employeeproject in employeeprojects:
            project_id = employeeproject[1]
            cursor.execute('SELECT * FROM resume_app_project WHERE id = ?', (project_id,))
            project = cursor.fetchone()

            pdf.set_font("Arial", 'B', 13)
            pdf.cell(200, 10, f"Project {i}: {project[2]}", ln=True)
            i = i + 1
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 10, f"- Technology used: {project[5]}", ln=True)

            pdf.set_font("Arial", 'B', 11)
            pdf.cell(200, 10, "Description:", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 10, project[1])

            pdf.set_font("Arial", 'B', 11)
            pdf.cell(200, 10, f"Role and Responsibilities:", ln=True)
            pdf.set_font("Arial", size=11)
            roles_responsibilities = project[4].split(',')
            for role in roles_responsibilities:
                pdf.cell(13)
                pdf.cell(0, 10, f"- {role}", ln=True)
            pdf.ln(5)

        output_dir = os.path.join(os.getcwd(), 'pdf_output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pdf_output_path = os.path.join(output_dir, f"resume_{employee_id}.pdf")
        pdf.output(pdf_output_path)

        return send_file(pdf_output_path, as_attachment=True)
    else:
        return "Employee not found."
    
if __name__ == '__main__':
    app.run(debug=True)
