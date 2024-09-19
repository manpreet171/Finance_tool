import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_future_value(present_value, rate, time):
    return present_value * (1 + rate) ** time

def format_currency(amount):
    return f"₹{amount:,.2f}"

def main():
    st.set_page_config(layout="wide", page_title="INR Finance Manager", page_icon="💰")
    
    # Custom CSS for financial theme
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f8ff;
    }
    .st-bb {
        background-color: #e6f2ff;
    }
    .stMetricValue {
        color: #006400;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("💰 Finance Planning tool - Crafted by Manpreet 📊")

    # Input section
    st.header("📝 Income Input")
    col1, col2 = st.columns(2)
    with col1:
        salary = st.number_input("Monthly Job Salary (in hand)", min_value=0.0, step=1000.0, format="%.2f")
    with col2:
        freelance = st.number_input("Freelancing Earnings", min_value=0.0, step=1000.0, format="%.2f")

    # Calculations
    salary_expenses = salary * 0.5
    salary_desires = salary * 0.2
    salary_investments = salary * 0.3

    freelance_expenses = freelance * 0.2
    freelance_desires = freelance * 0.3
    freelance_savings = freelance * 0.5

    total_expenses = salary_expenses + freelance_expenses
    total_desires = salary_desires + freelance_desires
    total_investments = salary_investments + freelance_savings

    # Display results
    st.header("💼 Money Allocation")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Expenses", value=format_currency(total_expenses), delta=f"{total_expenses/salary*100:.1f}%" if salary > 0 else None)
    with col2:
        st.metric(label="Total Desires", value=format_currency(total_desires), delta=f"{total_desires/salary*100:.1f}%" if salary > 0 else None)
    with col3:
        st.metric(label="Total Investments/Savings", value=format_currency(total_investments), delta=f"{total_investments/salary*100:.1f}%" if salary > 0 else None)

    # Detailed breakdown
    with st.expander("See detailed breakdown 📊"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Expenses 💸")
            st.write(f"Salary: {format_currency(salary_expenses)}")
            st.write(f"Freelance: {format_currency(freelance_expenses)}")
        with col2:
            st.subheader("Desires 🛍️")
            st.write(f"Salary: {format_currency(salary_desires)}")
            st.write(f"Freelance: {format_currency(freelance_desires)}")
        with col3:
            st.subheader("Investments/Savings 💰")
            st.write(f"Salary: {format_currency(salary_investments)}")
            st.write(f"Freelance: {format_currency(freelance_savings)}")

    # Visualization
    st.header("📈 Visualization")
    
    # Check if there's any income to visualize
    if salary > 0 or freelance > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for overall allocation
            fig, ax = plt.subplots()
            labels = ['Expenses', 'Desires', 'Investments/Savings']
            sizes = [total_expenses, total_desires, total_investments]
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            st.subheader('Overall Allocation 🍰')
            st.pyplot(fig)

        with col2:
            # Bar chart for salary vs freelance allocation
            fig, ax = plt.subplots()
            categories = ['Expenses', 'Desires', 'Investments/Savings']
            salary_data = [salary_expenses, salary_desires, salary_investments]
            freelance_data = [freelance_expenses, freelance_desires, freelance_savings]

            x = range(len(categories))
            width = 0.35

            ax.bar([i - width/2 for i in x], salary_data, width, label='Salary', color='#66b3ff')
            ax.bar([i + width/2 for i in x], freelance_data, width, label='Freelance', color='#ff9999')

            ax.set_ylabel('Amount (₹)')
            ax.set_title('Salary vs Freelance Allocation')
            ax.set_xticks(x)
            ax.set_xticklabels(categories)
            ax.legend()

            st.subheader('Salary vs Freelance Allocation 📊')
            st.pyplot(fig)
    else:
        st.info("🔎 Please enter some income to visualize the allocation.")

    # Investment growth calculation
    st.header("📈 Investment Growth Projection")
    rate = st.slider("Annual Return Rate", min_value=0.0, max_value=0.20, value=0.12, step=0.01, format="%.2f")
    years = st.slider("Investment Period (Years)", min_value=1, max_value=30, value=10)
    
    if total_investments > 0:
        future_value = calculate_future_value(total_investments * 12, rate, years)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Monthly Investment 💰", value=format_currency(total_investments))
            st.metric(label="Future Value 🔮", value=format_currency(future_value), delta=f"{(future_value/(total_investments*12*years)-1)*100:.1f}%")

        with col2:
            # Investment growth visualization
            years_range = range(1, years + 1)
            values = [calculate_future_value(total_investments * 12, rate, year) for year in years_range]

            fig, ax = plt.subplots()
            ax.plot(years_range, values, marker='o', color='#006400')
            ax.set_xlabel('Years')
            ax.set_ylabel('Investment Value (₹)')
            ax.set_title(f'Investment Growth Over {years} Years')
            ax.grid(True)

            # Format y-axis labels to display in lakhs or crores
            def format_func(value, tick_number):
                if value >= 10000000:  # 1 crore
                    return f'{value/10000000:.1f}Cr'
                elif value >= 100000:  # 1 lakh
                    return f'{value/100000:.1f}L'
                else:
                    return f'{value:.0f}'

            ax.yaxis.set_major_formatter(plt.FuncFormatter(format_func))

            st.pyplot(fig)
    else:
        st.info("💡 Please enter some income to calculate and visualize investment growth.")

    # Add a fun element
    if st.button("🎉 Celebrate Financial Planning!"):
        st.balloons()
        st.success("Great job on planning your finances! Keep it up! 🚀")

if __name__ == "__main__":
    main()