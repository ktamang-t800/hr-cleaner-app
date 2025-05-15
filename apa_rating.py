import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.title("📊 APA Rating History Cleaner")

# User input for target calculation date
target_date = st.date_input("📅 Calculate 'Service Duration & Time in Grade' until:", value=datetime.today())

# File upload
uploaded_file = st.file_uploader("📁 Upload APA Rating Excel File", type="xlsx")

if uploaded_file is not None:
    try:
        # Read starting from row 5 (index 4)
        df = pd.read_excel(uploaded_file, header=4, engine="openpyxl")

        # Set full column headers (A–V)
        df.columns = [
            "First Level Unit Name",                  # A
            "First Level Unit Head of Unit",          # B
            "User/Employee ID",                       # C
            "Nationality",                            # D
            "Birth Date",                             # E
            "Age",                                     # F
            "Gender",                                  # G
            "Grade",                                   # H
            "Designation",                             # I
            "Department",                              # J
            "Division",                                # K
            "Reporting Manager",                       # L
            "Employment Details Hire Date",            # M
            "Yrs of Service as Staff",                 # N
            "Grade Entry Date",                        # O
            "Time in Grade",                           # P
            "Employment Details Last Date Worked",     # Q
            "Form Name",                               # R
            "2021",                                     # S
            "2022",                                     # T
            "2023",                                     # U
            "Blank"                                     # V
        ]

        # Drop the fully blank column (Column V)
        df.drop(columns=["Blank"], inplace=True)

        # Round Age to 1 decimal
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce").round(1)

        # Unmerge vertically: Fill down columns A & B
        df["First Level Unit Name"] = df["First Level Unit Name"].ffill()
        df["First Level Unit Head of Unit"] = df["First Level Unit Head of Unit"].ffill()

        # Convert Hire Date to datetime
        df["Employment Details Hire Date"] = pd.to_datetime(df["Employment Details Hire Date"], errors="coerce")

        # Duration calculator
        def calculate_duration(from_date):
            if pd.isnull(from_date):
                return ""
            delta = target_date - from_date.date()
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            return f"{years} Years {months} Months {days} Days"

        # Calculated columns
        df["Calculated Service Duration"] = df["Employment Details Hire Date"].apply(calculate_duration)
        df["Calculated Time in Grade"] = df["Time in Grade"]

        # Preview
        st.subheader("🔍 Cleaned Preview")
        st.dataframe(df.head())

        # Download button
        output = io.BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)

        st.download_button(
            label="📥 Download Cleaned Excel",
            data=output,
            file_name="APA_Rating_Cleaned.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
