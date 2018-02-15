'''
Main entry point for the "kvik" command line interface to kvikler.
'''
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins

import kvikler
from kvikler.kvik.admin import admin

@with_plugins(iter_entry_points('kvikler.kvik_commands'))
@click.group()
def kvik():
    '''
    Command line frontend to the kvikler database system.
    '''
    pass

