import streamlit as st
import requests

st.set_page_config(page_title="Fitness Calculator", page_icon="🔥")

st.title("Fitness Calculator")
st.write("Use the tabs below to switch between calculators.")

# Tabs
# tab1, tab2 = st.tabs(["BMR Calculator", "Weight Loss"])
# tab1, tab2, tab3 = st.tabs(["BMR Calculator", "Weight Loss", "Fat Loss Planner"])
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 BMR Calculator",
    "🎯 Weight Loss Planner",
    "🔥 Fat Loss Planner",
    "🥗 Food Calorie Lookup"
])

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
            "Sedentary (little or no exercise)",
            "Lightly Active (exercise 1–3 days/week)",
            "Moderately Active (exercise 3–5 days/week)",
            "Very Active (exercise 6–7 days/week)",
            "Extra Active (hard physical job or 2x training)"
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
        "Sedentary (little or no exercise)": 1.2,
        "Lightly Active (exercise 1–3 days/week)": 1.375,
        "Moderately Active (exercise 3–5 days/week)": 1.55,
        "Very Active (exercise 6–7 days/week)": 1.725,
        "Extra Active (hard physical job or 2x training)": 1.9,
    }
    tdee = bmr * multipliers[activity]

    if st.button("Calculate BMR & TDEE"):
        st.success(f"**Basal Metabolic Rate (BMR):** {bmr:.0f} calories/day")
        st.info(f"**Total Daily Energy Expenditure (TDEE):** {tdee:.0f} calories/day \n\n"
                f"TDEE is the number of calories you burn per day including activity.")

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


# ----------------------------
# TAB 3: Fat Loss Planner
# ----------------------------
with tab3:
    st.header("Fat Loss Planner (3500 Calorie Rule)")

    pounds_to_lose = st.number_input("Target Fat Loss (lbs)", min_value=1.0, step=0.5, key="fatloss_pounds")

    option = st.radio("Plan by:", ["Daily Calorie Deficit", "Number of Days"], key="fatloss_option")

    if option == "Daily Calorie Deficit":
        daily_deficit = st.number_input("Daily Calorie Deficit (calories/day)", min_value=100, step=50, key="fatloss_deficit")
        total_deficit = pounds_to_lose * 3500
        days_needed = total_deficit / daily_deficit if daily_deficit > 0 else 0

        if st.button("Calculate Fat Loss (by deficit)"):
            st.success(f"To lose **{pounds_to_lose:.1f} lbs**, "
                       f"with a **{daily_deficit:.0f} calorie/day deficit**, "
                       f"it will take about **{days_needed:.0f} days**.")

            # Visualization: progress bar timeline
            st.subheader("Timeline Visualization")
            st.progress(min(1.0, daily_deficit / 1000))  # shows progress relative to 1000 deficit/day

    else:  # by number of days
        days = st.number_input("Number of Days", min_value=1, step=1, key="fatloss_days")
        total_deficit = pounds_to_lose * 3500
        daily_deficit = total_deficit / days if days > 0 else 0

        if st.button("Calculate Fat Loss (by days)"):
            st.success(f"To lose **{pounds_to_lose:.1f} lbs** in **{days:.0f} days**, "
                       f"you need a **{daily_deficit:.0f} calorie/day deficit**.")

            # Visualization: bar chart
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            ax.bar(["Daily Deficit Needed"], [daily_deficit])
            ax.set_ylabel("Calories/day")
            ax.set_title("Required Calorie Deficit")
            st.pyplot(fig)



# ----------------------------
# TAB 4: Food Calorie Lookup
# ----------------------------
with tab4:
    st.header("Food Calorie Lookup (USDA API)")

    food_query = st.text_input("Search for a food (e.g., apple, chicken, rice)", key="food_query")
    grams = st.number_input("Enter amount (grams)", min_value=1, step=1, key="food_weight")

    if st.button("Get Calories"):
        api_key = "pzScBHFYwdQzrtod4LLvcEDo2CtbEUcbZnp"
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_query}&pageSize=5&api_key={api_key}"

        try:
            response = requests.get(url)
            data = response.json()

            if "foods" not in data or len(data["foods"]) == 0:
                st.error("No results found. Try another food.")
            else:
                # Show top 5 matches as a selectbox
                food_names = [f["description"] for f in data["foods"]]
                selected_food = st.selectbox("Select a match", food_names)

                # Find selected food's nutrients
                chosen = next(f for f in data["foods"] if f["description"] == selected_food)
                nutrients = {n["nutrientName"]: n["value"] for n in chosen["foodNutrients"]}

                # Calories per 100g
                calories_per_100g = nutrients.get("Energy", None)

                if calories_per_100g:
                    total_calories = (calories_per_100g * grams) / 100
                    st.success(f"{grams} g of {selected_food} ≈ **{total_calories:.1f} calories**")
                else:
                    st.error("Calories not found for this food.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

