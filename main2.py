# main.py: Data Engineer Assignment for Skygeni
# Purpose: Analyze CSV files to answer four questions and generate visualizations
# Author: [Your Name]
# Date: April 19, 2025

import csv
import os
from statistics import mean, median
import logging
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Set up logging to track process and errors
logging.basicConfig(
    filename='results/assignment.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
VIS_DIR = os.path.join(BASE_DIR, 'visualizations')
RES_DIR = os.path.join(BASE_DIR, 'results')

# Ensure directories exist
os.makedirs(VIS_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

def read_csv(file_path):
    """Read a CSV file and return a list of dictionaries."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [dict((k.strip(), v.strip()) for k, v in row.items()) for row in reader]
        logging.info(f"Successfully read {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        raise

def parse_date(date_str):
    """Parse date string into datetime object with flexible formats and whitespace handling."""
    if not date_str or not isinstance(date_str, str):
        logging.warning(f"Invalid date string: {date_str}")
        return None
    date_str = date_str.strip()
    for fmt in ('%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%Y-%m-%d', '%m/%d/%y', '%Y/%m/%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    logging.warning(f"Unable to parse date (tried all formats): {date_str}")
    return None

def count_finance_clients(clients_data):
    """Count clients in Finance Lending and Block Chain industries."""
    target_industries = {'finance lending', 'block chain'}
    count = len({client['client_id'] for client in clients_data if client['industry'].lower() in target_industries})
    logging.info(f"Finance Lending and Block Chain clients: {count}")
    return count

def highest_renewal_rate(clients_data, subscriptions_data):
    """Find industry with highest renewal rate."""
    client_industry = {client['client_id']: client['industry'].lower() for client in clients_data}
    industry_renewals = {}
    industry_totals = {}
    
    for sub in subscriptions_data:
        client_id = sub['client_id']
        if client_id in client_industry:
            industry = client_industry[client_id]
            renew_status = sub['renewed'].lower()
            renew_count = 1 if renew_status in ('true', '1', 'yes') else 0
            industry_renewals[industry] = industry_renewals.get(industry, 0) + renew_count
            industry_totals[industry] = industry_totals.get(industry, 0) + 1
    
    renewal_rates = {
        industry: (industry_renewals.get(industry, 0) / total) * 100
        for industry, total in industry_totals.items() if total > 0
    }
    
    if not renewal_rates:
        logging.warning("No renewal data found")
        return "Unknown", 0.0
    
    max_industry = max(renewal_rates, key=renewal_rates.get)
    max_rate = renewal_rates[max_industry]
    
    plt.figure(figsize=(10, 6))
    plt.bar(renewal_rates.keys(), renewal_rates.values())
    plt.title('Renewal Rates by Industry')
    plt.xlabel('Industry')
    plt.ylabel('Renewal Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, 'renewal_rates.png'))
    plt.close()
    
    logging.info(f"Highest renewal rate: {max_industry} ({max_rate:.2f}%)")
    return max_industry, max_rate

def average_inflation_rate(subscriptions_data, inflation_data):
    """Calculate average inflation rate at renewal."""
    # Deduplicate renewal dates by (client_id, end_date) pair
    renewal_set = {(sub['client_id'], sub['end_date']) for sub in subscriptions_data if sub['renewed'].lower() in ('true', '1', 'yes')}
    renewal_dates = [parse_date(sub['end_date']) for sub in subscriptions_data if (sub['client_id'], sub['end_date']) in renewal_set and parse_date(sub['end_date'])]
    
    inflation_data = [row for row in inflation_data if parse_date(row['start_date']) and parse_date(row['end_date'])]
    if not inflation_data or not renewal_dates:
        logging.warning("No valid dates for inflation or renewals")
        return 0.0
    
    inflation_rates = []
    for r_date in renewal_dates:
        if r_date:
            matched = False
            for inf in inflation_data:
                start_dt = parse_date(inf['start_date'])
                end_dt = parse_date(inf['end_date'])
                if start_dt and end_dt and start_dt <= r_date <= end_dt:
                    try:
                        rate = float(inf['inflation_rate'])
                        inflation_rates.append(rate)
                        logging.info(f"Matched renewal {r_date.strftime('%Y-%m-%d')} to inflation {start_dt.strftime('%Y-%m-%d')} - {end_dt.strftime('%Y-%m-%d')} with rate {rate}%")
                        matched = True
                    except ValueError:
                        logging.warning(f"Invalid inflation rate for period {inf['start_date']} to {inf['end_date']}")
                    break
            if not matched:
                closest_start = min([parse_date(inf['start_date']) for inf in inflation_data if parse_date(inf['start_date'])],
                                  key=lambda x: abs(x - r_date) if x else float('inf'))
                for inf in inflation_data:
                    if parse_date(inf['start_date']) == closest_start:
                        try:
                            rate = float(inf['inflation_rate'])
                            inflation_rates.append(rate)
                            logging.info(f"Fallback match for renewal {r_date.strftime('%Y-%m-%d')} to closest {closest_start.strftime('%Y-%m-%d')} with rate {rate}%")
                        except ValueError:
                            logging.warning(f"Invalid inflation rate for closest date {inf['start_date']}")
                        break
    
    if not inflation_rates:
        logging.warning("No matching inflation rates found")
        return 0.0
    
    avg_inflation = mean(inflation_rates)
    logging.info(f"Inflation rates used: {inflation_rates}")
    
    plt.figure(figsize=(8, 5))
    plt.hist(inflation_rates, bins=5, edgecolor='black')
    plt.title('Distribution of Inflation Rates at Renewal')
    plt.xlabel('Inflation Rate (%)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, 'inflation_rates.png'))
    plt.close()
    
    logging.info(f"Average inflation rate: {avg_inflation:.2f}%")
    return avg_inflation

def median_payment_amount(payments_data):
    """Calculate median amount paid each year for all payment methods."""
    try:
        # Group amounts and payment methods by year
        amounts_by_year = defaultdict(list)
        payment_methods_by_year = defaultdict(list)
        for row in payments_data:
            date_str = row.get('payment_date', '').strip()
            amount = row.get('amount_paid', '').replace(',', '').strip()
            payment_method = row.get('payment_method', 'Unknown').strip()
            if date_str and amount and amount.replace('.', '', 1).isdigit():
                date = parse_date(date_str)
                if date:
                    year = date.year
                    amount_val = float(amount)
                    amounts_by_year[year].append(amount_val)
                    payment_methods_by_year[year].append(payment_method)
            else:
                if not (amount and amount.replace('.', '', 1).isdigit()):
                    logging.warning(f"Invalid amount skipped: {amount}")
                if date_str and parse_date(date_str) is None:
                    logging.warning(f"Invalid date format skipped for amount {amount}: {date_str}")
        
        # Calculate median for each year
        yearly_medians = {}
        for year, amounts in amounts_by_year.items():
            if amounts:
                median_val = median([x for x in amounts if x > 0])
                yearly_medians[year] = median_val
                unique_methods = set(payment_methods_by_year[year])
                logging.info(f"Median amount for year {year}: ${median_val:.2f} (based on {len(amounts)} amounts) with payment methods: {unique_methods}")
        
        logging.info(f"Processed medians for years: {yearly_medians}")
    except Exception as e:
        logging.error(f"Error processing payment amounts: {e}")
        return {}
    
    if not yearly_medians:
        logging.warning("No valid payment amounts found per year")
        return {}
    
    # Format result as newline-separated list for better readability
    median_result = "\n".join(f"{year}: ${median:.2f}" for year, median in sorted(yearly_medians.items()))
    
    # Create a boxplot for all amounts across years
    all_amounts = [amount for amounts in amounts_by_year.values() for amount in amounts if amount > 0]
    plt.figure(figsize=(8, 5))
    plt.boxplot(all_amounts)
    plt.title('Distribution of Payment Amounts Across Years')
    plt.ylabel('Amount ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(VIS_DIR, 'payment_amounts.png'))
    plt.close()
    
    logging.info(f"Median amounts per year: {median_result}")
    return median_result

def save_results(results):
    """Save results to a text file."""
    result_file = os.path.join(RES_DIR, 'results.txt')
    with open(result_file, 'w') as f:
        for key, value in results.items():
            f.write(f"{key}: {value}\n")
    logging.info(f"Results saved to {result_file}")

def main():
    """Main function to orchestrate the analysis."""
    logging.info("Starting analysis")
    
    try:
        clients_data = read_csv(os.path.join(DATA_DIR, 'industry_client_details.csv'))
        subscriptions_data = read_csv(os.path.join(DATA_DIR, 'subscription_information.csv'))
        inflation_data = read_csv(os.path.join(DATA_DIR, 'financial_information.csv'))
        payments_data = read_csv(os.path.join(DATA_DIR, 'payment_information.csv'))
        
        finance_clients = count_finance_clients(clients_data)
        top_industry, top_rate = highest_renewal_rate(clients_data, subscriptions_data)
        avg_inflation = average_inflation_rate(subscriptions_data, inflation_data)
        med_payment = median_payment_amount(payments_data)
        
        results = {
            "Number of Finance Lending and Block Chain Clients": finance_clients,
            "Industry with Highest Renewal Rate": f"{top_industry} ({top_rate:.2f}%)",
            "Average Inflation Rate at Renewal": f"{avg_inflation:.2f}%",
            "Median Amount Paid Each Year for All Payment Methods": med_payment
        }
        
        save_results(results)
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
