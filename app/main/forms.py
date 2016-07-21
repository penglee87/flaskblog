from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required,  Email, Regexp, EqualTo
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PostForm(Form):
    title = StringField("The title", validators=[Required()])
    summary = StringField("The summary", validators=[Required()])
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

class EditForm(Form):
    title = StringField("The title", validators=[Required()])
    summary = StringField("The summary", validators=[Required()])
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')
    delete = SubmitField('Delete')


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')