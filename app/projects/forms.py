__author__ = 'Cedric Da Costa Faro'

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional, Length, Required
from wtforms.fields.html5 import DateField


class ProfileForm(Form):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')


class ProjectForm(Form):
    title = StringField('Title', validators=[Required(), Length(1, 128)])
    description = TextAreaField('Desciption')
    date = DateField('Date', format='%d/%m/%Y')
    submit = SubmitField('Submit')