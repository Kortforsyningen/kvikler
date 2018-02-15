from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import click
import sqlalchemy

import kvikler
from kvikler.schema import create_schema
from kvikler.schema import drop_schema


@click.group()
def admin():
    '''
    Administrative tools for the kvikler database system.
    '''
    pass

@admin.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def initdb(verbose):
    '''
    Populate schema in database.
    '''
    if verbose:
        click.secho('Creating database', fg='red', bold=True)

    engine = sqlalchemy.create_engine(kvikler.con_str, echo=verbose)
    engine.connect()
    create_schema(engine)
    engine.dispose()

@admin.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def dropdb(verbose):
    '''
    Drop schema from database.
    '''
    if verbose:
        click.secho('Creating database', fg='red', bold=True)


    engine = sqlalchemy.create_engine(kvikler.con_str, echo=verbose)
    engine.connect()
    drop_schema(engine)
    engine.dispose()

