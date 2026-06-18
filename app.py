import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression


st.set_page_config(
    page_title="Google Play Store Analytics",
    page_icon="📱",
    layout="wide"
)

# loading dataset

@st.cache_data
def load_data():
    return pd.read_excel("cleaned dataset/googleplaycleaneddf.xlsx")

@st.cache_resource
def train_model(df):
    features = ["Category", "Type", "Content Rating", "Price", "Size"]
    target = "Success"

    data = df.copy()
    data["Success"] = np.where(data["Rating"] >= 4.2, 1, 0)
    data = data[features + [target]].dropna()

    X = data[features]
    y = data[target]

    num_cols = ["Price", "Size"]
    cat_cols = ["Category", "Type", "Content Rating"]

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=2000))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    return model

try:
    df = load_data()
    model = train_model(df)
except Exception as e:
    st.error(f"Error loading data or training model: {e}")
    st.stop()

# sidebar

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Overview", "Dataset", "EDA Dashboard", "Success Predictor"])


# OVERVIEW

if page == "Overview":
    st.image("screenshots/googleplayimage.png", width=500)
    st.title("📱 Google Play Store Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Apps", f"{len(df):,}")
    col2.metric("Average Rating", round(df["Rating"].mean(), 2))
    col3.metric("Average Installs", f"{int(df['Installs'].mean()):,}")
    col4.metric("Average Price", f"${round(df['Price'].mean(), 2)}")

    st.divider()

    st.subheader("📌 Executive Summary")

    st.write("""
    This project analyzes over 8,000 Google Play Store applications to identify the factors influencing app performance, user engagement, ratings, and installs.

    The analysis combines data cleaning, exploratory data analysis, statistical testing, machine learning, and interactive dashboards to uncover actionable business insights for developers and product teams.
    """)

    st.subheader("📈 Key Findings")

    st.markdown("""
    - Communication apps achieved the highest average installs (**43.1M installs**).
    - Social apps recorded over **27M average installs**, indicating strong user demand.
    - Reviews and installs showed a strong positive correlation (**r = 0.62**).
    - Paid apps achieved a higher average rating (**4.26**) than free apps (**4.17**).
    - Ratings differed significantly across categories (**ANOVA p-value < 0.05**).
    - More than **75% of applications were free**, highlighting the dominance of freemium business models.
    """)

    st.subheader("💼 Business Insights & Recommendations")

    st.markdown("""
    ##### 1. Focus on High-Growth Categories

    - **Evidence:** Communication apps averaged **43.1M installs**, while Social apps averaged **27.0M installs**.
    - **Recommendation:** Developers seeking large-scale user acquisition should prioritize categories with broad daily usage and strong network effects.


    ##### 2. Leverage User Engagement

    - **Evidence:** Reviews and installs exhibited a strong positive correlation (**r = 0.62**).
    - **Recommendation:** Encouraging reviews and ratings can improve visibility, credibility, and long-term app growth.


    ##### 3. Benchmark Within Categories

    - **Evidence:** ANOVA testing produced a statistically significant result (**p-value = 2.20e-30**), indicating that ratings vary across categories.
    - **Recommendation:** Compare performance against category-specific competitors rather than overall Play Store averages.


    ##### 4. Consider Freemium Monetization

    - **Evidence:** More than **75% of applications were free**, and the median app price was **$0**.
    - **Recommendation:** Ad-supported, subscription-based, or freemium models may be more effective for maximizing adoption.


    ##### 5. Evaluate Pricing Strategy Carefully

    - **Evidence:** Paid applications achieved an average rating of **4.26**, compared to **4.17** for free apps.
    - **Recommendation:** Premium pricing may be suitable for niche products that can clearly demonstrate value to users.
    """)

# Dataset


elif page == "Dataset":
    st.title("📋 Dataset Preview")
    st.write("Shape:", df.shape)
    st.dataframe(df.head(20))


# EDA dashboard

elif page == "EDA Dashboard":

    st.title("📊 EDA Dashboard")

    col1, col2 = st.columns(2)

    # Chart 1
    with col1:
        st.subheader("Top Categories by Installs")

        installs_by_category = (
            df.groupby("Category")["Installs"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(installs_by_category)

    # Chart 2
    with col2:
        st.subheader("Top Categories by Rating")

        rating_by_category = (
            df.groupby("Category")["Rating"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(rating_by_category)

    st.divider()

    col3, col4 = st.columns(2)

    # Chart 3
    with col3:
        st.subheader("Free vs Paid Apps")

        type_counts = (
            df["Type"]
            .value_counts()
        )

        st.bar_chart(type_counts)

    # Chart 4
    with col4:
        st.subheader("Content Rating Distribution")

        content_counts = (
            df["Content Rating"]
            .value_counts()
        )

        st.bar_chart(content_counts)


    st.image("PowerBI/pb1.png", caption="PowerBI Dashboard 1")  
    st.image("PowerBI/pb2.png", caption="PowerBI Dashboard 2")   


# Success Prediction (Logistic Regression)


elif page == "Success Predictor":
    st.title("🤖 App Success Predictor using Logistic Regression")
    st.markdown("Fill in the app details. The model predicts whether the app will have a **Rating ≥ 4.2** (Successful).")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox("Category", sorted(df["Category"].dropna().unique()))
        app_type = st.selectbox("Type", sorted(df["Type"].dropna().unique()))
        content_rating = st.selectbox("Content Rating", sorted(df["Content Rating"].dropna().unique()))

    with col2:
        price = st.number_input("Price ($)", min_value=0.0, value=0.0, step=0.99)
        size = st.number_input("Size (MB)", min_value=0.0, value=20.0, step=1.0)

    st.divider()

    if st.button("🔮 Predict Success", use_container_width=True, type="primary"):

        input_data = pd.DataFrame([{
            "Category": category,
            "Type": app_type,
            "Content Rating": content_rating,
            "Price": price,
            "Size": size
        }])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        prob_success = probability[1]
        prob_fail = probability[0]

        st.subheader("📊 Prediction Result")

        res_col1, res_col2, res_col3 = st.columns(3)

        if prediction == 1:
            res_col1.success("✅ SUCCESSFUL APP")
            res_col1.caption("Predicted Rating ≥ 4.2")
        else:
            res_col1.error("❌ NOT SUCCESSFUL")
            res_col1.caption("Predicted Rating < 4.2")

        res_col2.metric("Success Probability", f"{prob_success * 100:.1f}%")
        res_col3.metric("Failure Probability", f"{prob_fail * 100:.1f}%")

        st.markdown("#### Model Confidence")
        st.progress(float(prob_success))
        st.caption(f"The model is **{prob_success * 100:.1f}% confident** this app will be successful.")

    with st.expander("📋 View Input Summary"):
        st.json({
            "Category": category,
            "Type": app_type,
            "Content Rating": content_rating,
            "Price": price,
            "Size": size
        })
