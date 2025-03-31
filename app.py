import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Cambodia Education Dashboard", layout="wide")

# Load dataset from GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/bur3hani/camedu/main/cleaned_cambodia_education_2020_2021.csv"
    df = pd.read_csv(url)

    # Ensure required computed fields exist
    if 'Student–Teacher Ratio' not in df.columns:
        df['Student–Teacher Ratio'] = (df['Total Enrolment'] / df['Total Teachers']).round(2)
    if '% Girls Enrolled' not in df.columns:
        df['% Girls Enrolled'] = (df['Girls Enrolled'] / df['Total Enrolment'] * 100).round(2)
    if '% Female Teachers' not in df.columns:
        df['% Female Teachers'] = (df['Female Teachers'] / df['Total Teachers'] * 100).round(2)

    return df

# Load data
df = load_data()

# Title and intro
st.title("📘 Cambodia Education Equality Dashboard (2020–2021)")
st.markdown("""
This dashboard visualizes key public education indicators from Cambodia.
It highlights gender-based enrollment, teacher distribution, and repetition rates across provinces.
""")

# Province selector
province_list = sorted(df['Province'].unique())
selected_province = st.selectbox("Select a province to view:", province_list)
prov_df = df[df['Province'] == selected_province]

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("👧 % Girls Enrolled", f"{prov_df['% Girls Enrolled'].values[0]}%")
col2.metric("👩‍🏫 % Female Teachers", f"{prov_df['% Female Teachers'].values[0]}%")
col3.metric("📚 Student–Teacher Ratio", f"{prov_df['Student–Teacher Ratio'].values[0]}")

# Visual comparisons
st.subheader(f"📊 Enrollment & Staffing Breakdown for {selected_province}")
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# Enrollment barplot
sns.barplot(x=['Total Enrolled', 'Girls Enrolled'],
            y=[prov_df['Total Enrolment'].values[0], prov_df['Girls Enrolled'].values[0]],
            ax=ax[0], palette='Set2')
ax[0].set_title("Enrollment Breakdown")

# Teacher barplot
sns.barplot(x=['Total Teachers', 'Female Teachers'],
            y=[prov_df['Total Teachers'].values[0], prov_df['Female Teachers'].values[0]],
            ax=ax[1], palette='Set3')
ax[1].set_title("Teacher Breakdown")

st.pyplot(fig)

# Optional: Show full data
with st.expander("📂 Show full dataset"):
    st.dataframe(df)

st.markdown("---")
st.caption("Dashboard by @Bur3hani • Data from [GitHub](https://github.com/bur3hani/camedu)")
