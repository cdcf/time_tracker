__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from .. import db
from ..models import Agenda
from . import agendas
from .forms import AgendaForm


# We allow here a user to create a new agenda once he has logged in and to modify his own ones only
@agendas.route('/new_agenda/', methods=['GET', 'POST'])
@login_required
def new_agenda():
    form = AgendaForm()
    if form.validate_on_submit():
        agenda = Agenda(author=current_user)
        form.to_model(agenda)
        db.session.add(agenda)
        db.session.commit()
        flash('The agenda was added successfully.', 'success')
        return redirect(url_for('agendas.agenda_list'))
    return render_template('agendas/edit_agenda.html/', form=form)


# We list here all agendas
@agendas.route('/agenda_list/', methods=['GET', 'POST'])
@login_required
def agenda_list():
    page = request.args.get('page', 1, type=int)
    pagination = Agenda.query.order_by(Agenda.agenda_date.asc()).paginate(page,
                                                                      per_page=current_app.config['AGENDA_PER_PAGE'],
                                                                      error_out=False)
    list_of_agenda = pagination.items
    return render_template('agendas/list_agenda.html/', agendas=list_of_agenda, pagination=pagination)


# this function is used as basis to generate a agenda
@agendas.route('/agenda/<int:id>/')
def agenda(id):
    agenda = Agenda.query.get_or_404(id)
    headers = {}
    if current_user.is_authenticated():
        headers['X-XSS-Protection'] = '0'
    return render_template('agendas/agenda.html/', agenda=agenda), 200, headers


# We enable agenda owner to edit them if required
@agendas.route('/edit_agenda/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_agenda(id):
    agenda = Agenda.query.get_or_404(id)
    if not current_user.is_admin and agenda.author != current_user:
        abort(403)
    form = AgendaForm()
    if form.validate_on_submit():
        form.to_model(agenda)
        db.session.add(agenda)
        db.session.commit()
        flash('The agenda was updated successfully.', 'success')
        return redirect(url_for('agendas.agenda_list'))
    form.from_model(agenda)
    return render_template('agendas/edit_agenda.html', form=form)


@agendas.route('/delete_agenda/<int:id>/', methods=['POST'])
@login_required
def delete_agenda(id):
    agenda = Agenda.query.get_or_404(id)
    db.session.delete(agenda)
    db.session.commit()
    flash('Agenda was deleted successfully.', 'success')
    return redirect(url_for('agendas.agenda_list'))
