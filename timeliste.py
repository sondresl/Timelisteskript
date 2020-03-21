import pandas as pd
from datetime import date
from sys import argv
from pprint import pprint
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from ast import literal_eval
from collections import defaultdict

# Denne må settes riktig!
TIMELISTE = '/Users/sondrelunde/dev/Timeliste/timeliste-mal.pdf'
MONTH = ''

def init_dict(firstname, lastname, course, date_of_birth, month):
    global MONTH
    MONTH = month
    return {
        # Header
        'firstname':           firstname,
        'lastname':            lastname,
        'course_code':         course,
        'month':               month,
        'date_of_birth':       date_of_birth,
        'total_hours':         0,
        # Spesifikasjon av antall timer
        'meetings':            0,
        'lab_prep':            0,
        'lab':                 0,
        'class_prep':          0,
        'class':               0,
        'communication':       0,
        'other':               0,
        'other_info':          defaultdict(int),
        'oblig':               []
    }

def read_data():
    return pd.read_csv(argv[-1])

def fill_dict(output, data):
    FIELDS = ['meetings', 'lab_prep', 'lab', 'class_prep', 'class', 'communication', 'other']
    sum_fields = 0  # Will be the final hours tally

    for field in FIELDS:
        output[field] = data[data['type'] == field]['timer'].sum()
        output[field] = int(output[field]) if output[field] % 1 == 0 else output[field]
        sum_fields += output[field]

    for index, notes in data[data['type'] == 'other'].iterrows():
        output['other_info'][notes['info']] += notes['timer']

    for index, row in data[data['type'] == 'oblig'].iterrows():

        ny_num = row['oblig#']
        ny_levering = row['levering']
        ny_antall = row['#obliger']
        ny_timer = row['timer']

        for i, (num, lev, ant, tim) in enumerate(output['oblig']):
            if (num, lev) == (ny_num, ny_levering):
                output['oblig'][i] = (num, lev, ant + ny_antall, tim + ny_timer)
                break
        else:
            output['oblig'].append((ny_num, ny_levering, ny_antall, ny_timer))

        sum_fields += row['timer']

    output['total_hours'] = sum_fields
    return output

def draw_to_canvas(canvas, data):
    """ The offsets used in drawString were found through
        trial and error, and are hardcoded to the particular template
        we are using. (i * 12) specifies a horizontal offset for
        each of the fields. """
    safe_draw(canvas, data,  42, 745, 'firstname')
    safe_draw(canvas, data, 217, 745, 'course_code')
    safe_draw(canvas, data, 394, 745, 'date_of_birth')
    safe_draw(canvas, data,  42, 700, 'lastname')
    safe_draw(canvas, data, 217, 700, 'month')
    safe_draw(canvas, data, 394, 700, 'total_hours')
    safe_draw(canvas, data, 308, 580, 'meetings')
    safe_draw(canvas, data, 308, 550, 'lab_prep')
    safe_draw(canvas, data, 308, 520, 'lab')
    safe_draw(canvas, data, 308, 490, 'class_prep')
    safe_draw(canvas, data, 308, 460, 'class')
    safe_draw(canvas, data, 308, 430, 'communication')
    safe_draw(canvas, data, 308, 400, 'other')

    # Annet info (defaultdict)
    for i, (info, timer) in enumerate(data['other_info'].items()):
        canvas.drawString(42, 398 - (i * 12), f'{info} ({timer})')

    for y, tup in enumerate(data['oblig']):
        for x, val in enumerate(tup):
            val = int(val) if val % 1 == 0 else val
            canvas.drawString(42 + (x * 130), 260 - (y * 30), str(val))

    canvas.drawString(42, 100,date.today().strftime("%d/%m/%Y"))


def safe_draw(can, info, x, y, key):
    if info[key]:
        can.drawString(x, y, str(info[key]))


def write_pdf(data):
    """Mostly grabbed verbatim from
       https://stackoverflow.com/questions/1180115/add-text-to-existing-pdf-using-python"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    assert MONTH != '', 'MONTH has not been set'
    outputname = f'timeliste_{MONTH}.pdf'

    draw_to_canvas(can, data)
    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open(TIMELISTE, "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open(outputname, "wb")
    output.write(outputStream)
    outputStream.close()


def main():
    if len(argv) != 7:
        print("Missing command line arguments!")
        print("Usage: python gen_dict.py <firstname> <lastname> <course> <date_of_birth> <month> <csv-file>")
        exit(1)

    data = init_dict(*argv[1:-1])
    df = read_data()
    fill_dict(data, df)
    write_pdf(data)


if __name__ == "__main__":
    main()
