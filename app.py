# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os

st.set_page_config(page_title="Flight Segmentation", page_icon="✈️", layout="wide")

st.sidebar.title("📁 Navigation")
page = st.sidebar.radio("Go to:", ["Overview", "EDA", "Cluster Insight", "Recommendation", "Contact"])

# ✅ Upload CSV file
uploaded_file = st.file_uploader("📤 Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded and data loaded!")
else:
    df = pd.DataFrame()
    st.warning("⚠️ Harap upload file terlebih dahulu.")

# Tambahkan kolom 'route'
if not df.empty and 'route' not in df.columns:
    if 'source_city' in df.columns and 'destination_city' in df.columns:
        df['route'] = df['source_city'] + " → " + df['destination_city']

# Load framework image
if os.path.exists("framework_slide.jpeg"):
    framework_img = Image.open("framework_slide.jpeg")
else:
    framework_img = None

# Pages
if page == "Overview":
    st.title("✈️ Final Project – Flight Segmentation")
    st.write("Segmenting flights based on ticket characteristics to support strategic pricing and marketing strategies.")

    st.subheader("🔍 Business Objective")
    st.write("""
    - Identify different flight customer segments.
    - Help airlines and agencies design effective promotional and service strategies.
    """)

    st.subheader("🧠 Analytical Framework")
    if framework_img:
        st.image(framework_img, caption="CRISP-DM & Gartner Analytics Model", use_column_width=True)
    else:
        st.info("Gambar framework belum tersedia.")

    st.subheader("📊 Dataset Overview")
    if not df.empty:
        st.dataframe(df.head())
    else:
        st.info("Silakan upload file untuk melihat data.")

elif page == "EDA":
    st.title("📊 Exploratory Data Analysis")

    if df.empty:
        st.warning("Tidak ada data yang bisa dianalisis.")
    else:
        st.subheader("1. Distribution by Airline")
        fig1, ax1 = plt.subplots()
        sns.countplot(data=df, x='airline', order=df['airline'].value_counts().index, ax=ax1)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

        st.subheader("2. Price Distribution by Class")
        fig2, ax2 = plt.subplots()
        sns.boxplot(data=df, x='class', y='price', ax=ax2)
        st.pyplot(fig2)

        st.subheader("3. Average Price by Route")
        avg_price_route = df.groupby('route')['price'].mean().sort_values(ascending=False).head(10)
        st.bar_chart(avg_price_route)

elif page == "Cluster Insight":
    st.title("🔎 Cluster Insight & Interpretation")

    st.subheader("📊 Distribusi Segmen (Pie Chart)")
    if 'cluster' in df.columns:
        cluster_counts = df['cluster'].value_counts().sort_index()
        fig3, ax3 = plt.subplots()
        ax3.pie(cluster_counts.values, labels=[f"Cluster {i}" for i in cluster_counts.index],
                autopct='%1.1f%%', startangle=90, counterclock=False)
        ax3.axis('equal')
        st.pyplot(fig3)
    else:
        st.info("Kolom 'cluster' belum tersedia dalam dataset.")

    st.subheader("📌 Rangkuman Cluster")
    cluster_summary = pd.DataFrame({
        "Cluster": [0, 1, 2, 3],
        "Avg. Price": [9044.14, 5879.75, 55404.51, 8439.32],
        "Avg. Duration (hrs)": [7.86, 8.09, 14.71, 21.98],
        "Days Left": [14.38, 38.16, 25.79, 24.72]
    })
    st.dataframe(cluster_summary)

    st.markdown("""
    **Interpretasi Segmentasi:**
    - **Cluster 0**: Last-minute mid-range travelers  
    - **Cluster 1**: Budget leisure planners  
    - **Cluster 2**: Premium long-haul travelers  
    - **Cluster 3**: Budget long-stay travelers  
    """)

elif page == "Recommendation":
    st.title("💡 Strategic Recommendations")

    st.markdown("""
    - **Cluster 0** → Upselling & Fast-Track Access  
    - **Cluster 1** → Early-bird, Flash Sales, Group Bundles  
    - **Cluster 2** → Loyalty Programs, Lounge Access, Concierge  
    - **Cluster 3** → Long-stay Promos, Accommodation Bundles
    """)

    st.subheader("Promo Samples")
    st.markdown("""
    - ✨ **Weekend Flash Sale**  
      For routes like Delhi and Mumbai.

    - 🌙 **Midnight Deal**  
      Targeting flyers between 1–3 AM.

    - ⏳ **Early Bird Discount**  
      Book 60+ days early, get 20% off.
    """)

elif page == "Contact":
    st.title("📬 Contact")
    st.markdown("**Musdalifah Ahmad**")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/musdalifahahmad)")
    st.markdown("📧 musdalifahahmad5@gmail.com")
