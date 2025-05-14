import pandas as pd
import streamlit as st
import os
import io

st.title("HR Report Cleaner")

uploaded_file = st.file_uploader("Upload Excel file (Job Requisition Report)", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl", header=2)
        st.success("File uploaded successfully!")

        # Remove duplicate rows based on 'Application ID'
        df_cleaned = df.drop_duplicates(subset='Application ID')

        # Show preview
        st.subheader("Cleaned Data Preview")
        st.dataframe(df_cleaned.head())
        
# Convert the cleaned DataFrame to Excel format in memory
        output = io.BytesIO()
        df_cleaned.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

# Add download button
        st.download_button(
            label="📥 Download Cleaned Excel File",
            data=output,
            file_name="Job_Requisition_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
    except Exception as e:
        st.error(f"Error: {e}")
