from domain.role import Role
from domain.user import User

from flask import current_app, g
from mongodb.connection import get_db, close_db
from werkzeug.security import generate_password_hash

import click

def init_db():
    '''
    Initialize the database
    '''
    db = get_db()

    # it can be commented out to avoid data loss
    db.drop_collection('user')
    db.drop_collection('role')

    adm_user = User.find_all_by('username', 'sazevedo')

    if not adm_user:

        adm_user = User(
            username='sazevedo',
            password=generate_password_hash('initiare'),
            role='admin',              
            name='Sylvio Ximenez de Azevedo Neto'
        )
        
        adm_user.save()

    admin_role = Role.find_all_by('role', 'admin')

    if not admin_role:
        admin_role = Role()
        admin_role.role = 'admin'
        admin_role.save()

    user_role = Role.find_all_by('role', 'user')

    if not user_role:
        user_role = Role()
        user_role.role = 'user'
        user_role.save()

@click.command('init-db')
def init_db_command():
    '''
    Clear the existing data and create new tables
    '''
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    '''
    register database initialization command with the application
    '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
