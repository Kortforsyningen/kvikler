from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import datetime
import click


import kvikler
from kvikler.io import kms_coord_dict
from kvikler.io import kms_obs_list

@click.group()
def kmsfile():
    '''Parse various kms-files.'''
    pass

@kmsfile.command()
@click.argument('kmsfile', type=click.Path(exists=True))
def obs(kmsfile):
    '''Parse KMS observation file.'''
    #KMSObs = namedtuple('KMSObs', ['occupation', 'target', 'obs', 'dist', 'mean_error', 'n_sets', 'journal_no', 'obs_year', 'obs_date', 'minilabel', 'error_md', 'error_type', 'error_mc'])

    observations = kms_obs_list(kmsfile)
    header = True
    for obs in observations:
        if header:
            header = False
            click.secho('{:<13}'.format('occupation'), nl=False, fg='green')
            click.secho('{:<15}'.format('target'), nl=False, fg='green')
            click.secho('{:<9}'.format('obs'), nl=False, fg='green')
            click.secho('{:<9}'.format('dist'), nl=False, fg='green')
            click.secho('{:<9}'.format('mean_err'), nl=False, fg='green')
            click.secho('{:<8}'.format('n_sets'), nl=False, fg='green')
            click.secho('{:<12}'.format('journal_no'), nl=False, fg='green')
            #click.secho('{:<10}'.format('obs_year'), nl=False, fg='green')
            click.secho('{:<18}'.format('obs_date'), nl=False, fg='green')
            click.secho('{:<12}'.format('minilabel'), nl=False, fg='green')
            click.secho('{:<10}'.format('error_md'), nl=False, fg='green')
            click.secho('{:<6}'.format('unit'), nl=False, fg='green')
            click.secho('{:<10}'.format('error_mc'), fg='green')

        #click.echo(tuple(obs))
        click.secho('{:<13}'.format(obs.occupation), nl=False)
        click.secho('{:<13}'.format(obs.target), nl=False)
        click.secho('{: 8.3f}'.format(float(obs.obs),''), nl=False)
        click.secho('{: 8.3f} '.format(float(obs.dist)), nl=False)
        click.secho('{: 8.3f} '.format(float(obs.mean_error)), nl=False)
        click.secho('{:3d}{:<3} '.format(int(obs.n_sets), ''), nl=False)
        click.secho('{:10d}{:<4} '.format(int(obs.journal_no), ''), nl=False)
        dt = datetime.datetime.strptime(obs.obs_date, '%Y%m%d,%H.%M')
        click.secho('{:<18}'.format(dt.strftime('%Y-%m-%d %H:%M')), nl=False)
        click.secho('{:<10} '.format(obs.minilabel), nl=False)
        click.secho('{: 3.4f}{:<4}'.format(obs.error_md, ''), nl=False)
        click.secho('{:<5}'.format(obs.error_type), nl=False)
        click.secho('{: 3.4f} '.format(obs.error_mc))


def format_kmscoord(coord):
    '''Format a KMSCoord for use with click.echo'''

    if coord.unit in ('m', 'dg', 'rad'):
        s = '{:8.4f}'.format(float(coord.value))
    else:
        s = '{:<13}'.format(coord.value)

    s+= ' {:<4}'.format(coord.unit)

    return click.style(s)


@kmsfile.command()
@click.argument('kmsfile', type=click.Path(exists=True))
@click.option('-m', '--minilabel', is_flag=True, help='Display minilabels for each coordinate')
def coord(kmsfile, minilabel):
    '''Parse KMS Coordinate file.'''

    coordinates = kms_coord_dict(kmsfile)
    header = True

    for ident, coord in coordinates.iteritems():
        if header:
            header = False
            click.secho('{:<15}'.format('# Ident'), nl=False, fg='green')
            # we assume that all coordinates are the same dimension as the first
            if coord.easting is not None:
                click.secho('{:<17}'.format('Easting'), nl=False, fg='green')
            if coord.northing is not None:
                click.secho('{:<16}'.format('Northing'), nl=False, fg='green')
            if coord.elevation is not None:
                click.secho('{:<16}'.format('Elevation'), nl=False, fg='green')
            if minilabel:
                click.secho('{:<20}'.format('Mini label'), nl=False, fg='green')
            click.secho('Comment', fg='green')

        click.echo('{:<15}'.format(ident), nl=False)
        if coord.easting is not None:
            click.echo(format_kmscoord(coord.easting), nl=False)

        if coord.northing is not None:
            click.echo(format_kmscoord(coord.northing), nl=False)

        if coord.elevation is not None:
            click.echo(format_kmscoord(coord.elevation), nl=False)

        if minilabel:
            click.secho('{:<20}'.format(coord.minilabel), nl=False)

        commentstring = ''
        for s in coord.comment:
            commentstring += s + ' '
        commentstring = commentstring.rstrip()

        try:
            dt = datetime.datetime.strptime(commentstring, '%Y %m %d, %H.%M')
        except ValueError:
            dt = click.style(commentstring, fg='red')

        click.echo('{}'.format(dt))
