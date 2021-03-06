"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print "Student: {first} {last}\nGitHub account: {acct}".format(
        first=row[0], last=row[1], acct=row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """
        INSERT INTO students (first_name, last_name, github)
        VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name,
                               'github': github})
    db.session.commit()

    print "{} {} with GitHub username: {} has been added to database!".format(
        first_name, last_name, github)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
        SELECT title, description, max_grade
        FROM projects
        WHERE title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})

    row = db_cursor.fetchone()

    print "Project: {title}\nDescription: {description}\nMax Grade: {max}".format(
        title=row[0], description=row[1], max=row[2])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """
        SELECT project_title, grade
        FROM grades
        WHERE project_title = :title AND student_github = :github
        """

    db_cursor = db.session.execute(QUERY, {'title': title, 'github': github})

    row = db_cursor.fetchone()

    print "Project: {title}\nGrade: {grade}".format(
        title=row[0], grade=row[1])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
        INSERT INTO grades (student_github, project_title, grade)
        VALUES (:github, :title, :grade)
        """

    db.session.execute(QUERY, {'github': github,
                               'title': title,
                               'grade': grade})
    db.session.commit()

    print "{} has been given a grade of: {} on {}".format(
        github, grade, title)


def make_new_project(project_title, description, max_grade):
    """Add a new project and print confirmation.

    Given a project_title, description and max_grade, add project to the
    database and print a confirmation message.
    """
    QUERY = """
        INSERT INTO projects (title, description, max_grade)
        VALUES (:title, :description, :max_grade)
        """

    db.session.execute(QUERY, {'title': project_title, 'description': description,
                               'max_grade': max_grade})
    db.session.commit()

    print "{} with Max grade: {} has been added to database!".format(
        project_title, max_grade)


def get_all_grades(github):
    """Given a GitHub name, print all the grades of the student."""
    QUERY = """
        SELECT project_title, grade
        FROM grades
        WHERE student_github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    for row in db_cursor:
        print "Project: {title} Grade: {grade}\n".format(
            title=row[0], grade=row[1])


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "assign":
            github, title, grade = args
            assign_grade(github, title, grade)

        elif command == "grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."


if __name__ == "__main__":
    connect_to_db(app)

    #handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
