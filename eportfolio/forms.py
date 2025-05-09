from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        "User Name",
        validators=[
            DataRequired(message="User Name is required."),
            Length(max=64, message="User Name must be within 64 characters."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
        ],
    )
    submit = SubmitField("Login")

class AddSubjectForm(FlaskForm):
    subjectname = StringField(
        "Subject Name",
        validators=[
            DataRequired(message="Subject Name is required."),
        ],
    )
    student_id = StringField(
        "Student ID",
        validators=[DataRequired(message="Student ID is required.")]
    )
    submit = SubmitField("Submit")

class SearchSubjectForm(FlaskForm):
    search_term = StringField(
        "Search Term",
        validators=[
            DataRequired(message="Search Term is required."),
        ],
    )
    submit = SubmitField("Search")

class PortfolioForm(FlaskForm):
    entry = TextAreaField(
        "Journal Entry",
        validators=[DataRequired(message="Entry cannot be empty.")]
    )
    submit = SubmitField("Add Entry")