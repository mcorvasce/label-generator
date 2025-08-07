import streamlit as st
from fpdf import FPDF
import datetime
import pandas as pd
import os

# CSV file name
CSV_FILE = "label_log.csv"

# Set up Streamlit
st.set_page_config(page_title="Label Generator", layout="centered")
st.title("📦 Bottle Bin Label Generator")

# Hide +/- steppers on number inputs
hide_number_input_style = """
    <style>
    [data-testid="stNumberInput"] button {
        display: none;
    }
    </style>
"""
st.markdown(hide_number_input_style, unsafe_allow_html=True)

# Dropdown for formula names
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

# User inputs
formula_name = st.selectbox("Formula Name", formula_names)
bottle_count = st.number_input("Bottle Count", min_value=0, step=1)
weight_per_bottle = st.number_input("Weight per Bottle (lbs)", min_value=0.0, step=0.01, format="%.2f")
bin_weight = st.number_input("Bin Net Weight (lbs)", min_value=0.0, step=0.1, format="%.2f")

# Generate label + log
if st.button("Generate Label"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PDF: landscape 6x4, only values
    pdf = FPDF(orientation='L', unit='in', format=(6, 4))
    pdf.add_page()
    pdf.set_font("Arial", "B", 30)
    pdf.cell(0, 1, txt=formula_name.upper(), ln=True, align="C")
    pdf.set_font("Arial", "B", 40)
    pdf.cell(0, 1, txt=str(bottle_count), ln=True, align="C")
    pdf.set_font("Arial", "", 18)
    pdf.cell(0, 1, txt=timestamp, ln=True, align="C")

    pdf_file = "label.pdf"
    pdf.output(pdf_file)

    # Full CSV logging
    new_row = {
        "Timestamp": timestamp,
        "Formula Name": formula_name,
        "Bottle Count": bottle_count,
        "Weight per Bottle": weight_per_bottle,
        "Bin Weight": bin_weight
    }

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = df._append(new_row, ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(CSV_FILE, index=False)

    # Confirmation and download
    st.success("✅ Label created and data saved!")

    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download Label PDF", f, file_name="label.pdf")
