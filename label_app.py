import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Label Generator", layout="centered")

st.title("📦 4x6 Label Generator")

with st.form("label_form"):
    formula = st.text_input("Formula Name", placeholder="e.g., Sweet Greens")
    weight = st.text_input("Weight of One Bottle (lbs)", placeholder="e.g., 2.3")
    net_weight = st.text_input("Bin Net Weight (lbs)", placeholder="e.g., 524")
    count = st.text_input("Bottle Count", placeholder="e.g., 228")
    submitted = st.form_submit_button("Generate Label")

if submitted:
    # Create a 4x6 PDF label
    pdf = FPDF("P", "in", (4, 6))  # 4x6 inches
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    pdf.cell(0, 0.4, f"Formula: {formula}", ln=1)
    pdf.cell(0, 0.4, f"Bottle Weight: {weight} lbs", ln=1)
    pdf.cell(0, 0.4, f"Bin Net Weight: {net_weight} lbs", ln=1)
    pdf.cell(0, 0.4, f"Bottle Count: {count}", ln=1)
    pdf.cell(0, 0.4, f"Date: {now}", ln=1)

    # Save to in-memory file
    pdf_output = pdf.output(dest='S').encode('latin-1')

    st.success("✅ Label ready to download and print!")
    st.download_button(
        label="Download 4x6 Label PDF",
        data=pdf_output,
        file_name=f"label_{formula}_{now}.pdf",
        mime="application/pdf"
    )
