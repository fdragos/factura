import streamlit as st
import os
from datetime import datetime
import info
from db import init_db, get_urmatorul_numar_factura, salveaza_factura, incarca_facturi, sterge_factura, get_nr_factura_curent, increment_nr_factura, exista_factura
from factura import genereaza_factura_pdf

os.makedirs("facturi", exist_ok=True)
init_db()

st.set_page_config("Facturi Airbnb / Booking", layout="centered", )
tab1, tab2 = st.tabs(["🧾 Creează factură", "📁 Facturi salvate"])

with tab1:

    st.title("🧾 Creează factură")
    if "platforma" not in st.session_state:
        st.session_state["platforma"] = "airbnb"

    platforma = st.selectbox("Platformă", ["airbnb", "booking"], index=0 if st.session_state["platforma"] == "airbnb" else 1)
    st.session_state["platforma"] = platforma

    with st.form("form"):
        st.subheader("Date factura")
        serie_factura = st.text_input("Serie factura", "BVN")
        nr_factura = st.text_input("Nr factura", "000000")
        data_factura = st.date_input("Data facturare").strftime("%d.%m.%Y")

        st.subheader("Date firmă")
        firma = st.text_input("Denumire firma", info.firma)
        cif = st.text_input("C.I.F.", info.cif)
        reg_com = st.text_input("Nr. ord. reg. com.", info.reg_com)
        sediu = st.text_input("Sediu complet", info.sediu)
        iban = st.text_input("Cont IBAN", info.iban)
        banca = st.text_input("Banca", info.banca)

        st.subheader("Rezervare")
        cod_rezervare = st.text_input("Cod rezervare", "")
        checkin = st.date_input("Check-in").strftime("%d.%m.%Y")
        checkout = st.date_input("Check-out").strftime("%d.%m.%Y")
        nopti = st.number_input("Nopți", 0)
        suma_bruta = st.number_input("Sumă brută client (Booking)", value=0)
        suma_neta = st.number_input("Sumă netă încasată (Airbnb)", value=0)
        tva = st.number_input("TVA (%)", 9)

        st.subheader("Client")
        if st.session_state["platforma"] == "airbnb":
            client = st.text_input("Nume", "Airbnb Ireland UC", disabled=True)
            adresa = st.text_input("Adresă", "8 Hanover Quay, Dublin 2, Irlanda", disabled=True)
            tva_client = st.text_input("TVA client", "IE9827384L", disabled=True)
        else:
            client = st.text_input("Nume", "")
            adresa = st.text_input("Adresă", "")
            tva_client = st.text_input("TVA client", "")

        trimite = st.form_submit_button("✅ Generează")

    if not nr_factura.isdigit():
        st.warning("Numărul facturii trebuie să conțină doar cifre.")
    elif trimite:
        numar_int = int(nr_factura)
        nr_factura_complet = f"{serie_factura}{numar_int}"
        data = datetime.today().strftime("%d.%m.%Y")

        while True:
            nr_formatat = str(numar_int).zfill(6)
            nr_factura_complet = f"{serie_factura}{nr_formatat}"
            if not exista_factura(nr_factura_complet):
                break
            else:
                numar_int += 1
                st.warning(f"numar factura existent")

        fisier = f"facturi/Factura_{client}_{nr_factura_complet}.pdf".replace(" ", "_")



        date = {
            "factura": [f"Seria: {serie_factura}", f"Numar: {nr_factura}", f"Data facturare: {data_factura}"],
            "nr_factura": nr_factura_complet,
            "data": data,
            "furnizor": [f"Denumire firma: {firma}", f"CIF: {cif}", f"Reg. Com.: {reg_com}", f"Sediu: {sediu}", f"IBAN: {iban}", f"Banca: {banca}"],
            "client": [client, adresa, f"Cod TVA: {tva_client}"],
            "platforma": platforma,
            "cod_rezervare": cod_rezervare,
            "checkin": checkin,
            "checkout": checkout,
            "nopti": nopti,
            "suma_bruta": suma_bruta,
            "suma_neta": suma_neta,
            "tva": tva
        }

        genereaza_factura_pdf(date, fisier)
        salveaza_factura(nr_factura_complet, data, client, platforma, cod_rezervare, fisier)
        
        st.success(f"Factura {nr_factura_complet} generată.")
        with open(fisier, "rb") as f:
            st.download_button("📥 Descarcă factura", f, file_name=os.path.basename(fisier), mime="application/pdf")

with tab2:
    st.title("📁 Facturi existente")
    facturi = incarca_facturi()

    if not facturi:
        st.info("Nu există facturi salvate.")
    else:
        for nr, data, client, platforma, cod, fisier in facturi:
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"**Factura {nr}** | {data} | {platforma.upper()} | {client} | {cod}")
            with col2:
                with open(fisier, "rb") as f:
                    st.download_button("⬇️", f, file_name=os.path.basename(fisier), key=f"dl{nr}")
            with col3:
                if st.button("🗑️ Șterge", key=f"del{nr}"):
                    sterge_factura(nr)
                    os.remove(fisier)
                    st.rerun()