import pandas as pd

# Load the Excel file and use row 3 as the header
df = pd.read_excel("/Users/ken/Documents/HR Automation/JobRequisitionReport-Component1.xlsx", engine="openpyxl", header=2)

# Remove duplicate rows based on 'Application ID'
df_cleaned = df.drop_duplicates(subset='Application ID')

# Save the cleaned file to your Desktop
df_cleaned.to_excel("/Users/ken/Desktop/Job Requisition Data.xlsx", index=False)

print("File saved to your Desktop as 'Job Requisition Data.xlsx'")
