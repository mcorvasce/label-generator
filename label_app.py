import streamlit as st
from fpdf import FPDF
import datetime
import requests

# Set page configuration
st.set_page_config(page_title="Label Generator", layout="centered")

# NoCodeAPI endpoint (replace with your actual URL or use Streamlit secrets)
NOCODE_API_URL = st.secrets["nocode_api_url"]

# Formula options
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

# Title
st.title("📦 4x6 Label Generator")

# Input form
formula = st.selectbox("Formula Name", formulas)
weight = st.text_input("Weight of One Bottle (lbs)", placeholder="e.g., 2.3")
net_weight = st.text_input("Bin Net Weight (lbs)", placeholder="e.g., 524")
count = st.text_input("Bottle Count", placeholder="e.g., 228")

# C
