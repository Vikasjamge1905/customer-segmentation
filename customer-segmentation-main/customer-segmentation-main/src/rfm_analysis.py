"""
RFM Analysis Module
Handles Recency, Frequency, and Monetary value calculations for customer segmentation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Dict


class RFMAnalysis:
    """Perform RFM analysis on transaction data."""
    
    def __init__(self, df: pd.DataFrame, reference_date: datetime = None):
        """
        Initialize RFM analysis.
        
        Args:
            df: Transaction dataframe with CustomerID, InvoiceDate, Quantity, UnitPrice
            reference_date: Date to calculate recency from (default: max date in data)
        """
        self.df = df.copy()
        self.reference_date = reference_date or self.df['InvoiceDate'].max()
        self.rfm_df = None
        
    def calculate_rfm(self) -> pd.DataFrame:
        """
        Calculate RFM metrics for each customer.
        
        Returns:
            DataFrame with CustomerID and RFM metrics
        """
        # Calculate Recency: Days since last purchase
        last_purchase = self.df.groupby('CustomerID')['InvoiceDate'].max()
        recency = (self.reference_date - last_purchase).dt.days.reset_index()
        recency.columns = ['CustomerID', 'Recency']
        
        # Calculate Frequency: Number of purchases
        frequency = self.df.groupby('CustomerID')['InvoiceID'].count().reset_index()
        frequency.columns = ['CustomerID', 'Frequency']
        
        # Calculate Monetary: Total amount spent
        self.df['TotalAmount'] = self.df['Quantity'] * self.df['UnitPrice']
        monetary = self.df.groupby('CustomerID')['TotalAmount'].sum().reset_index()
        monetary.columns = ['CustomerID', 'Monetary']
        
        # Merge all metrics
        self.rfm_df = recency.merge(frequency, on='CustomerID').merge(monetary, on='CustomerID')
        
        # Round monetary values
        self.rfm_df['Monetary'] = self.rfm_df['Monetary'].round(2)
        
        return self.rfm_df
    
    def assign_rfm_scores(self, q: int = 4) -> pd.DataFrame:
        """
        Assign RFM scores using quantile-based ranking.
        
        Args:
            q: Number of quantiles (default: 4 for quartiles)
            
        Returns:
            DataFrame with R_Score, F_Score, M_Score columns
        """
        if self.rfm_df is None:
            self.calculate_rfm()
        
        rfm_copy = self.rfm_df.copy()
        
        # Recency: Lower is better (more recent), so reverse ranking
        rfm_copy['R_Score'] = pd.qcut(rfm_copy['Recency'], q=q, labels=False, duplicates='drop') + 1
        rfm_copy['R_Score'] = q + 1 - rfm_copy['R_Score']  # Reverse so higher = more recent
        
        # Frequency: Higher is better
        rfm_copy['F_Score'] = pd.qcut(rfm_copy['Frequency'], q=q, labels=False, duplicates='drop') + 1
        
        # Monetary: Higher is better
        rfm_copy['M_Score'] = pd.qcut(rfm_copy['Monetary'], q=q, labels=False, duplicates='drop') + 1
        
        # Combined RFM Score (concatenation)
        rfm_copy['RFM_Score'] = (rfm_copy['R_Score'].astype(str) + 
                                 rfm_copy['F_Score'].astype(str) + 
                                 rfm_copy['M_Score'].astype(str))
        
        return rfm_copy
    
    def get_statistics(self) -> Dict:
        """Get RFM statistics."""
        if self.rfm_df is None:
            self.calculate_rfm()
        
        stats = {
            'total_customers': len(self.rfm_df),
            'recency_mean': self.rfm_df['Recency'].mean(),
            'recency_median': self.rfm_df['Recency'].median(),
            'frequency_mean': self.rfm_df['Frequency'].mean(),
            'frequency_median': self.rfm_df['Frequency'].median(),
            'monetary_mean': self.rfm_df['Monetary'].mean(),
            'monetary_median': self.rfm_df['Monetary'].median(),
            'total_revenue': self.rfm_df['Monetary'].sum()
        }
        return stats
    
    def segment_by_percentile(self) -> pd.DataFrame:
        """
        Create customer segments based on RFM percentiles.
        
        Returns:
            DataFrame with segment labels
        """
        if self.rfm_df is None:
            self.calculate_rfm()
        
        rfm_copy = self.rfm_df.copy()
        
        # Define percentiles for segmentation
        r_median = rfm_copy['Recency'].median()
        f_median = rfm_copy['Frequency'].median()
        m_median = rfm_copy['Monetary'].median()
        
        def assign_segment(row):
            r = row['Recency'] <= r_median
            f = row['Frequency'] >= f_median
            m = row['Monetary'] >= m_median
            
            if r and f and m:
                return 'Champions'
            elif (not r) and f and m:
                return 'Loyal Customers'
            elif r and (not f) and m:
                return 'Big Spenders'
            elif r and f and (not m):
                return 'At Risk'
            elif (not r) and (not f) and m:
                return 'Potential Loyalists'
            elif (not r) and f and (not m):
                return 'Need Attention'
            elif r and (not f) and (not m):
                return 'New Customers'
            else:
                return 'Lost'
        
        rfm_copy['Segment'] = rfm_copy.apply(assign_segment, axis=1)
        
        return rfm_copy
