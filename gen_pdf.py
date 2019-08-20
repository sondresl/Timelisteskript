from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from sys import argv
from ast import literal_eval


def read_data(filename):
    with open(filename) as f:
        return {k: v for k, v in (line.split() for line in f if line[0] != '#')}


def read_python_dict(filename):
    with open(filename) as f:
        return literal_eval(f.read())


def draw_to_canvas(can, info):
    safe_draw(can, info,  42, 745, 'firstname')
    safe_draw(can, info, 217, 745, 'course_code')
    safe_draw(can, info, 394, 745, 'date_of_birth')
    safe_draw(can, info,  42, 700, 'lastname')
    safe_draw(can, info, 217, 700, 'month')
    safe_draw(can, info, 394, 700, 'total_hours')
    safe_draw(can, info, 308, 580, 'meetings')
    safe_draw(can, info, 308, 550, 'lab_prep')
    safe_draw(can, info, 308, 520, 'lab')
    safe_draw(can, info, 308, 490, 'klasseromstime_prep')
    safe_draw(can, info, 308, 460, 'klasseromstime')
    safe_draw(can, info, 308, 430, 'kommunikasjon')
    safe_draw(can, info, 308, 400, 'annet')

    safe_draw(can, info, 42,  260, "oblig_1_nr")
    safe_draw(can, info, 175, 260, "oblig_1_levering")
    safe_draw(can, info, 305, 260, "oblig_1_antall")
    safe_draw(can, info, 435, 260, "oblig_1_timer")

    safe_draw(can, info, 42,  230, "oblig_2_nr")
    safe_draw(can, info, 175, 230, "oblig_2_levering")
    safe_draw(can, info, 305, 230, "oblig_2_antall")
    safe_draw(can, info, 435, 230, "oblig_2_timer")

    safe_draw(can, info, 42,  200, "oblig_3_nr")
    safe_draw(can, info, 175, 200, "oblig_3_levering")
    safe_draw(can, info, 305, 200, "oblig_3_antall")
    safe_draw(can, info, 435, 200, "oblig_3_timer")

    safe_draw(can, info, 42,  170, "oblig_4_nr")
    safe_draw(can, info, 175, 170, "oblig_4_levering")
    safe_draw(can, info, 305, 170, "oblig_4_antall")
    safe_draw(can, info, 435, 170, "oblig_4_timer")


def safe_draw(can, info, x, y, key):
    if info[key]:
        can.drawString(x, y, str(info[key]))


def write_pdf(data, outputname='destination.pdf'):
    """Mostly grabbed from https://stackoverflow.com/questions/1180115/add-text-to-existing-pdf-using-python"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    draw_to_canvas(can, data)

    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("timeliste-2017.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

def main():
    if len(argv) < 2:
        print("Missing data file")
        exit(1)

    fn = argv[1]

    data = read_python_dict(fn)

    write_pdf(data)

if __name__ == "__main__":
    main()
