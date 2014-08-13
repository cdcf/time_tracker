__author__ = 'Cedric Da Costa Faro'

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional, Length


# We define here the profile data of a user
class ProfileForm(Form):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')