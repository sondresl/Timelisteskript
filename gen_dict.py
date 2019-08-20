import pandas as pd
from sys import argv

output = {
    # Header
    'firstname':           'Sondre',
    'lastname':            'Lunde',
    'course_code':         'IN2040',
    'month':               'August',
    'date_of_birth':       'dd/mm/yy',
    'total_hours':         0,
    # Spesifikasjon av antall timer
    'meetings':            0,
    'lab_prep':            0,
    'lab':                 0,
    'klasseromstime_prep': 0,
    'klasseromstime':      0,
    'kommunikasjon':       0,
    'annet':               0,
    # Oblig rad 1
    'oblig_1_nr':          0,
    'oblig_1_levering':    0,
    'oblig_1_antall':      0,
    'oblig_1_timer':       0,
    # Oblig rad 2
    'oblig_2_nr':          0,
    'oblig_2_levering':    0,
    'oblig_2_antall':      0,
    'oblig_2_timer':       0,
    # Oblig rad 3
    'oblig_3_nr':          0,
    'oblig_3_levering':    0,
    'oblig_3_antall':      0,
    'oblig_3_timer':       0,
    # Oblig rad 4
    'oblig_4_nr':          0,
    'oblig_4_levering':    0,
    'oblig_4_antall':      0,
    'oblig_4_timer':       0
}

data = pd.read_csv(argv[1])

output['meetings'] = data[data['type'] == 'møte']['timer'].sum()
output['lab_prep'] = data[data['type'] == 'lab_prep']['timer'].sum()
output['lab'] = data[data['type'] == 'lab']['timer'].sum()
output['time_prep'] = data[data['type'] == 'time_prep']['timer'].sum()
output['time'] = data[data['type'] == 'time']['timer'].sum()
output['kommunikasjon'] = data[data['type'] == 'kommunikasjon']['timer'].sum()

output['total_hours'] = data[data['dato'] == 'Totalt']['timer'].sum()

output['annet'] = (output['total_hours'] - output['meetings'] - output['lab_prep'] - output['lab'] - output['time_prep'] - output['time'] - output['kommunikasjon'])



