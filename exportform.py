import datetime
from fpdf import FPDF
import database_connect as dc
import easygui


def export_form(form_id):
    """Generates a PDF of the information collected for the form
    **args(form_id)"""

    form_name = dc.db.session.query(dc.forms_table.form_name).filter_by(id=form_id).one()[0]
    project_name = dc.db.session.query(dc.forms_table.project_name).filter_by(id=form_id).one()[0]
    tests = dc.db.session.query(dc.tests_table.test_name,
                                dc.tests_table.id,
                                dc.tests_table.test_description).filter_by(form_id=form_id).all()

    tester_name = easygui.enterbox(title="Tester Name", msg="Please enter the name of the tester")
    if tester_name:
        easygui.msgbox("Your PDF has been generated")
    else:
        return False
    today = datetime.date.today().strftime("%d-%m-%Y")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14, style="BU")
    pdf.cell(200, 10, txt="Testing Form", ln=1, align='C')
    pdf.cell(200, 10, ln=2, txt='')

    # Build the information
    pdf.set_font("Arial", size=12)
    pdf.cell(60, 10, border=1, txt="Project Name", align='L')
    pdf.cell(60, 10, border=1, txt=project_name, ln=1)

    pdf.cell(60, 10, border=1, txt="Test Name", align='L')
    pdf.cell(60, 10, border=1, txt=form_name, ln=1)

    pdf.cell(60, 10, border=1, txt="Tester", align='L')
    pdf.cell(60, 10, border=1, txt=tester_name, ln=1)

    pdf.cell(60, 10, border=1, txt="Date", align='L')
    pdf.cell(60, 10, border=1, txt=today, ln=1)

    pdf.cell(200, 20, ln=2, txt='')

    # Loop through the tests to populate the below
    for test in tests:
        runs = 1
        test_title = test[0]
        test_description = test[2]
        test_runs = dc.db.session.query(dc.test_runs).filter_by(test_id=test[1]).all()

        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(60, 10, border=0, txt=test_title, align='L')
        pdf.ln()
        pdf.cell(190, 10, border=1, txt="Description", align='C')
        pdf.ln()
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 15, border=1, txt=test_description, align='L')
        for run in test_runs:
            pdf.ln()
            pdf.cell(20, 10, border=1, txt=f"Test {runs}", align='L')
            pdf.cell(150, 10, border=1, txt=run.test_details)
            if run.test_result == 'Pass':
                pdf.set_text_color(0, 255, 0)
            else:
                pdf.set_text_color(255, 0, 0)
            pdf.cell(20, 10, border=1, txt=run.test_result.upper())
            pdf.set_text_color(0, 0, 0)
            runs += 1
        pdf.ln(20)

    pdf.output(f"../completed-forms/{project_name}-{form_name}-{today}.pdf", dest='F')
