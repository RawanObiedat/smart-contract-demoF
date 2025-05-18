import pandas as pd
from datetime import datetime, timedelta

# Input Data
number_of_hours = 15
funding_type = "Teachers Grant"  # Options: Royal Grant, Teachers Grant, Staff Grant, Loans & Grants, Regular, Parallel
payment_option = "Partial"       # Options: "Full" or "Partial"
amount_paid_by_student = 400     # Amount paid if "Partial", ignored if "Full"

# Determine credit hour price based on funding type
funding_prices = {
    "Royal Grant": 45,
    "Teachers Grant": 40,
    "Staff Grant": 35,
    "Loans & Grants": 0,
    "Regular": 50,
    "Parallel": 60
}
credit_hour_price = funding_prices.get(funding_type, 50)

# Calculate total fees
hour_fees = credit_hour_price * number_of_hours
university_fixed_fee = 60
total_amount = hour_fees + university_fixed_fee

# Gas fee covered by the university
gas_fee = 13.5
effective_payment = total_amount if payment_option == "Full" else amount_paid_by_student

# Prepare installment plan
installments_count = 3
installment_value = round(total_amount / installments_count, 2)
today = datetime.today()
due_dates = [today + timedelta(days=30 * i) for i in range(installments_count)]
reminder_dates = [date - timedelta(days=14) for date in due_dates]

# Allocate paid amount across installments
payments = []
statuses = []
remaining = total_amount
remaining_payment = effective_payment

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
    remaining_payment -= paid
    remaining -= paid

# Compute remaining balance after each installment
remaining_after_payments = []
running_balance = total_amount
for i in range(installments_count):
    running_balance -= payments[i]
    remaining_after_payments.append(round(running_balance, 2))

# Create the installment DataFrame
df = pd.DataFrame({
    "Installment #": [f"#{i+1}" for i in range(installments_count)],
    "Due Date": [d.strftime("%Y-%m-%d") for d in due_dates],
    "Reminder Date": [r.strftime("%Y-%m-%d") for r in reminder_dates],
    "Installment Amount (JOD)": [installment_value] * installments_count,
    "Paid Amount (JOD)": payments,
    "Remaining After Payment (JOD)": remaining_after_payments,
    "Status": statuses
})

# Display summary
print("🧾 Payment Summary:")
print("Funding Type:", funding_type)
print("Credit Hour Price (JOD):", credit_hour_price)
print("Total Credit Hours:", number_of_hours)
print("University Fixed Fee (JOD):", university_fixed_fee)
print("Total Tuition Fee (JOD):", total_amount)
print("Payment Type:", payment_option)
print("Amount Paid by Student (JOD):", effective_payment)

print("\n📅 Installment Schedule:\n")
print(df.to_string(index=False))
