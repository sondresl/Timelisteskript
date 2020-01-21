import pandas as pd
from datetime import date
from sys import argv
from pprint import pprint
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from sys import argv
from ast import literal_eval

def init_dict(firstname, lastname, course, date_of_birth, month):
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
        'klasseromstime_prep': 0,
        'klasseromstime':      0,
        'kommunikasjon':       0,
        'annet':               0,
        'annet_info':         [],
        'retting':            []
    }

def read_data():
    return pd.read_csv(argv[-1])

def fill_dict(output, data):
    FIELDS = ['meetings', 'lab_prep', 'lab', 'class_prep', 'class', 'kommunikasjon', 'annet']
    sum_fields = 0

    for field in FIELDS:
        output[field] = data[data['type'] == field]['timer'].sum()
        output[field] = int(output[field]) if output[field] % 1 == 0 else output[field]
        sum_fields += output[field]

    for index, notes in data[data['type'] == 'annet'].iterrows():
        output['annet_info'].append((notes['info'], notes['timer']))

    for index, row in data[data['type'] == 'retting'].iterrows():
        output[field] = int(output[field]) if output[field] % 1 == 0 else output[field]
        output['retting'].append((row['oblig#'], row['levering'], row['#obliger'], row['timer']))
        sum_fields += row['timer']

    output['total_hours'] = sum_fields
    return output

def read_python_dict(filename):
    with open(filename) as f:
        return literal_eval(f.read())

def draw_to_canvas(can, data):
    safe_draw(can, data,  42, 745, 'firstname')
    safe_draw(can, data, 217, 745, 'course_code')
    safe_draw(can, data, 394, 745, 'date_of_birth')
    safe_draw(can, data,  42, 700, 'lastname')
    safe_draw(can, data, 217, 700, 'month')
    safe_draw(can, data, 394, 700, 'total_hours')
    safe_draw(can, data, 308, 580, 'meetings')
    safe_draw(can, data, 308, 550, 'lab_prep')
    safe_draw(can, data, 308, 520, 'lab')
    safe_draw(can, data, 308, 490, 'class_prep')
    safe_draw(can, data, 308, 460, 'class')
    safe_draw(can, data, 308, 430, 'kommunikasjon')
    safe_draw(can, data, 308, 400, 'annet')

    for i, (info, timer) in enumerate(data['annet_info']):
        can.drawString(42, 398 - (i * 12), f'{info} ({timer})')

    for y, tup in enumerate(data['retting']):
        for x, val in enumerate(tup):
            val = int(val) if val % 1 == 0 else val
            can.drawString(42 + (x * 130), 260 - (y * 30), str(val))

    can.drawString(42, 100,date.today().strftime("%d/%m/%Y"))


def safe_draw(can, info, x, y, key):
    if info[key]:
        can.drawString(x, y, str(info[key]))

def write_pdf(data, outputname='destination.pdf', timeliste='timeliste-2017.pdf'):
    """Mostly grabbed verbatim from
       https://stackoverflow.com/questions/1180115/add-text-to-existing-pdf-using-python"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    draw_to_canvas(can, data)
    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(open(timeliste, "rb"))
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

    print(date.today().strftime("%d/%m/%Y"))
    data = init_dict(*argv[1:-1])
    df = read_data()
    fill_dict(data, df)
    write_pdf(data)

if __name__ == "__main__":
    main()
