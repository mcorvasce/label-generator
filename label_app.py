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

# Create Label
if st.button("Generate Label"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PDF generation
    pdf = FPDF(orientation='P', unit='in', format=(4, 6))
    pdf.add_page()
