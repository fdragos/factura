

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import info

def genereaza_factura_pdf(date, cale_salveaza):
    pdf = canvas.Canvas(cale_salveaza, pagesize=A4)
    width, height = A4
    x_left = 40
    y = height - 50

    # HEADER
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(width / 2, y, "FACTURA FISCALA")
    y -= 20
    pdf.setFont("Helvetica", 10)

    for line in date["factura"]:
        y -= 15
        pdf.drawCentredString(width / 2, y, line)
    
    y -= 40

    # FURNIZOR
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x_left, y, "Furnizor:")
    pdf.setFont("Helvetica", 10)

    for line in date["furnizor"]:
        y -= 15
        pdf.drawString(x_left, y, line)

    pdf.line(x_left, y - 10, x_left + 500, y - 10)

    # CLIENT
    y -= 30
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x_left, y, "Client (Beneficiar):")
    pdf.setFont("Helvetica", 10)

    for line in date["client"]:
        y -= 15
        pdf.drawString(x_left, y, line)
    
    pdf.line(x_left, y - 10, x_left + 500, y - 10)

    # DETALII SERVICII
    y -= 30
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x_left, y, "Detalii servicii")
    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(x_left, y, "Nr.")
    pdf.drawString(x_left + 30, y, "Descriere serviciu")
    pdf.drawString(x_left + 250, y, "UM")
    pdf.drawString(x_left + 290, y, "Cant.")
    pdf.drawString(x_left + 340, y, "Pret unitar")
    pdf.drawString(x_left + 420, y, "Valoare")
    y -= 15
    pdf.setFont("Helvetica", 10)

    pret_unitar = date['suma_neta'] if date['platforma'] == "airbnb" else round(date['suma_bruta'] / (1 + date['tva'] / 100), 2)
    valoare = date['suma_neta'] if date['platforma'] == "airbnb" else date['suma_bruta']

    pdf.drawString(x_left, y, "1")
    pdf.drawString(x_left + 30, y, f"Cazare – {date['cod_rezervare']}")
    pdf.drawString(x_left + 250, y, "noapte")
    pdf.drawString(x_left + 290, y, str(date['nopti']))
    pdf.drawString(x_left + 340, y, f"{pret_unitar:.2f}")
    pdf.drawString(x_left + 420, y, f"{valoare:.2f}")
    
    # TOTAL
    y -= 30
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(x_left, y, f"Total de plata: {valoare:.2f} lei")
    y -= 15
    if date['platforma'] == "airbnb":
        pdf.drawString(x_left, y, "TVA: 0 lei (taxare inversa)")
    else:
        tva_val = round(valoare * date['tva'] / (100 + date['tva']), 2)
        pdf.drawString(x_left, y, f"TVA (inclus): {tva_val:.2f} lei ({date['tva']}%)")

    pdf.line(x_left, y - 10, x_left + 500, y - 10 )

    # MENȚIUNI
    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(x_left, y, "Mentiuni:")
    y -= 15
    if date['platforma'] == "airbnb":
        pdf.drawString(x_left, y, "- Taxare inversa conform art. 278 alin. (2) din Codul Fiscal.")
        y -= 15
        pdf.drawString(x_left, y, "- Beneficiarul este obligat la plata TVA.")
    y -= 15
    pdf.drawString(x_left, y, f"- Sejur: {date['checkin']} – {date['checkout']}")
    y -= 15
    pdf.drawString(x_left, y, f"- Cod rezervare: {date['cod_rezervare']}")
    y -= 30
    pdf.drawString(x_left, y, "Reprezentant legal: .............................................")

    pdf.save()

