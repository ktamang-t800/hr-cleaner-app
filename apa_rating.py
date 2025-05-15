import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.title("📊 APA Rating History Cleaner")

# User input for target calculation date
target_date = st.date_input("📅 Calculate durations until:", value=datetime.today())

# File upload
uploaded_file = st.file_uploader("📁 Upload APA Rating Excel File", type="xlsx")

if uploaded_file is not None:
    try:
        # Read starting from row 5 (index 4)
        df = pd.read_excel(uploaded_file, header=4, engine="openpyxl")

        # Set proper column headers (A to R)
        df.columns = [
            "First Level Unit Name", "First Level Unit Head of Unit", "User/Employee ID", "Nationality",
            "Birth Date", "Age", "Gender", "Grade", "Designation", "Department", "Division",
            "Reporting Manager", "Hire Date", "Yrs of Service as Staff", "Grade Entry Date",
            "Time in Grade", "Last Date Worked", "Form Name", "Blank1", "Blank2", "Blank3", "Blank4"
        ]

        # Drop fully blank column (assumed to be 'Blank1' = Column S)
        df.drop(columns=["Blank1"], inplace=True)

        # Round Age to 1 decimal
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce").round(1)

        # Unmerge vertically: Fill down columns A & B
        df["First Level Unit Name"] = df["First Level Unit Name"].ffill()
        df["First Level Unit Head of Unit"] = df["First Level Unit Head of Unit"].ffill()

        # Convert Hire Date and Grade Entry Date to datetime
        df["Hire Date"] = pd.to_datetime(df["Hire Date"], errors="coerce")
        df["Grade Entry Date"] = pd.to_datetime(df["Grade Entry Date"], errors="coerce")

        # Duration calculator
        def calculate_duration(from_date):
            if pd.isnull(from_date):
                return ""
            delta = target_date - from_date.date()  # Ensure correct type
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            return f"{years} Years {months} Months {days} Days"

        # Calculate service & time in grade
        df["Calculated Service Duration"] = df["Hire Date"].apply(calculate_duration)
        df["Calculated Time in Grade"] = df["Grade Entry Date"].apply(calculate_duration)

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
