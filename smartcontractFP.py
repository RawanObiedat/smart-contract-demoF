import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page title
st.title("🎓 Tuition Installment Planner")

# --- Inputs from user ---
number_of_hours = st.number_input("Enter number of credit hours:", min_value=1, value=15)
funding_type = st.selectbox("Select funding type:", [
    "Royal Grant", "Teachers Grant", "Staff Grant",
    "Loans & Grants", "Regular", "Parallel"
])
payment_option = st.radio("Select payment type:", ["Full", "Partial"])

# Only show partial payment input if selected
if payment_option == "Partial":
    amount_paid_by_student = st.number_input("Enter amount you want to pay now (JOD):", min_value=0.0, value=400.0)
else:
    amount_paid_by_student = 0.0  # ignored in case of Full payment

# --- Logic processing ---
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

# Effective payment based on payment type
effective_payment = total_amount if payment_option == "Full" else amount_paid_by_student

# Prepare installment plan
installments_count = 3
installment_value = round(total_amount / installments_count, 2)
today = datetime.today()
due_dates = [today + timedelta(days=30 * i) for i in range(installments_count)]
reminder_dates = [d - timedelta(days=14) for d in due_dates]

# Allocate paid amount
payments = []
statuses = []
remaining_payment = effective_payment
running_balance = total_amount
remaining_after_payments = []

for i in range(installments_count):
    if remaining_payment >= installment_value:
        paid = installment_value
        status = "Paid"
    elif 0 < remaining_payment < installment_value:
        paid = remaining_payment
        status = "Partial"
    else:
        paid = 0
        status = "Pending"

    payments.append(round(paid, 2))
    statuses.append(status)

    running_balance -= paid
    remaining_after_payments.append(round(running_balance, 2))
    remaining_payment -= paid

# --- Display summary ---
st.subheader("🧾 Payment Summary")
st.write("**Funding Type:**", funding_type)
st.write("**Credit Hour Price (JOD):**", credit_hour_price)
st.write("**Total Credit Hours:**", number_of_hours)
st.write("**University Fixed Fee (JOD):**", university_fixed_fee)
st.write("**Total Tuition Fee (JOD):**", total_amount)
st.write("**Payment Type:**", payment_option)
if payment_option == "Partial":
    st.write("**Amount Paid by Student (JOD):**", amount_paid_by_student)

# --- Show Installment Table ---
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
