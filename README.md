# 📱 Google Play Store Data Analysis Project

## 📌 Project Overview

This project performs an in-depth **Exploratory Data Analysis (EDA)**, **Descriptive Statistics**, and **Inferential Statistics** on the Google Play Store dataset to uncover insights about app performance, ratings, installs, categories, pricing, reviews, and user sentiment.

The objective is to transform raw app-store data into meaningful business insights and build a strong foundation for future Machine Learning models that can predict app success, ratings, installs, and user engagement.

---

## 🎯 Project Goals

- Understand the structure and quality of Google Play Store data
- Perform extensive data cleaning and preprocessing
- Analyse app ratings, installs, reviews, pricing, and categories
- Generate business insights using visualisations
- Apply statistical techniques to validate assumptions
- Prepare the dataset for future Machine Learning applications

---

## 📂 Dataset Information

This project uses two datasets:

### 1. Google Play Store Apps Dataset
Contains information about:

- App Name
- Category
- Rating
- Reviews
- Size
- Installs
- Type (Free/Paid)
- Price
- Content Rating
- Genres
- Last Updated

### 2. Google Play Store User Reviews Dataset
Contains:

- User Reviews
- Sentiment
- Sentiment Polarity
- Sentiment Subjectivity

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Jupyter Notebook

---

## 📊 Exploratory Data Analysis (EDA)

The notebook includes extensive EDA covering:

### Data Understanding
- Dataset shape
- Data types
- Missing value analysis
- Duplicate record analysis

### Data Cleaning
- Handling missing values
- Removing duplicates
- Data type conversions
- Cleaning installs and price columns
- Standardising categorical variables

### Univariate Analysis
- Rating distribution
- Install distribution
- Price distribution
- Category frequency analysis

### Bivariate Analysis
- Reviews vs Installs
- Rating vs Reviews
- Category vs Rating
- Free vs Paid Apps

### Multivariate Analysis
- Correlation analysis
- Category-based performance analysis
- Sentiment impact analysis

---

## 📈 Statistical Analysis

### Descriptive Statistics

The project calculates:

- Mean
- Median
- Mode
- Standard Deviation
- Variance
- Quartiles
- Distribution Analysis

### Correlation Analysis

Relationship analysis between:

- Ratings
- Reviews
- Installs
- Sentiment Scores
- App Pricing

### Inferential Statistics

#### Hypothesis Testing

**Free vs Paid App Ratings**

- Null Hypothesis (H₀):
  Mean ratings of Free and Paid apps are equal

- Alternative Hypothesis (H₁):
  Mean ratings of Free and Paid apps are different

#### ANOVA Test

**Ratings Across Categories**

Used to determine whether app categories have significantly different rating distributions.

---

## 📊 Key Visualizations

The notebook includes visualisations such as:

- Rating Distribution
- Category Distribution
- Correlation Heatmap
- Free vs Paid Rating Boxplot
- Reviews vs Installs Scatterplot
- Sentiment vs Rating Analysis
- Category-wise Rating Distribution
- Top Categories by Installs
- Top Categories by Ratings

---

## 🔍 Major Insights

Some insights extracted from the analysis include:

- Certain categories dominate total installs.
- App ratings vary significantly across categories.
- Reviews and installs show a strong positive relationship.
- Free and paid apps exhibit different rating behaviours.
- User sentiment can influence overall app ratings.
- Category selection plays an important role in app performance.

---

## 📁 Project Structure

```text
Google-Play-Store-EDA/
│
├── googleplayeda.ipynb
├── googleplaystore.csv
├── googleplaystore_user_reviews.csv
├── README.md
│
└── future_ml_models/
```

---

## 🚀 Future Work

This project is intentionally designed as the first phase of a larger analytics pipeline.

### Upcoming Machine Learning Tasks

#### Regression Models

Predict:

- App Rating
- Number of Installs
- User Engagement Metrics

Potential algorithms:

- Linear Regression
- Random Forest Regressor
- XGBoost Regressor

#### Classification Models

Predict:

- High Performing Apps
- Successful vs Unsuccessful Apps
- Sentiment Categories

Potential algorithms:

- Logistic Regression
- Random Forest
- XGBoost
- LightGBM

#### Advanced Analytics

- Feature Engineering
- Feature Selection
- Model Explainability (SHAP)
- Hyperparameter Tuning
- Cross Validation

---

## 💡 Business Applications

This analysis can help:

- App Developers
- Product Managers
- Marketing Teams
- Data Analysts

to understand:

- What drives app success
- Which categories perform best
- User sentiment patterns
- Factors affecting ratings and installs

---

## 📚 Learning Outcomes

Through this project, I practised:

- Data Cleaning
- Data Wrangling
- Exploratory Data Analysis
- Descriptive Statistics
- Inferential Statistics
- Hypothesis Testing
- ANOVA
- Data Visualisation
- Business Insight Generation

---

## 👨‍💻 Author

**Swap Nicolson**

Aspiring Data Analyst focused on:

- Data Analytics
- Statistics
- Machine Learning
- Business Intelligence
- Power BI
- Python

---

⭐ If you found this project useful, consider giving it a star.
