import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, inch
from textwrap import wrap
import datetime
import pandas as pd
import os

# File paths
CSV_FILE = "label_log.csv"
PDF_FILE = "label.pdf"

# Set up Streamlit
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

# Dropdown options
formula_names = [
    "Almost Perfect Citrus Carrot", "Apple Celery", "Better Mood Shot - Functional Mother",
    "Blue Sipper", "Breastfeeding - Functional Mother", "Calm - Bridal", "Celery Juice",
    "Chocolate Cashew", "Chocolate Protein", "Citrus Carrot", "Citrus Mint",
    "Clementine Creamsicle", "Cookies & Cream", "Cool Greens", "Craving Crusher Shot",
    "Deblot - Bridal", "Detox - Bridal", "Energy - Bridal", "Ginger Turmeric", "Green Sipper",
    "Hair - Bridal", "Lemony Greens", "Orange Sipper", "Peanut Butter", "Peanut Butter Cup",
    "Pina Colada", "Pink Sipper", "Protein Greens", "Protein Shot", "Purple Sipper",
    "Red Sipper", "Replenish Shot", "Salt Water Refrigerant Bottle", "Skin Glow - Bridal",
    "Skinny Boost Shot", "Sleep - Bridal", "Sleep Shot", "Strawberry Greens", "Strong & Lean",
    "Sweet Greens", "Sweet Roots", "Tarte Greens", "Tropical Greens", "Tropical Sunrise",
    "Vanilla Cashew", "Yellow Sipper"
]

# Input fields (English + Spanish)
formula_name = st.selectbox("Formula Name (Nombre de la Fórmula)", formula_names)
bottle_count = st.number_input("Bottle Count (Cantidad de Botellas)", min_value=0, step=1)
weight_per_bottle = st.number_input("Weight per Bottle (Peso por Botella, lbs)", min_value=0.0, step=0.01, format="%.2f")
bin_weight = st.number_input("Bin Gross Weight (Peso Bruto del Bin, lbs)", min_value=0.0, step=0.1, format="%.2f")

# Generate label
if st.button("Generate Label / Generar Etiqueta"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create PDF with reportlab
    width, height = landscape((6 * inch, 4 * inch))
    c = canvas.Canvas(PDF_FILE, pagesize=(width, height))

    # Formula wrapping and positioning
    formula_font = "Helvetica-Bold"
    formula_font_size = 40
    side_margin = 0.5 * inch
    max_text_width = width - 2 * side_margin

    c.setFont(formula_font, formula_font_size)
    wrapped_lines = []
    for line in wrap(formula_name.upper(), width=40):
        text_width = c.stringWidth(line, formula_font, formula_font_size)
        if text_width <= max_text_width:
            wrapped_lines.append(line)
        else:
            wrapped_lines += wrap(line, width=20)
    wrapped_lines = wrapped_lines[:2]

    # Adjust top margin based on line count
    if len(wrapped_lines) == 1:
        top = height - 1.4 * inch
    else:
        top = height - 0.9 * inch

    # Draw formula lines
    line_spacing = 0.6 * inch
    for i, line in enumerate(wrapped_lines):
        c.drawCentredString(width / 2, top - i * line_spacing, line)

    # Draw bottle count
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(width / 2, height - 2.4 * inch, str(bottle_count))

    # Draw timestamp
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

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = df._append(new_row, ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(CSV_FILE, index=False)

    st.success("✅ Label created and data saved! / Etiqueta creada y datos guardados")

    # PDF download
    with open(PDF_FILE, "rb") as f:
        st.download_button("📄 Download Label / Descargar Etiqueta", f, file_name="label.pdf")

# Spacer to push admin tools down the page
st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.divider()

# Admin-only CSV download
if st.checkbox("🔒 Admin: Show CSV download"):
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "rb") as f:
            st.download_button("📊 Download CSV Log / Descargar CSV", f, file_name="label_log.csv")
    else:
        st.info("No CSV file found yet.")
