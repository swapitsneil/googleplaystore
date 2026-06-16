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
    st.title("📱 Google Play Store Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Apps", f"{len(df):,}")
    col2.metric("Average Rating", round(df["Rating"].mean(), 2))
    col3.metric("Average Installs", f"{int(df['Installs'].mean()):,}")
    col4.metric("Average Price", f"${round(df['Price'].mean(), 2)}")

    st.divider()
    st.subheader("Project Overview")
    st.write("""
    This project analyzes Google Play Store applications using:
    
    - Data Cleaning
    - Exploratory Data Analysis
    - Descriptive & Inferential Statistics
    - Machine Learning (Logistic Regression & Linear Regression)
    - Streamlit Deployment
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

    with col1:
        st.subheader("Top Categories by Installs")
        installs_by_category = (
            df.groupby("Category")["Installs"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        st.bar_chart(installs_by_category)

    with col2:
        st.subheader("Top Categories by Rating")
        rating_by_category = (
            df.groupby("Category")["Rating"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        st.bar_chart(rating_by_category)


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