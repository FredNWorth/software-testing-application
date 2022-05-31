"""All the background operations"""
import easygui
import database_connect as dc

'''List comprehension is used to create a list 
containing all the projects from the database table'''
# SELECT id, project_name FROM projects_table
project_list = [{r[1]: r[0]} for r in
                dc.db.session.query(dc.projects_table.id, dc.projects_table.project_name).all()]
all_projects = [p[0] for p in [list(k.keys()) for k in project_list]]
delete_types = {"form": "delete_form",
                "test": "delete_test",
                }


def new_project():
    """Create a new project, takes no args but will ask the user for a project name,
    The new project is returned as a string"""
    # global project_list
    new_project_input = easygui.enterbox(title="New Project",
                                         msg="Please enter a project name")
    if new_project_input:
        if new_project_input in all_projects:
            try_again = easygui.ynbox(title="Already Created", msg=f"{new_project_input} already exists, "
                                                                   f"please open it or create a new project",
                                      choices=["Try Again", "Cancel"])
            if try_again:
                new_project()
            else:
                return False

        # INSERT INTO projects_table (project_name) VALUES ('NAME OF NEW PROJECT');
        dc.db.session.add(dc.projects_table(project_name=f"{new_project_input}"))
        dc.db.session.commit()
        new_project_id = dc.db.session.query(dc.projects_table.id).filter_by(project_name=new_project_input).all()
        return new_project_input, new_project_id


def create_new_form(project) -> tuple:
    """Create a new form, this takes a project arg,
    the form created will be added to the forms_table table
    it uses the project as a reference when retrieving all the reports.
    The new form is returned as a string or False if no form name entered"""
    new_form = easygui.enterbox(title="Title",
                                msg="Please enter a title"
                                )
    if new_form:
        # INSERT INTO forms_table (project_name, form_name) VALUES ('NAME OF PROJECT', 'NAME OF FORM');
        dc.db.session.add(dc.forms_table(project_name=project, form_name=new_form))
        dc.db.session.commit()
        new_form_id = dc.db.session.query(dc.forms_table.id).filter_by(form_name=new_form, project_name=project).all()
        return new_form, new_form_id


def create_new_test(form_id) -> tuple:
    """Create a new test, this takes a form name  and a project arg,
    the test created will be added to the tests_table table along with the form id
    this is as a reference when retrieving all the reports.
    The new test is returned as a tuple"""

    print(form_id)
    new_test = easygui.enterbox(title="Test Title",
                                msg="Please enter a title"
                                )
    if new_test:
        test_description = easygui.enterbox(title="Test Description",
                                            msg="Please describe the test"
                                            )
        # INSERT INTO tests_table (test_name, test_description, form_id) VALUES
        # ('NAME OF ApplicationTester', 'DESCRIPTION', form_id);
        dc.db.session.add(dc.tests_table(test_name=new_test, test_description=test_description, form_id=form_id))
        dc.db.session.commit()
        new_test_id = dc.db.session.query(dc.tests_table.id).filter_by(test_name=new_test, form_id=form_id).all()
        return new_test, new_test_id, test_description


def delete_form(element_id):
    """Deletes a form, takes the project name and the form name as args"""
    # DELETE FROM forms_table WHERE project_name = project_name AND form_name = form_name
    dc.db.session.query(dc.forms_table).filter_by(id=element_id).delete()
    dc.db.session.commit()


def delete_project(project_id):
    """Deletes a form, takes the project name as an arg.
    This will not delete any of the forms associated with the project.
    This is to preserve them in the case that the project is deleted in error.
    If the user wishes to completely remove a project and all the tests,
    the tests need to be deleted first"""
    # May add a full erasure option in at a later date
    dc.db.session.query(dc.projects_table).filter_by(id=project_id).delete()
    dc.db.session.commit()


def delete_test(element_id):
    """Deletes a form, takes the project name and the form name as args"""
    # DELETE FROM tests_table WHERE id = id
    dc.db.session.query(dc.tests_table).filter_by(id=element_id).delete()
    dc.db.session.commit()


def delete_element(delete_type, element_id):
    """calls the appropriate delete function based on the type of thing being deleted
    **args(delete_type (i.e. form, test, test run),
    element_id (i.e. the id that will be used to remove the row from the db table))"""
    function_call = delete_types[delete_type]
    globals()[function_call](**{"element_id": element_id})


def run_test(test_id, test_number, form_id):
    """Creates a test on the database and displays it on the UI.
    **args(test_id, test_number, form_id)"""
    # TODO: Write Test to DB
    notes_of_test = easygui.enterbox(title="Notes", msg="Please type any notes about the test")
    if not notes_of_test:
        easygui.msgbox(title="Error", msg="You must write a description")
        return False
    else:
        pass_fail = easygui.choicebox(title="Pass/Fail", msg="Did the test pass?",
                                      choices=['Pass', 'Fail'])
        dc.db.session.add(dc.test_runs(test_id=test_id, form_id=form_id,
                                       test_attempt=test_number, test_details=notes_of_test, test_result=pass_fail))
        dc.db.session.commit()

        return notes_of_test, pass_fail


