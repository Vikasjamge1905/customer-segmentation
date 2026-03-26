"""
Sample data generator for demonstration and testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_retail_data(n_customers=500, n_transactions=5000, seed=42):
    """
    Generate realistic sample retail transaction data.
    
    Args:
        n_customers: Number of unique customers
        n_transactions: Number of transactions
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with transaction data
    """
    np.random.seed(seed)
    
    # Generate dates
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Different customer behaviors
    customer_ids = np.arange(1, n_customers + 1)
    
    # Assign purchase frequency distribution to customers
    # Some customers are frequent, some occasional
    purchase_propensity = np.random.beta(2, 5, n_customers)
    
    transactions = []
    
    for _ in range(n_transactions):
        # Select customer with weighted probability
        customer_id = np.random.choice(customer_ids, p=purchase_propensity / purchase_propensity.sum())
        
        # Generate transaction details
        invoice_id = f'INV{len(transactions):06d}'
        invoice_date = np.random.choice(dates)
        
        # Quantity varies by customer type
        quantity = max(1, int(np.random.normal(5, 3)))
        
        # Price varies
        unit_price = round(np.random.uniform(5, 100), 2)
        
        transactions.append({
            'InvoiceID': invoice_id,
            'CustomerID': customer_id,
            'InvoiceDate': invoice_date,
            'Quantity': quantity,
            'UnitPrice': unit_price
        })
    
    df = pd.DataFrame(transactions)
    return df.sort_values('InvoiceDate').reset_index(drop=True)


if __name__ == "__main__":
    # Generate and save sample data
    df = generate_sample_retail_data()
    df.to_csv('data/sample_retail_data.csv', index=False)
    print(f"Generated sample data: {len(df)} transactions from {df['CustomerID'].nunique()} customers")
    print(f"Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
