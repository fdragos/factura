

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

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
    factura = [
        f"Seria: {date['serie_factura']}",
        f"Numar: {date['nr_factura']}",
        f"Data: {date['data_factura']}"
    ]
    for line in factura:
        y -= 15
        pdf.drawCentredString(width / 2, y, line)
    
    y -= 40

    # FURNIZOR
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x_left, y, "Furnizor:")
    pdf.setFont("Helvetica", 10)
    furnizor = [
        f"Denumire firma: {date['firma']}",
        f"C.I.F.: {date['cif']}",
        f"Nr. ord. reg. com.: {date['reg_com']}",
        f"Sediul: {date['sediu']}",
        f"Cont RON: {date['iban']}",
        f"Banca: {date['banca']}"
    ]
    for line in furnizor:
        y -= 15
        pdf.drawString(x_left, y, line)

    pdf.line(x_left, y - 10, x_left + 500, y - 10)

    # CLIENT
    y -= 30
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x_left, y, "Client (Beneficiar):")
    pdf.setFont("Helvetica", 10)
    client = [
        f"Denumire: {date['client']}",
        f"Adresa: {date['adresa_client']}",
        f"Cod TVA: {date['tva_client']}"
    ]
    for line in client:
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

# INTERFAȚĂ STREAMLIT
st.title("🧾 Generator Facturi Airbnb / Booking")

with st.form("form_factura"):
    st.subheader("Date factura")
    serie_factura = st.text_input("Serie factura", "BVN")
    nr_factura = st.text_input("Nr factura", "000000")
    data_factura = st.date_input("Data facturare").strftime("%d.%m.%Y")

    st.subheader("Date firma")
    firma = st.text_input("Denumire firma", "Nicmond Impex SRL")
    cif = st.text_input("C.I.F.", "RO10823292")
    reg_com = st.text_input("Nr. ord. reg. com.", "J08/894/1998")
    sediu = st.text_input("Sediu complet", "SAT CRISTIAN COM. CRISTIAN, STR. MIHAI EMINESCU, NR. 44D, Jud. Brasov")
    iban = st.text_input("Cont IBAN", "RO63RNCB0857008643990001")
    banca = st.text_input("Banca", "BANCA COMERCIALA ROMANA")

    st.subheader("Date rezervare")
    platforma = st.selectbox("Platformă", ["airbnb", "booking"])
    cod_rezervare = st.text_input("Cod rezervare", "HMZS29R93J")
    checkin = st.date_input("Check-in").strftime("%d.%m.%Y")
    checkout = st.date_input("Check-out").strftime("%d.%m.%Y")
    nopti = st.number_input("Număr nopți", 1)

    suma_bruta = st.number_input("Sumă brută client (Booking)", value=300.00)
    suma_neta = st.number_input("Sumă netă încasată (Airbnb)", value=276.64)

    st.subheader("Date client (pers. fizică pentru Booking / Airbnb Irlanda)")
    client = st.text_input("Denumire client", "Airbnb Ireland UC")
    adresa_client = st.text_input("Adresă client", "8 Hanover Quay, Dublin 2, Irlanda")
    tva_client = st.text_input("Cod TVA client", "IE9827384L")

    tva = st.number_input("TVA aplicabil (%)", value=9)

    submitted = st.form_submit_button("Generează factură")
   
    # Variabilă pentru confirmare
    factura_generata = False
    path = "factura_dinamica.pdf"
   
    if submitted:
        date = {
            "serie_factura": serie_factura, "nr_factura": nr_factura, "data_factura": data_factura,
            "firma": firma, "cif": cif, "reg_com": reg_com, "sediu": sediu,
            "iban": iban, "banca": banca, "platforma": platforma,
            "client": client, "adresa_client": adresa_client, "tva_client": tva_client,
            "cod_rezervare": cod_rezervare, "checkin": checkin, "checkout": checkout,
            "nopti": nopti, "suma_bruta": suma_bruta, "suma_neta": suma_neta, "tva": tva
        }
        genereaza_factura_pdf(date, path)
        factura_generata = True

    # Afișare buton de descărcare după submit
if factura_generata:
    st.success("✅ Factura a fost generată cu succes!")
    with open(path, "rb") as f:
        name = (client + serie_factura + nr_factura + ".pdf").replace(" ", "_")
        st.download_button("📥 Descarcă PDF", f, file_name=name, mime="application/pdf")
