__author__ = 'Cedric Da Costa Faro'

from flask.ext.wtf import Form
from wtforms import SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from ..models import Client, Project
from wtforms.fields.html5 import DateField
import datetime


# We define here the structure of a client, typically, the client name and a location
def get_clients():
    return Client.query.all()


def get_projects():
    return Project.query.all()


class AgendaForm(Form):
    agenda_date = DateField('Date', format='%d/%m/%Y', default=datetime.date.today())
    project_id = QuerySelectField('Select_Project',
        validators=[Required()],
        query_factory=get_projects,
        allow_blank=True,
        get_label='title',
        blank_text=u'-- Please choose a project --')
    submit = SubmitField('Submit')

    def from_model(self, agenda):
        self.agenda_date.data = agenda.agenda_date
        self.project_id.data = agenda.project_agenda

    def to_model(self, agenda):
        agenda.agenda_date = self.agenda_date.data
        agenda.project_agenda = self.project_id.data
