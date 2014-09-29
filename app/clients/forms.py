__author__ = 'Cedric Da Costa Faro'

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, Required


# We define here the structure of a client, typically, the client name and a location
class ClientForm(Form):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    location = TextAreaField('Location', validators=[Required()])
    submit = SubmitField('Submit')

    def from_model(self, client):
        self.name.data = client.name
        self.location.data = client.location

    def to_model(self, client):
        client.name = self.name.data
        client.location = self.location.data
