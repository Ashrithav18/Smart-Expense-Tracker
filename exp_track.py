import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE = "expenses.csv"

# Function to add expense
def add_expense(date, category, amount, description):
    new_data = pd.DataFrame([[date, category, amount, description]],
                            columns=["Date", "Category", "Amount", "Description"])
    
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    
    df.to_csv(FILE, index=False)

# Function to load expenses
def load_expenses():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# Function to suggest savings
def suggest_savings(df):
    if df.empty:
        return "No data available to suggest savings."
    
    summary = df.groupby("Category")["Amount"].sum()
    max_category = summary.idxmax()
    max_amount = summary.max()

    suggestion = (
        f"💡 You spent the most on *{max_category}* (₹{max_amount:.2f}).\n\n"
        f"👉 Try reducing expenses in this category by 20%. "
        f"This could save you around ₹{max_amount * 0.2:.2f} next month."
    )
    return suggestion

# Streamlit UI
st.title("💰 Smart Expense Tracker")

menu = ["Add Expense", "View Expenses", "Summary & Suggestions"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Expense":
    st.subheader("➕ Add New Expense")
    
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "current Bill","phone bill", "Other bill","Other"])
    amount = st.number_input("Amount", min_value=1.0, step=0.5)
    description = st.text_input("Description")
    
    if st.button("Save Expense"):
        add_expense(date, category, amount, description)
        st.success("✅ Expense added successfully!")

elif choice == "View Expenses":
    st.subheader("📋 All Expenses")
    df = load_expenses()
    st.dataframe(df)

elif choice == "Summary & Suggestions":
    st.subheader("📊 Expense Summary & Next Month Prediction")
    df = load_expenses()
    
    if not df.empty:
        summary = df.groupby("Category")["Amount"].sum()
        st.bar_chart(summary)

        total = df["Amount"].sum()
        avg_monthly = total  # assuming one month’s data

        st.write(f"💵 *Total spent this month:* ₹{total:.2f}")
        st.write(f"📈 *Estimated spend next month (same trend):* ₹{avg_monthly:.2f}")

        # Suggestions
        st.subheader("🔍 Smart Savings Suggestion")
        st.info(suggest_savings(df))
    else:
        st.info("No expenses recorded yet.")