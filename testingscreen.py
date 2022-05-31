from tkinter import Label, Toplevel, Button
from app_brain import run_test
import database_connect as dc


class TestingScreen:
    # TODO: Add edit comment and delete test run

    def get_previous_runs(self):
        for test in self.test_runs_list:
            self.add_test_ui(test)

    def add_test_ui(self, test_result):
        font = ('Ariel', 12, 'bold')
        test_label = Label(self.test_details, text=f"Test {self.test_number}",
                           font=font, background="white", borderwidth=1)
        test_description_label = Label(self.test_details, text=test_result[0],
                                       font=font, background="white", highlightcolor="black",
                                       highlightthickness=2, wraplength=250
                                       )
        test_result_label = Label(self.test_details, text=test_result[1],
                                  font=font, background="white", borderwidth=1)
        test_label.grid(row=self.test_row, column=0)
        test_description_label.grid(row=self.test_row, column=1, columnspan=4)
        test_result_label.grid(row=self.test_row, column=5)
        self.test_row += 1
        self.test_number += 1

    def run_a_test(self):
        test_result = run_test(self.test_id, self.test_number, self.form_id)
        if test_result:
            self.add_test_ui(test_result)

    def __init__(self, window_x_y, form_id, test_name, test_id, description, root):
        self.test_runs_list = dc.db.session.query(dc.test_runs.test_details, dc.test_runs.test_result).filter_by\
            (form_id=form_id, test_id=test_id).all()
        print(self.test_runs_list)
        self.window_x_y = window_x_y
        self.form_id = form_id
        self.test_name = test_name
        self.test_id = test_id
        self.test_list = [t for t in
                          dc.db.session.query(dc.tests_table.id,
                                              dc.tests_table.test_name, dc.tests_table.test_description).filter_by(
                              form_id=self.form_id).all()]
        self.test_description = description
        self.test_row = 4
        self.test_number = 1
        self.test_geometry = f"800x700+{int(window_x_y[0]) + 400}+{window_x_y[1]}"
        self.test_details = Toplevel(root, background="white", name="run tests", padx=20, pady=20)
        self.test_details.geometry(self.test_geometry)
        self.test_details.title(test_name)
        self.test_title = Label(self.test_details, text=test_name, justify="left",
                                font=("Arial", 24, "bold"), background="white")
        self.test_title.grid(row=0, column=0)
        self.test_description = Label(self.test_details, text=f'\n{self.test_description}\n', justify="left",
                                      font=("Arial", 14, "italic"), background="white")
        self.test_description.grid(row=1, column=0, columnspan=6)
        self.run_test_button = Button(self.test_details, text="Run Test", font=("Ariel", 12, "bold"),
                                      width=10, height=2, background="#F3B562",
                                      command=self.run_a_test)
        self.run_test_button.grid(row=3, column=0, pady=10)
        self.get_previous_runs()
