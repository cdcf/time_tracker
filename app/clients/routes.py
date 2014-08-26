__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from .. import db
from ..models import Client
from . import clients
from .forms import ClientForm


# We allow here a user to create a new client account once he has logged in and to modify his own ones only
@clients.route('/new_client/', methods=['GET', 'POST'])
@login_required
def client_new():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(author=current_user)
        form.to_model(client)
        db.session.add(client)
        db.session.commit()
        flash('The client was added successfully.', 'success')
        return redirect(url_for('clients.list_client'))
    return render_template('clients/edit_client.html/', form=form)


# We list here all clients
@clients.route('/list_client/', methods=['GET', 'POST'])
@login_required
def list_client():
    page = request.args.get('page', 1, type=int)
    pagination = Client.query.order_by(Client.name.asc()).paginate(page,
                                                                      per_page=current_app.config['CLIENT_PER_PAGE'],
                                                                      error_out=False)
    list_client = pagination.items
    return render_template('clients/list_client.html/', clients=list_client, pagination=pagination)




# this function is used as basis to generate a client
@clients.route('/client/<int:id>/')
def client(id):
    client = Client.query.get_or_404(id)
    headers = {}
    if current_user.is_authenticated():
        headers['X-XSS-Protection'] = '0'
    return render_template('clients/client.html/', client=client), 200, headers


# We enable client owner to edit them if required
@clients.route('/edit_client/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = Client.query.get_or_404(id)
    if not current_user.is_admin and client.author != current_user:
        abort(403)
    form = ClientForm()
    if form.validate_on_submit():
        form.to_model(client)
        db.session.add(client)
        db.session.commit()
        flash('The client was updated successfully.', 'success')
        return redirect(url_for('clients.list_client'))
    form.from_model(client)
    return render_template('clients/edit_client.html', form=form)


@clients.route('/delete_client/<int:id>/', methods=['POST'])
@login_required
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('Client was deleted successfully.', 'success')
    return redirect(url_for('clients.list_client'))
