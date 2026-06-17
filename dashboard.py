
import streamlit as st
import mysql.connector
import pandas as pd
from mcp_connection import get_ai_answer
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.title("AI Sales Dashboard")

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="salesdb"
)

# ---------------- Revenue KPI ----------------

revenue_query = """
SELECT SUM(p.price * s.quantity) AS revenue
FROM sales s
JOIN products p
ON s.product_id = p.product_id
"""

revenue_df = pd.read_sql(revenue_query, conn)

# ---------------- Customer KPI ----------------

customer_query = """
SELECT COUNT(*) AS customers
FROM customers
"""

customer_df = pd.read_sql(customer_query, conn)

# ---------------- Product KPI ----------------

product_query = """
SELECT COUNT(*) AS products
FROM products
"""

product_df = pd.read_sql(product_query, conn)

# ---------------- KPI Cards ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{int(revenue_df['revenue'][0])}"
    )

with col2:
    st.metric(
        "Total Customers",
        int(customer_df['customers'][0])
    )

with col3:
    st.metric(
        "Total Products",
        int(product_df['products'][0])
    )

# ---------------- Sales Analysis ----------------

sales_query = """
SELECT
p.product_name,
SUM(s.quantity) AS total_quantity
FROM sales s
JOIN products p
ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_quantity DESC
"""

sales_df = pd.read_sql(sales_query, conn)

# ---------------- Chart ----------------

st.subheader("Top Selling Products Chart")

st.bar_chart(
    sales_df.set_index("product_name")
)

# ---------------- Table ----------------

st.subheader("Top Selling Products Data")

st.dataframe(sales_df)

# ---------------- Product Filter ----------------

st.subheader("Product Filter")

selected_product = st.selectbox(
    "Select Product",
    sales_df["product_name"]
)

filtered_data = sales_df[
    sales_df["product_name"] == selected_product
]

st.write(filtered_data)

# ---------------- AI Business Insights ----------------

st.subheader("AI Business Insights")

top_product = sales_df.iloc[0]["product_name"]
top_quantity = sales_df.iloc[0]["total_quantity"]

st.success(
    f"🔥 Top Selling Product: {top_product} ({int(top_quantity)} units sold)"
)

total_revenue = int(revenue_df['revenue'][0])

st.info(
    f"💰 Total Business Revenue: ₹{total_revenue}"
)

# ---------------- PDF Report Generator ----------------

def generate_pdf():

    file_name = "sales_report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Sales Analytics Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Total Revenue: ₹{total_revenue}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Top Product: {top_product}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Total Customers: {int(customer_df['customers'][0])}",
            styles["Normal"]
        )
    )

    doc.build(content)

    return file_name

pdf_file = generate_pdf()

with open(pdf_file, "rb") as file:

    st.download_button(
        label="Download Sales Report PDF",
        data=file,
        file_name="AI_Sales_Report.pdf",
        mime="application/pdf"
    )

# ---------------- Monthly Revenue Trend ----------------

monthly_query = """
SELECT
DATE_FORMAT(s.sale_date, '%Y-%m') AS month,
SUM(p.price * s.quantity) AS revenue
FROM sales s
JOIN products p
ON s.product_id = p.product_id
GROUP BY month
ORDER BY month
"""

monthly_df = pd.read_sql(monthly_query, conn)

st.subheader("Monthly Revenue Trend")

st.line_chart(
    monthly_df.set_index("month")
)

# ---------------- AI Data Analyst ----------------

st.subheader("🤖 Ask AI Data Analyst")

question = st.text_input(
    "Ask your question:",
    placeholder="Example: Which product sold highest?",
    key="ai_question"
)

if question:

    answer = get_ai_answer(question)

    st.success(answer)

# ---------------- Close Connection ----------------

conn.close()

