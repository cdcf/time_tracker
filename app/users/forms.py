__author__ = 'Cedric Da Costa Faro'

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import Optional, Length, Required, EqualTo


# We define here the profile data of a user
class ProfileForm(Form):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = TextAreaField('Location', validators=[Optional()])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[Required(),
                                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')
