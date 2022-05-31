"""This contains the sqlite3 database information.
The database is rebuilt on launch if it does not exist."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

if not os.path.exists("../db"):
    os.mkdir("../db")
if not os.path.exists("../completed-forms"):
    os.mkdir("../completed-forms")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/project_testing.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Projects table class
class projects_table(db.Model):
    """Table to store all the different projects only requires one input: project_name"""
    id = db.Column('project_id', db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))

    def __init__(self, project_name):
        self.project_name = project_name


class forms_table(db.Model):
    id = db.Column('form_id', db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    form_name = db.Column(db.String(100))

    def __init__(self, project_name, form_name):
        self.project_name = project_name
        self.form_name = form_name


class tests_table(db.Model):
    id = db.Column('test_id', db.Integer, primary_key=True)
    form_id = db.Column(db.Integer)
    test_name = db.Column(db.String(100))
    test_description = db.Column(db.String(250))
    tests = db.Column(db.String(1000000))
    favourite = db.Column(db.String(1))

    def __init__(self, test_name, test_description, form_id, favourite='N'):
        self.test_name = test_name
        self.test_description = test_description
        self.favourite = favourite
        self.form_id = form_id


class test_runs(db.Model):
    id = db.Column('test__run_id', db.Integer, primary_key=True)
    form_id = db.Column(db.Integer)
    test_id = db.Column(db.Integer)
    test_attempt = db.Column(db.Integer)
    test_details = db.Column(db.String(250))
    test_result = db.Column(db.String(10))

    def __init__(self, form_id, test_id, test_attempt, test_details, test_result):
        self.form_id = form_id
        self.test_id = test_id
        self.test_attempt = test_attempt
        self.test_details = test_details
        self.test_result = test_result


db.create_all()
'''
Create tables on sqlite database

CREATE TABLE forms_table (
	form_id INTEGER NOT NULL, 
	project_name VARCHAR(100), 
	form_name VARCHAR(100), 
	PRIMARY KEY (form_id)
)
CREATE TABLE projects_table (
	project_id INTEGER NOT NULL, 
	project_name VARCHAR(100), 
	PRIMARY KEY (project_id)
)
CREATE TABLE tests_table (
	test_id INTEGER NOT NULL, 
	test_name VARCHAR(100),
	test_description VARCHAR(250),  
	favourite VARCHAR(1),
	PRIMARY KEY (project_id)
)
'''



