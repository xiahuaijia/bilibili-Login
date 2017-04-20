from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Name', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])

class SigupForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password0 = PasswordField('Password0', validators=[DataRequired()])
    password1 = PasswordField('Password1', validators=[DataRequired()])

class VerCode(FlaskForm):
    vercode = StringField('Vercode', validators=[DataRequired()])
