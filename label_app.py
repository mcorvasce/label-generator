import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, inch
import datetime
import pandas as pd
import os

# Output files
CSV_FILE = "label_log.csv"
PDF_FILE = "label.pdf"

# Streamlit setup
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

# Initialize session state if needed
for field in ["formula_name", "bottle_count", "weight_per_bottle", "bin_weight", "generated"]:
    if field not in st.session_state:
        st.session_state[field] = None if field == "formula_name" else 0 if "weight" in field else 0

# Clear inputs if label was just generated
if st.session_state.generated:
    st.session_state.formula_name = None
    st.session_state.bottle_count = 0
    st.session_state.weight_per_bottle = 0.0
    st.session_state.bin_weight = 0.0
    st.session_state.generated = False

# Inputs (bilingual)
formula_name = st.selectbox("Formula Name (Nombre de la Fórmula)", formula_names, index=formula_names.index(st.session_state.formula_name) if st.session_state.formula_name else 0)
bottle_count = st.number_input("Bottle Count (Cantidad de Botellas)", min_value=0, step=1, value=st.session_state.bottle_count)
weight_per_bottle = st.number_input("Weight per Bottle (Peso por Botella, lbs)", min_value=0.0, step=0.01, format="%.2f", value=st.session_state.weight_per_bottle)
bin_weight = st.number_input("Bin Gross Weight (Peso Bruto del Bin, lbs)", min_value=0.0, step=0.1, format="%.2f", value=st.session_state.bin_weight)

# Handle label creation
if st.button("Generate Label / Generar Etiqueta"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ReportLab PDF generation
    width, height = landscape((6 * inch, 4 * inch))
    c = canvas.Canvas(PDF_FILE, pagesize=(width, height))

    # Wrapping logic
    font = "Helvetica-Bold"
    font_size = 40
    max_line_width = width - (1.0 * inch)
    line_spacing = 0.6 * inch

    def split_lines(text, font, font_size, max_width, canvas_obj, max_lines=3):
        words = text.split()
        lines = []
        current_line = ""
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

    # Apply split
    wrapped_lines = split_lines(formula_name.upper(), font, font_size, max_line_width, c, max_lines=3)
    top = height - 0.75 * inch if len(wrapped_lines) == 3 else (height - 0.9 * inch if len(wrapped_lines) == 2 else height - 1.4 * inch)

    # Draw formula name
    c.setFont(font, font_size)
    for i, line in enumerate(wrapped_lines):
        c.drawCentredString(width / 2, top - i * line_spacing, line)

    # Draw bottle count
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(width / 2, height - 2.4 * inch, str(bottle_count))

    # Draw timestamp
    c.setFont("Helvetica", 20)
    c.drawCentredString(width / 2, height - 3.4 * inch, timestamp)

    # Save PDF
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

    # Set fields to clear
    st.session_state.generated = True
    st.session_state.formula_name = formula_name
    st.session_state.bottle_count = bottle_count
    st.session_state.weight_per_bottle = weight_per_bottle
    st.session_state.bin_weight = bin_weight

    # Show download button
    with open(PDF_FILE, "rb") as f:
        st.download_button("📄 Download Label / Descargar Etiqueta", f, file_name="label.pdf")

# Spacer before admin section
st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.divider()

# Admin CSV download
if st.checkbox("🔒 Admin: Show CSV download"):
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "rb") as f:
            st.download_button("📊 Download CSV Log", f, file_name="label_log.csv")
    else:
        st.info("No CSV file found yet.")
