import streamlit as st
import pandas as pd
import plotly.express as px
from script import generate_report

st.set_page_config(page_title="DataSage", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
.metric-title {
    color: #94a3b8;
    font-size: 14px;
}
.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("## 📊 DataSage")
    st.markdown("**From Data to Decisions—Instantly**")

    st.markdown("---")

    st.markdown("### ⚙️ Workflow")
    st.markdown("""
    1. Upload Excel  
    2. Map columns  
    3. Generate report  
    4. Download  
    """)

    st.markdown("---")
    st.info("Tip: Clean column names = better results")

    st.markdown("---")
    st.caption("Built by Satya Sagari")

# ------------------ HEADER ------------------
st.markdown("""
<h1 style='text-align: center;'>
Data<span style='color:#22C55E;'>Sage</span>
</h1>
<p style='text-align: center; color:#94a3b8; font-size:18px;'>
From Data to Decisions—Instantly
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------ UPLOAD ------------------
st.markdown("### 📂 Upload Excel File")

# Sample file download
with open("input.xlsx", "rb") as f:
    st.download_button("📥 Download Sample Excel", f, "input.xlsx")

uploaded_file = st.file_uploader("Drag & drop or browse", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    st.markdown("### 👀 Data Preview")
    st.dataframe(df.head())

    st.success("File uploaded successfully")
    st.success("🔒 Your data is processed securely. No data is stored.")

    # ------------------ COLUMN MAPPING ------------------
    st.markdown("### 🔄 Column Mapping")
    st.info("Select correct columns (Date = date field, Sales = numeric values, etc.)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        date_col = st.selectbox("Date", df.columns)

    with col2:
        sales_col = st.selectbox("Sales", df.columns)

    with col3:
        product_col = st.selectbox("Product", df.columns)

    with col4:
        city_col = st.selectbox("City", df.columns)

    if len({date_col, sales_col, product_col, city_col}) < 4:
        st.error("Select different columns")
        st.stop()

    st.markdown("---")

    # ------------------ BUTTON ------------------
    st.markdown("""
    ### 📦 Your report will include:
    - Summary metrics  
    - Monthly sales chart  
    - City-wise analysis  
    """)

    if st.button("🚀 Generate Report"):

        with st.spinner("Processing..."):

            report_path, total_sales, avg_sales, top_product_name, top_product_value, monthly_sales, sales_by_city = generate_report(
                df, date_col, sales_col, product_col, city_col
            )

        st.success("Report generated successfully")

        # ------------------ METRICS ------------------
        st.markdown("### 📊 Key Metrics")

        m1, m2, m3 = st.columns(3)

        m1.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Sales</div>
            <div class="metric-value">₹{total_sales:,}</div>
        </div>
        """, unsafe_allow_html=True)

        m2.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Top Product</div>
            <div class="metric-value">{top_product_name}</div>
        </div>
        """, unsafe_allow_html=True)

        m3.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Sale</div>
            <div class="metric-value">₹{avg_sales:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ------------------ CHARTS ------------------
        st.markdown("### 📈 Insights")

        c1, c2 = st.columns(2)

        # Monthly Chart
        with c1:
            monthly_sales.index = monthly_sales.index.astype(str)

            fig = px.line(
                x=monthly_sales.index,
                y=monthly_sales.values,
                markers=True
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Month",
                yaxis_title="Sales",
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

        # City Chart
        with c2:
            fig2 = px.bar(
                x=sales_by_city.index,
                y=sales_by_city.values
            )

            fig2.update_layout(
                template="plotly_dark",
                xaxis_title="City",
                yaxis_title="Sales",
                showlegend=False
            )

            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # ------------------ DOWNLOAD ------------------
        st.markdown("### 📥 Download Report")

        with open(report_path, "rb") as file:
            st.download_button(
                label="Download Excel Report",
                data=file,
                file_name="DataSage_Report.xlsx"
            )
