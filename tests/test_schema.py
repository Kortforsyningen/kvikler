""""
Test suite for the schema module in the kvikler package.
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import sqlalchemy

import kvikler
# Yes, this is bad pep8-form, but sometimes breaking the rules is necessary. Rebel rebel.
kvikler.IS_TESTING = True

from kvikler.schema import create_schema
from kvikler.schema import drop_schema


def test_table_relationships():
    '''
    Table relationship consistency.

    We need to make sure that we set up the schema correctly. One way to do so
    is to create a new schema, create all tables and drop them again. sqlalchemy
    will tell us if the primary-foreign key relationships are not correctly set
    up when we try to drop the tables.
    '''

    engine = sqlalchemy.create_engine('sqlite://', echo=True)
    engine.connect()

    create_schema(engine)
    drop_schema(engine)

    engine.dispose()
