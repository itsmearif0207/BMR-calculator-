import streamlit as st

st.set_page_config(page_title="Fitness Calculator", page_icon="🔥")

st.title("Fitness Calculator")
st.write("Use the tabs below to switch between calculators.")

# Tabs
tab1, tab2 = st.tabs(["BMR Calculator", "Weight Loss Planner"])

# ----------------------------
# TAB 1: BMR Calculator
# ----------------------------
with tab1:
    st.header("BMR Calculator (Mifflin-St Jeor)")

    sex = st.radio("Sex", ["Male", "Female"], key="bmr_sex")
    weight_lbs = st.number_input("Weight (lbs)", min_value=1.0, step=1.0, key="bmr_weight")
    height_ft = st.number_input("Height (feet)", min_value=0, step=1, key="bmr_height_ft")
    height_in = st.number_input("Height (inches)", min_value=0, step=1, key="bmr_height_in")
    age = st.number_input("Age (years)", min_value=1, step=1, key="bmr_age")

    activity = st.selectbox(
        "Activity Level",
        [
            "Sedentary (little/no exercise)",
            "Lightly Active (1-3 days/week)",
            "Moderately Active (3-5 days/week)",
            "Very Active (6-7 days/week)",
            "Extra Active (physical job or 2x training)"
        ],
        key="bmr_activity"
    )

    # Conversion
    weight_kg = weight_lbs * 0.453592
    height_cm = ((height_ft * 12) + height_in) * 2.54

    # BMR calculation
    if sex == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Activity multipliers
    multipliers = {
        "Sedentary (little/no exercise)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725,
        "Extra Active (physical job or 2x training)": 1.9,
    }
    tdee = bmr * multipliers[activity]

    if st.button("Calculate BMR"):
        st.success(f"Your BMR is **{bmr:.0f} calories/day**")
        st.info(f"Your TDEE (with activity) is **{tdee:.0f} calories/day**")

# ----------------------------
# TAB 2: Weight Loss Planner
# ----------------------------
with tab2:
    st.header("Weight Loss Goal Planner")

    sex = st.radio("Sex", ["Male", "Female"], key="goal_sex")
    weight_lbs = st.number_input("Current Weight (lbs)", min_value=1.0, step=1.0, key="goal_weight")
    target_weight_lbs = st.number_input("Target Weight (lbs)", min_value=1.0, step=1.0, key="goal_target")
    days = st.number_input("Days to reach goal", min_value=1, step=1, key="goal_days")
    height_ft = st.number_input("Height (feet)", min_value=0, step=1, key="goal_height_ft")
    height_in = st.number_input("Height (inches)", min_value=0, step=1, key="goal_height_in")
    age = st.number_input("Age (years)", min_value=1, step=1, key="goal_age")

    activity = st.selectbox(
        "Activity Level",
        [
            "Sedentary (little/no exercise)",
            "Lightly Active (1-3 days/week)",
            "Moderately Active (3-5 days/week)",
            "Very Active (6-7 days/week)",
            "Extra Active (physical job or 2x training)"
        ],
        key="goal_activity"
    )

    # Conversion
    weight_kg = weight_lbs * 0.453592
    height_cm = ((height_ft * 12) + height_in) * 2.54

    # BMR calculation
    if sex == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    multipliers = {
        "Sedentary (little/no exercise)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725,
        "Extra Active (physical job or 2x training)": 1.9,
    }
    tdee = bmr * multipliers[activity]

    # Weight loss math
    if target_weight_lbs < weight_lbs:
        pounds_to_lose = weight_lbs - target_weight_lbs
        total_deficit = pounds_to_lose * 3500
        daily_deficit = total_deficit / days
        daily_calories = tdee - daily_deficit
    else:
        pounds_to_lose = 0
        daily_deficit = 0
        daily_calories = tdee

    if st.button("Calculate Goal"):
        st.write(f"**Your BMR:** {bmr:.0f} calories/day")
        st.write(f"**Your TDEE (with activity):** {tdee:.0f} calories/day")

        if pounds_to_lose > 0:
            st.write(f"**Goal:** Lose {pounds_to_lose:.1f} lbs in {days} days")
            st.write(f"**Daily Calorie Deficit Needed:** {daily_deficit:.0f} calories")
            st.success(f"🎯 Target intake: **{daily_calories:.0f} calories/day**")

            if daily_calories < 1200:
                st.warning("⚠️ This is very low. Extend your timeline for a safer plan.")
        else:
            st.info("Your target weight is not less than your current weight.")
