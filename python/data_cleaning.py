import pandas as pd

# Load dataset
df = pd.read_csv(r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\dataset\online_retail_II.csv', encoding='ISO-8859-1')

# Display first 5 rows
print(df.head())

# Dataset information
print(df.info())

# Remove rows where CustomerID is missing
df = df.dropna(subset=['Customer ID'])

# Remove cancelled invoices
df = df[~df['Invoice'].astype(str).str.startswith('C')]

# Create TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['Price']

# Convert InvoiceDate column to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Save cleaned dataset
df.to_csv(r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\dataset\cleaned_data.csv', index=False)

print("Data cleaned successfully!")
