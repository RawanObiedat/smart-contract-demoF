import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Page setup
st.set_page_config(page_title="Student Contract", layout="wide")

# --- Login ---
st.sidebar.title("🔐 Login")
student_name = st.sidebar.text_input("Student Name:")
password = st.sidebar.text_input("Password:", type="password")

if student_name and password:
    st.success(f"Welcome, {student_name}!")

    # --- Input Data ---
    st.header("📄 Contract Information")

    # Select number of credit hours
    number_of_hours = st.selectbox("Number of Credit Hours:", options=[3, 6, 9, 12, 15, 18, 21, 24], index=4)

    # Select funding type
    funding_type = st.selectbox("Funding Type:", [
        "Royal Grant", "Teachers Grant", "Staff Grant",
        "Loans & Grants", "Regular", "Parallel"
    ])

    # Select payment option
    payment_option = st.radio("Payment Type:", ["Full", "Partial"])

    # Input amount paid if partial payment
    if payment_option == "Partial":
        amount_paid_by_student = st.number_input("Amount Paid Now (JOD):", min_value=0.0, value=0.0)
    else:
        amount_paid_by_student = 0.0

    # --- Calculations ---
    funding_prices = {
        "Royal Grant": 45,
        "Teachers Grant": 40,
        "Staff Grant": 35,
        "Loans & Grants": 0,
        "Regular": 50,
        "Parallel": 60
    }
    credit_hour_price = funding_prices.get(funding_type, 50)

    hour_fees = credit_hour_price * number_of_hours
    university_fixed_fee = 60
    total_amount = hour_fees + university_fixed_fee

    # Gas fee covered by university
    gas_fee = 13.5

    # Effective payment amount based on payment type
    effective_payment = total_amount if payment_option == "Full" else amount_paid_by_student

    # --- Installment plan ---
    installments_count = 3
    installment_value = round(total_amount / installments_count, 2)
    today = datetime.today()
    due_dates = [today + timedelta(days=30 * i) for i in range(installments_count)]
    reminder_dates = [d - timedelta(days=14) for d in due_dates]

    # Allocate paid amount across installments
    payments = []
    statuses = []
    remaining_after_payments = []
    remaining_payment = effective_payment

    for i in range(installments_count):
        if remaining_payment >= installment_value:
            paid = installment_value
            status = "Paid"
            remaining = 0.0
        elif 0 < remaining_payment < installment_value:
            paid = remaining_payment
            status = "Partial"
            remaining = installment_value - paid
        else:
            paid = 0.0
            status = "Pending"
            remaining = installment_value

        payments.append(round(paid, 2))
        statuses.append(status)
        remaining_after_payments.append(round(remaining, 2))

        remaining_payment -= paid

    # --- Display information ---
    st.subheader("📊 Payment Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Funding Type", funding_type)
    col2.metric("Credit Hour Price (JOD)", credit_hour_price)
    col3.metric("Number of Credit Hours", number_of_hours)

    col4, col5, col6 = st.columns(3)
    col4.metric("Fixed Fee (JOD)", university_fixed_fee)
    col5.metric("Total Tuition Fee (JOD)", total_amount)
    col6.metric("Payment Type", payment_option)

    if payment_option == "Partial":
        st.info(f"💰 Amount Paid by Student: {amount_paid_by_student} JOD")

    # --- Installments Table ---
    st.subheader("📅 Installment Schedule")
    df = pd.DataFrame({
        "Installment #": [f"#{i+1}" for i in range(installments_count)],
        "Due Date": [d.strftime("%Y-%m-%d") for d in due_dates],
        "Reminder Date": [r.strftime("%Y-%m-%d") for r in reminder_dates],
        "Installment Amount (JOD)": [installment_value] * installments_count,
        "Paid Amount (JOD)": payments,
        "Remaining After Payment (JOD)": remaining_after_payments,
        "Status": statuses
    })
    st.dataframe(df)

    # --- Payment Confirmation ---
    if st.button("Confirm Payment"):
        st.success("✅ Payment has been confirmed successfully.")

    # --- Payment Distribution Chart ---
    st.subheader("📈 Payment Distribution")
    paid_total = sum(payments)
    remaining_total = total_amount - paid_total
    pie_chart_df = pd.DataFrame({
        "Category": ["Paid", "Remaining"],
        "Amount": [paid_total, remaining_total]
    })
    fig = px.pie(pie_chart_df, names="Category", values="Amount", title="Payment Status")
    st.plotly_chart(fig)

    # --- Info Sidebar ---
    st.sidebar.markdown("### ℹ️ Additional Information")
    st.sidebar.write(f"🧑‍🎓 Student Name: {student_name}")
    st.sidebar.write(f"📚 Number of Credit Hours: {number_of_hours}")
    st.sidebar.write(f"💳 Funding Type: {funding_type}")
    st.sidebar.write(f"💰 Total Tuition Fee: {total_amount} JOD")
    st.sidebar.write(f"💵 Amount Paid: {effective_payment} JOD")
    st.sidebar.write(f"📆 Today's Date: {today.strftime('%Y-%m-%d')}")

else:
    st.warning("Please enter your student name and password to continue.")
