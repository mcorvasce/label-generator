import streamlit as st
from fpdf import FPDF
import datetime
import requests

st.set_page_config(page_title="Label Generator", layout="centered")
st.title("📦 4x6 Label Generator")

# NoCodeAPI endpoint (from Streamlit secrets)
NOCODE_API_URL = st.secrets["nocode_api_url"]

# Dropdown options
formulas = [
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

# Form for user inputs
with st.form("label_form"):
    formula = st.selectbox("Formula Name", formulas)
    weight = st.text_input("Weight of One Bottle (lbs)", placeholder="e.g., 2.3")
    net_weight = st.text_input("Bin Net Weight (lbs)", placeholder="e.g., 524")
    count = st.text_input("Bottle Count", placeholder="e.g., 228")
    submitted = st.form_submit_button("Generate Label")

if submitted:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Generate PDF label
    pdf = FPDF("P", "in", (4, 6))
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 0.4, f"Formula: {formula}", ln=1)
    pdf.cell(0, 0.4, f"Bottle Weight: {weight} lbs", ln=1)
    pdf.cell(0, 0.4, f"Bin Net Weight: {net_weight} lbs", ln=1)
    pdf.cell(0, 0.4, f"Bottle Count: {count}", ln=1)
    pdf.cell(0, 0.4, f"Date: {now}", ln=1)

    pdf_output = pdf.output(dest="S").encode("latin-1")

    # Log to Google Sheet via NoCodeAPI
    try:
        payload = {
            "data": [[now, formula, weight, net_weight, count]]
        }
        response = requests.post(NOCODE_API_URL, json=payload)
        if response.status_code == 200:
            st.success("✅ Label generated and logged successfully.")
        else:
            st.warning("⚠️ Label created, but failed to log to sheet.")
    except Exception as e:
        st.warning(f"⚠️ Error logging to sheet: {e}")

    # Download button
    st.download_button(
        label="Download 4x6 Label PDF",
        data=pdf_output,
        file_name=f"label_{formula}_{now}.pdf",
        mime="application/pdf"
    )
