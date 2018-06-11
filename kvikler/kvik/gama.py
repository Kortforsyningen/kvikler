import click

import kvikler

@click.group()
def gama():
    '''
    Tools for working with GNU Gama XML files.
    '''
    pass

@gama.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.argument('obs_file', nargs=-1, type=click.Path(exists=True))
@click.argument('gama_file', nargs=1, type=click.Path(exists=False))
def obs(verbose, obs_file, gama_file):
    '''
    Convert one or more observation files to GNU Gama XML format.
    '''
    if verbose:
        click.secho('Reading observation file(s)...', fg='red', bold=True)

@gama.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.argument('gama_file', nargs=1, type=click.Path(exists=True))
@click.argument('pub_file', nargs=1, type=click.Path(writable=True))
def pub(verbose, gama_file, pub_file):
    '''
    Convert a GNU Gama XML file to REFGEO pub file.
    '''
    if verbose:
        click.secho('Reading Gama file...', fg='red', bold=True)
