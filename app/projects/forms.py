__author__ = 'Cedric Da Costa Faro'

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional, Length, Required
from wtforms.fields.html5 import DateField


# We define here the profile data of a user
class ProfileForm(Form):
    name = StringField('Name', validators=[Optional(), Length(1, 64)])
    location = StringField('Location', validators=[Optional(), Length(1, 64)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')


# We define here the structure of a project, typically, the project name, a brief description and a date when it starts
# and we allow that it is updated if required
class ProjectForm(Form):
    title = StringField('Title', validators=[Required(), Length(1, 128)])
    description = TextAreaField('Desciption')
    date = DateField('Date', format='%d/%m/%Y', placeholder='dd/mm/yyyy')
    submit = SubmitField('Submit')

    def from_model(self, project):
        self.title.data = project.title
        self.description.data = project.description
        self.date.data = project.date

    def to_model(self, project):
        project.title = self.title.data
        project.description = self.description.data
        project.date = self.date.data