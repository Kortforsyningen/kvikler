import math
import re
from collections import namedtuple

KMSValue = namedtuple('KMSValue', ['value', 'unit'])
KMSCoord = namedtuple('KMSCoord', ['dimensions', 'northing', 'easting', 'elevation', 'minilabel', 'comment'])
KMSObs = namedtuple('KMSObs', ['occupation', 'target', 'obs', 'dist', 'mean_error', 'n_sets', 'journal_no', 'obs_year', 'obs_date', 'minilabel', 'error_md', 'error_type', 'error_mc'])

def kms_coord_dict(filename):
    '''
    Ingest KMS formated coordinate files and return a dictionary of coordinates
    with station-id as key. For each station a KMSCoord is added to the dict.
    '''
    stations = {}

    with open(filename, mode='r') as f:
        text = f.read()

    text2 = re.sub(r'\*.*?;', '', text, flags=re.DOTALL)
    text3 = re.sub(r'\s+\n', '\n', text2, flags=re.MULTILINE)
    lines = text3.split('\n')

    for line in lines:

        if line[0:17].strip().startswith('#'):
            kms_label = line.strip()
        elif line[0:17].strip().startswith('-1z'):
            kms_label = ''
        else:
            northing = None
            easting = None
            elevation = None

            station_id = line[0:17].replace(' ', '')
            station_descr = line[18:21].replace(' ', '')
            cols = re.split('  +', line[21:].strip())

            elements = []
            for i,element in enumerate(cols):
                value = None
                unit = None
                if element.strip().endswith((' m', ' dg', ' rad')):
                    value = ''.join(element.strip().split(' ')[:-1])
                    unit = element.strip().split(' ')[-1]

                if element.strip().endswith((' sx', ' nt')):
                    value = element.strip()
                    unit = element.strip().split(' ')[-1]

                if value is not None:
                    elements.append(KMSValue(value, unit))

            if len(elements) == 3:
                easting = elements[0]
                northing = elements[1]
                elevation = elements[2]

            if len(elements) == 2:
                easting = elements[0]
                northing = elements[1]

            if len(elements) == 1:
                elevation = elements[0]

            if len(elements)> 0:
                stations[station_id] = KMSCoord(
                    dimensions=len(elements),
                    northing=northing,
                    easting=easting,
                    elevation=elevation,
                    minilabel=kms_label,
                    comment=cols[len(elements):],
                )

    return stations



def kms_obs_list(filename):
    """Ingest KMS formated observations files and return a list of observations.

    Returns a list of KMSObs tuples.
    """
    observations = []

    with open(filename, mode="r") as f:
        text = f.read()

    text2 = re.sub(r'\*.*?;', '', text, flags=re.DOTALL)
    text3 = re.sub(r'\s+\n', '\n', text2, flags=re.MULTILINE)
    lines = text3.split('\n')

    for line in lines:
        obs_col = re.split('  +', line.strip())

        if line[0:12].strip().startswith('#'):
            kms_label_col = re.split(' +', line.strip())
            kms_label = kms_label_col[0]
            obs_error_type = kms_label_col[2]
            obs_error_md = float(kms_label_col[1])
            obs_error_mc = float(kms_label_col[3])

        elif line[0:12].strip().startswith('-1a'):
            kms_label = ''
            station_from = ''

        elif obs_col[0].strip() != '':
            if obs_col[0].strip().endswith('a'):
                station_from = (obs_col[0].replace('a', '').replace(' ', '').strip())
                obs_year = obs_col[1].strip()
                obs_sets = float( obs_col[2].replace(' ', '').strip() )
                obs_journal_no = obs_col[3].strip()
            else:
                station_to = obs_col[0].replace(' ', '').strip()
                obs_value = (float(obs_col[1].replace('m', '').replace(' ', '')))
                obs_dist = (float(obs_col[2].replace('m', '').replace(' ', '')) / 1000.0)
                obs_date = obs_col[3].strip()
                obs_setups = float(obs_col[4].replace(' ', '').strip())

                if obs_error_type == 'ne':
                    obs_std_dev = \
                        math.sqrt((obs_error_md**2 * obs_dist+ obs_error_mc**2) / obs_sets)

                elif obs_error_type == 'ppm':
                    obs_dist_single = (obs_dist - 2 * 0.025) / (obs_setups - 1)
                    obs_std_dev = math.sqrt((obs_error_md**2 \
                                    * (2 * 0.025**2 + (obs_setups - 1)
                                    * obs_dist_single**2)
                                    + obs_error_mc**2) / obs_sets)

                observations.append(KMSObs(
                    station_from,
                    station_to,
                    obs_value,
                    obs_dist,
                    obs_std_dev,
                    obs_sets,
                    obs_journal_no,
                    obs_year,
                    obs_date,
                    kms_label,
                    obs_error_md,
                    obs_error_type,
                    obs_error_mc,
                ))

    return observations
