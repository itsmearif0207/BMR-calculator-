import streamlit as st

st.title("BMR Calculator (Mifflin-St Jeor)")

# User inputs
sex = st.radio("Sex", ["Male", "Female"])
weight_lbs = st.number_input("Weight (lbs)", min_value=1.0, step=1.0)
height_ft = st.number_input("Height (feet)", min_value=0, step=1)
height_in = st.number_input("Height (inches)", min_value=0, step=1)
age = st.number_input("Age (years)", min_value=1, step=1)

# Conversion
weight_kg = weight_lbs * 0.453592
height_cm = ((height_ft * 12) + height_in) * 2.54

# BMR calculation
if sex == "Male":
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
else:
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

# Output
if st.button("Calculate BMR"):
    st.success(f"Your BMR is **{bmr:.2f} calories/day**")
