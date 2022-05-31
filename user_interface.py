"""Creates the GUI allowing users to interact with the system"""
from tkinter import Tk, Button, Label, Toplevel
from app_brain import *
from windows import Window
from testingscreen import TestingScreen
from exportform import export_form

BACKGROUND_COLOUR = "#91c9c0"
GEOMETRY = "400x700"
HEADER_FONT = ("Arial", 18, "bold")


def open_project(proj_name):
    ProjectUI(proj_name)


def open_form(form_name, proj_name):
    FormUI(form_name, proj_name)


class HomeUI(Tk):
    """This creates the Home Screen,
    can only be used once as it is a derived class of Tk and calls the mainloop()"""

    def delete_project_ui(self, project_id):
        project_button = self.nametowidget(f'project: {project_id}')
        delete_button = self.nametowidget(f'{project_id}')
        project_button.destroy()
        delete_button.destroy()
        delete_project(project_id)

    def project_button_build(self, proj_name, proj_id):
        create_button = Button(self, text=proj_name, name=f'project: {proj_id}',
                               command=lambda i=proj_name: open_project(i))
        create_button.config(width=40, height=2)
        create_button.grid(column=0, columnspan=2, row=self.row, pady=10)
        create_delete_button = Button(self, name=str(proj_id),
                                      text="X", command=lambda i=proj_id: self.delete_project_ui(i))
        create_delete_button.config(width=10, height=2)
        create_delete_button.grid(column=2, columnspan=2, row=self.row, pady=10, padx=5)
        self.row += 1

    def create_new_project(self):
        title = new_project()

        if title:
            self.project_button_build(title[0], title[1][0][0])

    def get_projects(self):
        for project in project_list:
            project_name = list(project.keys())[0]
            project_id = list(project.values())[0]
            self.project_button_build(project_name, project_id)

    def __init__(self, heading):
        super().__init__()
        self.title("Application Testing")
        self.config(pady=20, padx=20, background=BACKGROUND_COLOUR)
        self.resizable(False, False)
        self.geometry(GEOMETRY)
        self.page_title = Label(text=heading,
                                background=BACKGROUND_COLOUR,
                                font=HEADER_FONT)
        self.page_title.grid(row=1, column=0, columnspan=3, pady=20)

        # Buttons
        self.new_project_btn = Button(text="➕ New Project", command=self.create_new_project)
        self.new_project_btn.grid(row=2, column=1, columnspan=2, pady=10)
        self.new_project_btn.config(width=50, height=2)
        self.row = 3
        self.get_projects()


class ProjectUI(Window):
    """Opens a new window to explore the selected project.
    uses tkinter Toplevel to reference the root (i.e. HomeUI)"""

    def form_button_build(self, form_name, form_id):
        """Creates two buttons, one for the form, one to remove the form.
        Takes one argument of form name"""
        create_button = Button(self.this_window, name=f'form: {str(form_id)}', text=form_name,
                               command=lambda i=form_name: open_form(i, self.heading))
        create_button.config(width=40, height=2)
        create_button.grid(column=0, columnspan=2, row=self.row, pady=10)
        create_delete_button = Button(self.this_window, name=str(form_id),
                                      text="X", command=lambda i=form_id: self.delete_from_ui(i, 'form'))
        create_delete_button.config(width=10, height=2)
        create_delete_button.grid(column=2, columnspan=2, row=self.row, pady=10, padx=5)

    def get_forms(self):
        """Loops through the form list that's created in init and generates buttons on screen"""
        for form in self.form_list:
            form_name = list(form.keys())[0]
            form_id = list(form.values())[0]
            self.form_button_build(form_name, form_id)
            self.row += 1

    def create_form_button(self):
        """Calls the create_new_form function in app_brain to allow the agent to add a new form.
        This function uses the returned string to generate a new on-screen button"""
        form_name = create_new_form(self.heading)
        if form_name:
            self.form_button_build(form_name[0], form_name[1][0][0])
            self.row += 1

    def __init__(self, heading):
        super().__init__(heading, root)
        self.new_test_btn = Button(self.this_window, text="➕ Add New Test Form", command=self.create_form_button)
        self.new_test_btn.config(width=50, height=2)
        self.new_test_btn.grid(row=3, column=0, columnspan=3, pady=10)
        self.row = 4
        # SELECT
        self.form_list = [{f[1]: f[0]} for f in
                          dc.db.session.query(dc.forms_table.id,
                                              dc.forms_table.form_name).filter_by(project_name=heading).all()]
        self.get_forms()


class FormUI(Window):
    """Opens a new window to explore the selected project.
    """

    def open_test(self, test_id, test_name, description):
        print(test_id)
        window_x_y = (self.this_window.winfo_x(), self.this_window.winfo_y())
        TestingScreen(window_x_y, self.form_id, test_name, test_id, description, root)

    def test_button_build(self, test_name, test_id, test_description):
        """Creates two buttons, one for the form, one to remove the form.
        Takes one argument of form name"""
        create_button = Button(self.this_window, name=f'test: {str(test_id)}', text=test_name,
                               command=lambda i=test_id, n=test_name, d=test_description: self.open_test(i, n, d))
        create_button.config(width=30, height=2)
        create_button.grid(column=0, columnspan=2, row=self.row)
        create_delete_button = Button(self.this_window, name=str(test_id),
                                      text="X", command=lambda i=test_id: self.delete_from_ui(i, 'test'))
        create_delete_button.config(width=5, height=2)
        create_delete_button.grid(column=2, columnspan=2, row=self.row, pady=10, padx=5)

    def create_new_test(self):
        test_name = create_new_test(self.form_id)
        if test_name:
            print(test_name)
            self.test_button_build(test_name[0], test_name[1][0][0], test_name[2])
            self.row += 1

    def get_tests(self):
        for test in self.test_list:
            self.test_button_build(test[1], test[0], test[2])
            self.row += 1

    def __init__(self, heading, project):
        super().__init__(f'{project} - {heading}', root)
        self.project = project
        self.form = heading
        self.new_test_btn = Button(self.this_window, text="➕ New Test", command=self.create_new_test)
        self.new_test_btn.grid(row=2, column=0, pady=10, padx=10)
        self.new_test_btn.config(width=10, height=2)
        self.row = 3
        self.form_id = dc.db.session.query(dc.forms_table.id).filter_by(form_name=self.form,
                                                                        project_name=self.project).all()[0][0]
        self.generate_form_btn = Button(self.this_window, text="Generate PDF", background="#F06060",
                                        command=lambda form_id=self.form_id: export_form(form_id))
        self.generate_form_btn.grid(row=2, column=1, columnspan=3, pady=10)
        self.generate_form_btn.config(width=25, height=2)
        self.test_list = [t for t in
                          dc.db.session.query(dc.tests_table.id,
                                              dc.tests_table.test_name, dc.tests_table.test_description).filter_by(
                              form_id=self.form_id).all()]
        self.get_tests()


root = HomeUI("Application Tester")
