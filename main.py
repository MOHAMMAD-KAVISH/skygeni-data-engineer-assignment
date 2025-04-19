import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- Load Data ----------------------
# Update with the full path where your files are located
financial = pd.read_csv('D:/skygeni-data-engineer-assignment/data/financial_information.csv')
industry = pd.read_csv('D:/skygeni-data-engineer-assignment/data/industry_client_details.csv')
payments = pd.read_csv('D:/skygeni-data-engineer-assignment/data/payment_information.csv')
subscriptions = pd.read_csv('D:/skygeni-data-engineer-assignment/data/subscription_information.csv')

# ---------------------- Q1: Finance Lending & Blockchain Clients ----------------------
finance_blockchain = industry[industry['industry'].isin(['Finance Lending', 'Block Chain'])]
q1_count = finance_blockchain['client_id'].nunique()
print("Q1. Number of Finance Lending & Blockchain clients:", q1_count)

# ---------------------- Q2: Industry with Highest Renewal Rate ----------------------
# Merge both files on client_id
sub_industry = pd.merge(subscriptions, industry, on='client_id')

# Total unique clients per industry
total_per_industry = sub_industry.groupby('industry')['client_id'].nunique()

# Renewed subscriptions
renewed = sub_industry[sub_industry['renewed'] == True].copy()

# Convert 'start_date' to datetime
renewed['start_date'] = pd.to_datetime(renewed['start_date'], errors='coerce')

# Extract year
renewed['year'] = renewed['start_date'].dt.year

# Renewed unique clients per industry
renewed_per_industry = renewed.groupby('industry')['client_id'].nunique()

# Renewal rate = (renewed clients / total clients) * 100
renewal_rate = (renewed_per_industry / total_per_industry) * 100

# Industry with highest renewal rate
top_industry = renewal_rate.idxmax()

print("Q2. Industry with highest renewal rate:", top_industry)
print(renewal_rate.sort_values(ascending=False))

# Optional: Visualization
renewal_rate.sort_values().plot(kind='barh', figsize=(8,5), title="Renewal Rate by Industry")
plt.xlabel("Renewal Rate (%)")
plt.tight_layout()
plt.savefig("renewal_rate_by_industry.png")
plt.close()

# ---------------------- Q3: Average Inflation Rate During Renewal ----------------------
# Convert dates to datetime format
renewed['start_date'] = pd.to_datetime(renewed['start_date'], errors='coerce')
financial['start_date'] = pd.to_datetime(financial['start_date'], errors='coerce')

# Extract year from both datasets
renewed['year'] = renewed['start_date'].dt.year
financial['year'] = financial['start_date'].dt.year

# Merge on 'year'
merged_inflation = pd.merge(renewed, financial[['year', 'inflation_rate']], on='year', how='left')

# Calculate average inflation rate
average_inflation = merged_inflation['inflation_rate'].mean()

print("Q3. Average inflation rate at time of renewal:", round(average_inflation, 2), "%")


# ---------------------- Q4: Median Amount Paid Each Year by Payment Method ----------------------
# Convert payment date to datetime and extract year
payments['payment_date'] = pd.to_datetime(payments['payment_date'], errors='coerce')
payments['year'] = payments['payment_date'].dt.year

# Group by year and payment method to calculate median amount paid
medians = payments.groupby(['year', 'payment_method'])['amount_paid'].median().reset_index()

# Display results
print("Q4. Median Amount Paid Each Year by Payment Method:\n", medians)

# Optional: Visualization - Pie chart for latest year
latest_year = payments['year'].max()
latest_data = medians[medians['year'] == latest_year]
plt.figure(figsize=(6,6))
plt.pie(latest_data['amount_paid'], labels=latest_data['payment_method'], autopct='%1.1f%%')
plt.title(f"Median Amount Paid by Payment Method in {latest_year}")
plt.tight_layout()
plt.savefig("median_amount_pie.png")
plt.close()


