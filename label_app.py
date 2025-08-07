import streamlit as st
from fpdf import FPDF
import datetime
import pandas as pd
import os
import math

# CSV file name
CSV_FILE = "label_log.csv"

# Set up Streamlit
st.set_page_config(page_title="Label Generator", layout="centered")
st.title("📦 Bottle Bin Label Generator")

# Hide +/- buttons
hide_number_input_style = """
    <style>
    [data-testid="stNumberInput"] button {
        display: none;
    }
    </style>
"""
st.markdown(hide_number_input_style, unsafe_allow_html=True)

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

# Inputs
formula_name = st.selectbox("Formula Name", formula_names)
bottle_count = st.number_input("Bottle Count", min_value=0, step=1)
weight_per_bottle = st.number_input("Weight per Bottle (lbs)", min_value=0.0, step=0.01, format="%.2f")
bin_weight = st.number_input("Bin Net Weight (lbs)", min_value=0.0, step=0.1, format="%.2f")

# Custom class to enable rotation in FPDF
class PDF(FPDF):
    def rotate(self, angle, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        self._out(f'q {math.cos(math.radians(angle)):.5f} {math.sin(math.radians(angle)):.5f} '
                  f'{-math.sin(math.radians(angle)):.5f} {math.cos(math.radians(angle)):.5f} '
                  f'{x * self.k:.2f} {y * self.k:.2f} cm')
    
    def rotate_text(self, x, y, txt, angle, font_size=12, font_weight='', align='C'):
        self.rotate(angle, x, y)
        self.set_xy(x, y)
        self.set_font("Arial", font_weight, font_size)
        self.cell(0, 0, txt, align=align)
        self._out('Q')  # reset rotation

# Label generation
if st.button("Generate Label"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PDF 6x4 inches, landscape
    pdf = PDF(orientation='L', unit='in', format=(6, 4))
    pdf.add_page()

    # Rotated text
    center_x = 3  # middle of 6-inch width
    center_y = 2  # middle of 4-inch height

    pdf.rotate_text(center_x, center_y - 0.8, formula_name.upper(), angle=90, font_size=26, font_weight='B')
    pdf.rotate_text(center_x, center_y, str(bottle_count), angle=90, font_size=36, font_weight='B')
    pdf.rotate_text(center_x, center_y + 0.8, timestamp, angle=90, font_size=16, font_weight='')

    pdf_file = "label.pdf"
    pdf.output(pdf_file)

    # Append full data to CSV
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

    # UI confirmation
    st.success("✅ Label created and data saved!")

    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download Rotated Label PDF", f, file_name="label.pdf")
