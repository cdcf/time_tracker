__author__ = 'Cedric Da Costa Faro'

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length, Required
from wtforms.fields.html5 import DateField


# We define here the structure of a project, typically, the project name, a brief description and a date when it starts
# and we allow that it is updated if required
# We define here the structure of a client, typically, the client name and a location
def get_clients():
    from ..models import Client
    return Client.query.all()
    
class ProjectForm(Form):
    title = StringField('Title', validators=[Required(), Length(1, 128)])
    description = TextAreaField('Desciption')
    date = DateField('Date', format='%d/%m/%Y')
    client_id = QuerySelectField('Select Client', query_factory=get_clients, allow_blank=True, get_label='name')
    submit = SubmitField('Submit')

    def from_model(self, project):
        self.title.data = project.title
        self.description.data = project.description
        self.client_id.data = str(project.client_id)
        self.date.data = project.date

    def to_model(self, project):
        project.title = self.title.data
        project.description = self.description.data
        project.client_id = str(self.client_id.data)
        project.date = self.date.data
