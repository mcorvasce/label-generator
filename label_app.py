import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, inch
import datetime
import pandas as pd
import os
import pytz  # For timezone support
import base64

# Files
CSV_FILE = "label_log.csv"
PDF_FILE = "label.pdf"

# App config
st.set_page_config(page_title="Label Generator", layout="centered")
st.title("📦 Bottle Bin Label Generator / Generador de Etiquetas para Bines")

# Hide number input steppers
st.markdown("""
    <style>
    [data-testid="stNumberInput"] button {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Shortened formula names
formula_names = [
    "AP Citrus Carrot", "Apple Celery", "Better Mood Shot - FM",
    "Blue Sipper", "Breastfeeding - FM", "Calm - Bridal", "Celery Juice",
    "Chocolate Cashew", "Chocolate Protein", "Citrus Carrot", "Citrus Mint",
    "Clementine Creamsicle", "Cookies & Cream", "Cool Greens", "Craving Crusher Shot",
    "Deblot - Bridal", "Detox - Bridal", "Energy - Bridal", "Ginger Turmeric", "Green Sipper",
    "Hair - Bridal", "Lemony Greens", "Orange Sipper", "Peanut Butter", "Peanut Butter Cup",
    "Pina Colada", "Pink Sipper", "Protein Greens", "Protein Shot", "Purple Sipper",
    "Red Sipper", "Replenish Shot", "Salt Water", "Skin Glow - Bridal",
    "Skinny Boost Shot", "Sleep - Bridal", "Sleep Shot", "Strawberry Greens", "Strong & Lean",
    "Sweet Greens", "Sweet Roots", "Tarte Greens", "Tropical Greens", "Tropical Sunrise",
    "Vanilla Cashew", "Yellow Sipper"
]

# Session state defaults
if "label_ready" not in st.session_state:
    st.session_state.label_ready = False
if "clear_form" not in st.session_state:
    st.session_state.clear_form = False

# Handle clearing
if st.session_state.clear_form:
    st.session_state.formula_name = None
    st.session_state.bottle_count = 0
    st.session_state.weight_per_bottle = 0.0
    st.session_state.bin_weight = 0.0
    st.session_state.label_ready = False
    st.session_state.clear_form = False

# Inputs
formula_name = st.selectbox(
    "Formula Name (Nombre de la Fórmula)",
    options=["Choose Flavor (Elija el Sabor)"] + formula_names,
    index=0,
    key="formula_name"
)

if formula_name == "Choose Flavor (Elija el Sabor)":
    st.warning("⚠️ Please select a valid formula name.")
    valid_selection = False
else:
    valid_selection = True

bottle_count = st.number_input("Bottle Count (Cantidad de Botellas)", min_value=0, step=1, key="bottle_count")
weight_per_bottle = st.number_input("Weight per Bottle (Peso por Botella, lbs)", min_value=0.0, step=0.01, format="%.2f", key="weight_per_bottle")
bin_weight = st.number_input("Bin Gross Weight (Peso Bruto del Bin, lbs)", min_value=0.0, step=0.1, format="%.2f", key="bin_weight")

# Generate Label
if st.button("Generate Label / Generar Etiqueta") and valid_selection:
    # Use Eastern Time
    eastern = pytz.timezone("US/Eastern")
    timestamp = datetime.datetime.now(eastern).strftime("%Y-%m-%d %H:%M:%S")

    width, height = landscape((6 * inch, 4 * inch))
    c = canvas.Canvas(PDF_FILE, pagesize=(width, height))

    font = "Helvetica-Bold"
    font_size = 40
    line_spacing = 0.6 * inch
    max_line_width = width - (1.0 * inch)

    def wrap_text(text, font, font_size, max_width, canvas_obj, max_lines=3):
        words = text.split()
        lines, current_line = [], ""
        for word in words:
            trial = f"{current_line} {word}".strip()
            if canvas_obj.stringWidth(trial, font, font_size) <= max_width:
                current_line = trial
            else:
                lines.append(current_line)
                current_line = word
                if len(lines) == max_lines - 1:
                    break
        lines.append(current_line)
        return lines[:max_lines]

    wrapped_lines = wrap_text(formula_name.upper(), font, font_size, max_line_width, c)
    top = height - (0.75 * inch if len(wrapped_lines) == 3 else 0.9 * inch if len(wrapped_lines) == 2 else 1.4 * inch)

    c.setFont(font, font_size)
    for i, line in enumerate(wrapped_lines):
        c.drawCentredString(width / 2, top - i * line_spacing, line)

    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(width / 2, height - 2.4 * inch, str(bottle_count))

    c.setFont("Helvetica", 20)
    c.drawCentredString(width / 2, height - 3.4 * inch, timestamp)

    c.showPage()
    c.save()

    # Save to CSV
    new_row = {
        "Timestamp": timestamp,
        "Formula Name": formula_name,
        "Bottle Count": bottle_count,
        "Weight per Bottle": weight_per_bottle,
        "Bin Gross Weight": bin_weight
    }

    if os.path.exists("label_log.csv"):
        df = pd.read_csv("label_log.csv")
        df = df._append(new_row, ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df.to_csv("label_log.csv", index=False)

    st.session_state.label_ready = True
    st.success("✅ Label created and data saved! / Etiqueta creada y datos guardados")

# Show download + print + reset buttons
if st.session_state.label_ready and os.path.exists(PDF_FILE):
    with open(PDF_FILE, "rb") as f:
        # Download button
        st.download_button("📄 Download Label / Descargar Etiqueta", f, file_name="label.pdf")

        # Print button via PDF base64 viewer
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_url = f"data:application/pdf;base64,{base64_pdf}"
        st.markdown(
            f'<a href="{pdf_url}" target="_blank">🖨️ Print Label / Imprimir Etiqueta</a>',
            unsafe_allow_html=True
        )

    # Reset prompt
    st.markdown("✅ After printing, click below to start the next label  \n✅ **Después de imprimir, haga clic abajo para comenzar la siguiente etiqueta**")
    if st.button("➡️ Start Next Label / Comenzar Siguiente Etiqueta"):
        st.session_state.clear_form = True
        st.rerun()

# Admin section (translations will be removed in future version)
st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.divider()
if st.checkbox("🔒 Admin: Show CSV download / Mostrar descarga de CSV"):
    if os.path.exists("label_log.csv"):
        with open("label_log.csv", "rb") as f:
            st.download_button("📊 Download CSV Log / Descargar CSV", f, file_name="label_log.csv")
    else:
        st.info("No CSV file found yet. / No se encontró archivo CSV aún.")
