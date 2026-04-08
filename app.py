import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from script import generate_report

st.set_page_config(page_title="DataSage", layout="centered")

st.title("⚡ DataSage")
st.caption("From Data to Decisions—Instantly")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    columns = df.columns.tolist()

    # Column mapping
    date_col = st.selectbox("Select Date Column", columns)
    sales_col = st.selectbox("Select Sales Column", columns)
    product_col = st.selectbox("Select Product Column", columns)
    city_col = st.selectbox("Select City Column", columns)

    if len({date_col, sales_col, product_col, city_col}) < 4:
        st.error("Please select different columns")
        st.stop()

    # Generate report
    report_path, total_sales, avg_sales, top_product_name, top_product_value, monthly_sales, sales_by_city = generate_report(
        df, date_col, sales_col, product_col, city_col
    )

    # Summary
    st.subheader("📊 Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"₹{total_sales:,}")
    col2.metric("Top Product", top_product_name)
    col3.metric("Avg Sale", f"₹{avg_sales:.2f}")

    # Charts
    st.subheader("📈 Monthly Sales")

    fig, ax = plt.subplots()
    monthly_sales.index = monthly_sales.index.astype(str)

    ax.plot(monthly_sales.index, monthly_sales.values, marker='o')
    ax.set_title("Monthly Sales Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")
    ax.grid(True)

    st.pyplot(fig)

    # City chart
    st.subheader("🏙️ Sales by City")

    fig2, ax2 = plt.subplots()
    cities = sales_by_city.index
    values = sales_by_city.values

    colors = ["#6366F1", "#22C55E", "#F59E0B", "#EF4444", "#14B8A6"]

    ax2.bar(cities, values, color=colors[:len(cities)])
    ax2.set_title("Sales by City")
    ax2.set_xlabel("City")
    ax2.set_ylabel("Sales")

    plt.xticks(rotation=45)

    st.pyplot(fig2)

    # Download
    st.success("✅ Report ready!")

    with open(report_path, "rb") as file:
        st.download_button(
            label="📥 Download Excel Report",
            data=file,
            file_name="report.xlsx"
        )