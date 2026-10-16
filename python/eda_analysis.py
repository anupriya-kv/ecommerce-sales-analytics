import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\dataset\cleaned_data.csv'
)

# Show first 10 rows
print("\nFIRST 10 ROWS:")
print(df.head(10))

# Show column names
print("\nCOLUMN NAMES:")
print(df.columns)

# Show dataset shape
print("\nDATASET SHAPE:")
print(df.shape)

# Show missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Show data types
print("\nDATA TYPES:")
print(df.dtypes)

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=True)

# Create Year column
df['Year'] = df['InvoiceDate'].dt.year

# Create Month column
df['Month'] = df['InvoiceDate'].dt.month

# Create YearMonth column
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

# Display updated columns
print("\nUPDATED DATA:")
print(df[['InvoiceDate', 'Year', 'Month', 'YearMonth']].head())

print("\nUPDATED DATA TYPES:")
print(df.dtypes)

# Monthly Sales Trend
monthly_sales = df.groupby('YearMonth')['TotalPrice'].sum()

print("\nMONTHLY SALES TREND:")
print(monthly_sales)

import matplotlib.pyplot as plt

# Plot monthly sales trend
monthly_sales.plot(figsize=(12,6))

# Chart title and labels
plt.title('Monthly Sales Trend')
plt.xlabel('Year-Month')
plt.ylabel('Revenue')

# Rotate x-axis labels
plt.xticks(rotation=45)

plt.savefig(r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\screenshots\monthly_sales_trend.png')
# Show chart
plt.show()

# Top Selling Products Analysis
top_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)

print("\nTOP 10 PRODUCTS:")
print(top_products)

# Plot Top Products
top_products.plot(kind='bar', figsize=(12,6))

# Chart formatting
plt.title('Top 10 Selling Products')
plt.xlabel('Product')
plt.ylabel('Revenue')

# Rotate labels
plt.xticks(rotation=75, fontsize=8)
plt.tight_layout()

# Save chart
plt.savefig(r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\screenshots\graphs\top_products.png')

# Show chart
plt.show()

# Country-wise Sales Analysis
country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)

print("\nTOP 10 COUNTRIES BY SALES:")
print(country_sales)

# Plot Country-wise Sales
country_sales.plot(kind='bar', figsize=(12,6))

# Chart formatting
plt.title('Top 10 Countries by Sales')
plt.xlabel('Country')
plt.ylabel('Revenue')

# Rotate labels
plt.xticks(rotation=45, fontsize=9)

# Adjust layout
plt.tight_layout()

# Save chart
plt.savefig(r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\screenshots\graphs\top_countries.png')

# Show chart
plt.show()

# Top Customers Analysis
top_customers = df.groupby('Customer ID')['TotalPrice'].sum().sort_values(ascending=False).head(10)

print("\nTOP 10 CUSTOMERS:")
print(top_customers)

# Plot Top Customers
top_customers.plot(kind='bar', figsize=(12,6))

# Chart formatting
plt.title('Top 10 Customers by Revenue')
plt.xlabel('Customer ID')
plt.ylabel('Revenue')

# Rotate labels
plt.xticks(rotation=45, fontsize=9)

# Adjust layout
plt.tight_layout()

# Save chart
plt.savefig(r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\screenshots\graphs\top_customers.png')

# Show chart
plt.show()

# Customer Segmentation

customer_spending = df.groupby('Customer ID')['TotalPrice'].sum()

# Create segments
high_value = customer_spending[customer_spending > 10000]
medium_value = customer_spending[(customer_spending > 5000) & (customer_spending <= 10000)]
low_value = customer_spending[customer_spending <= 5000]

# Print counts
print("\nCUSTOMER SEGMENTATION:")

print(f"High Value Customers: {len(high_value)}")
print(f"Medium Value Customers: {len(medium_value)}")
print(f"Low Value Customers: {len(low_value)}")

# Customer Segmentation Chart

segments = ['High Value', 'Medium Value', 'Low Value']
counts = [len(high_value), len(medium_value), len(low_value)]

plt.figure(figsize=(8,5))

plt.bar(segments, counts)

plt.title('Customer Segmentation')
plt.xlabel('Customer Segment')
plt.ylabel('Number of Customers')

# Save chart
plt.savefig(r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\screenshots\graphs\customer_segmentation.png')

# Show chart
plt.show()

# -----------------------------
# COHORT ANALYSIS
# -----------------------------

# Create InvoiceMonth column
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')

# Create CohortMonth (first purchase month of customer)
df['CohortMonth'] = df.groupby('Customer ID')['InvoiceMonth'].transform('min')

# Display sample cohort data
print("\nCOHORT DATA SAMPLE:")
print(df[['Customer ID', 'InvoiceMonth', 'CohortMonth']].sample(10).to_string(index=False))

#---------------
#COHORT INDEX CALCULATION
#---------------
# Extract year and month from InvoiceMonth
invoice_year = df['InvoiceMonth'].dt.year
invoice_month = df['InvoiceMonth'].dt.month

# Extract year and month from CohortMonth
cohort_year = df['CohortMonth'].dt.year
cohort_month = df['CohortMonth'].dt.month

# Calculate Cohort Index
df['CohortIndex'] = (
    (invoice_year - cohort_year) * 12
    + (invoice_month - cohort_month)
    + 1
)

# Display sample cohort index data
print("\nCOHORT INDEX SAMPLE:")

print(
    df[
        ['Customer ID', 'InvoiceMonth', 'CohortMonth', 'CohortIndex']
    ].sample(10).to_string(index=False)
)

# Create customer Retention Matrix

cohort_data = df.groupby(
    ['CohortMonth', 'CohortIndex']
)['Customer ID'].nunique().reset_index()

# Create pivot table
retention_matrix = cohort_data.pivot(
    index='CohortMonth',
    columns='CohortIndex',
    values='Customer ID'
)

# Display retention matrix
print("\nRETENTION MATRIX:")
print(retention_matrix)

# Convert Retention Matrix to Percentage

retention_percentage = retention_matrix.divide(
    retention_matrix.iloc[:, 0],
    axis=0
)

# Convert to percentage
retention_percentage = retention_percentage.round(3) * 100

# Display retention percentage matrix
print("\nRETENTION PERCENTAGE MATRIX:")
print(retention_percentage)

#heatmap

import seaborn as sns

# Create Cohort Heatmap
plt.figure(figsize=(14,8))

sns.heatmap(
    retention_percentage,
    annot=True,
    fmt='.1f',
    cmap='Blues'
)

# Chart title
plt.title('Customer Retention Cohort Analysis')

# Axis labels
plt.xlabel('Cohort Index')
plt.ylabel('Cohort Month')

# Save heatmap
plt.savefig(
    r'C:\Users\Anupriya\Desktop\Ecommerce_Analytics_Project\screenshots\graphs\cohort_heatmap.png'
)

# Show chart
plt.show()
