import random
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io


def divide_evenly(wordlist, nwords, npages):
    pages = []
    floor_division = nwords // npages
    for i in range(npages):
        pages.append(random.sample(wordlist, floor_division))
    remainder = nwords - floor_division * npages
    for j in range(remainder):
        pages[j].append(random.choice(wordlist))
    random.shuffle(pages)
    return pages


words = open('words_alpha.txt').read().split('\n')

existing_pdf = PdfFileReader(open("Scanned Document.pdf", "rb"))
number_of_pages = len(existing_pdf.pages)

words_for_pdf = divide_evenly(words, 20, number_of_pages)

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=A4)

for i in range(number_of_pages):
    line = " ".join(words_for_pdf[i])
    can.drawString(10, 100, line)
    print(line)
    can.showPage()

can.save()

packet.seek(0)
new_pdf = PdfFileReader(packet)
output = PdfFileWriter()

for i in range(number_of_pages):
    page = new_pdf.getPage(i)
    page.mergePage(existing_pdf.getPage(i))
    output.addPage(page)

outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()