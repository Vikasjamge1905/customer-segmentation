"""
Main Analysis Pipeline
Complete end-to-end customer segmentation workflow
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from datetime import datetime
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from rfm_analysis import RFMAnalysis
from clustering import ClusteringEngine
from visualization import Visualizer


class DataPreprocessor:
    """Handle data cleaning and preprocessing."""
    
    @staticmethod
    def clean_data(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
        """
        Clean retail transaction data.
        
        Args:
            df: Raw transaction dataframe
            verbose: Print cleaning steps
            
        Returns:
            Cleaned dataframe
        """
        print("=" * 60)
        print("DATA CLEANING PROCESS")
        print("=" * 60)
        
        original_rows = len(df)
        
        # Remove null CustomerID
        df = df.dropna(subset=['CustomerID'])
        if verbose:
            print(f"✓ Removed null CustomerID: {original_rows - len(df)} rows")
        
        original_rows = len(df)
        
        # Remove negative quantities (returns)
        df = df[df['Quantity'] > 0]
        if verbose:
            print(f"✓ Removed negative quantities: {original_rows - len(df)} rows")
        
        # Convert InvoiceDate to datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        df = df.dropna(subset=['InvoiceDate'])
        if verbose:
            print(f"✓ Converted InvoiceDate to datetime format")
        
        # Remove duplicates
        original_rows = len(df)
        df = df.drop_duplicates()
        if verbose:
            print(f"✓ Removed duplicates: {original_rows - len(df)} rows")
        
        print(f"Final cleaned dataset: {len(df)} rows, {len(df.columns)} columns\n")
        
        return df
    
    @staticmethod
    def load_sample_data() -> pd.DataFrame:
        """
        Load or create sample retail data for demonstration.
        
        Returns:
            Sample transaction dataframe
        """
        np.random.seed(42)
        
        n_transactions = 5000
        n_customers = 500
        
        dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
        
        data = {
            'InvoiceID': [f'INV{i:06d}' for i in range(n_transactions)],
            'CustomerID': np.random.choice(range(1, n_customers + 1), n_transactions),
            'InvoiceDate': np.random.choice(dates, n_transactions),
            'Quantity': np.random.randint(1, 20, n_transactions),
            'UnitPrice': np.random.uniform(5, 100, n_transactions).round(2)
        }
        
        df = pd.DataFrame(data)
        return df.sort_values('InvoiceDate').reset_index(drop=True)


class SegmentationPipeline:
    """Complete customer segmentation pipeline."""
    
    def __init__(self, data_path: str = None, use_sample: bool = True):
        """
        Initialize pipeline.
        
        Args:
            data_path: Path to CSV file (if None, uses sample data)
            use_sample: Use sample data generation
        """
        self.data_path = data_path
        self.use_sample = use_sample
        self.df = None
        self.rfm_df = None
        self.clustered_df = None
        self.segmented_df = None
        self.results = {}
        
    def load_data(self) -> pd.DataFrame:
        """Load and clean data."""
        print("LOADING DATA...")
        
        if self.use_sample or self.data_path is None:
            print("Using sample retail data...\n")
            self.df = DataPreprocessor.load_sample_data()
        else:
            print(f"Loading from {self.data_path}...\n")
            self.df = pd.read_csv(self.data_path)
        
        self.df = DataPreprocessor.clean_data(self.df)
        return self.df
    
    def perform_rfm_analysis(self) -> pd.DataFrame:
        """Perform RFM analysis."""
        print("=" * 60)
        print("RFM ANALYSIS")
        print("=" * 60)
        
        rfm_analyzer = RFMAnalysis(self.df)
        self.rfm_df = rfm_analyzer.calculate_rfm()
        
        stats = rfm_analyzer.get_statistics()
        
        print(f"Total Customers: {stats['total_customers']}")
        print(f"\nRecency Statistics:")
        print(f"  Mean: {stats['recency_mean']:.2f} days")
        print(f"  Median: {stats['recency_median']:.2f} days")
        print(f"\nFrequency Statistics:")
        print(f"  Mean: {stats['frequency_mean']:.2f} purchases")
        print(f"  Median: {stats['frequency_median']:.2f} purchases")
        print(f"\nMonetary Statistics:")
        print(f"  Mean: ${stats['monetary_mean']:.2f}")
        print(f"  Median: ${stats['monetary_median']:.2f}")
        print(f"  Total Revenue: ${stats['total_revenue']:.2f}\n")
        
        self.results['rfm_stats'] = stats
        
        return self.rfm_df
    
    def apply_clustering(self, n_clusters: int = 4, algorithm: str = 'kmeans') -> pd.DataFrame:
        """
        Apply clustering algorithm.
        
        Args:
            n_clusters: Number of clusters
            algorithm: 'kmeans' or 'dbscan'
            
        Returns:
            Clustered dataframe
        """
        print("=" * 60)
        print(f"CLUSTERING - {algorithm.upper()}")
        print("=" * 60)
        
        clusterer = ClusteringEngine(self.rfm_df)
        
        if algorithm.lower() == 'kmeans':
            # Find optimal k first
            print("Finding optimal number of clusters...")
            optimization_results = clusterer.find_optimal_clusters(max_k=10)
            
            print(f"\nCluster Optimization Results:")
            for k, inertia, silhouette in zip(
                optimization_results['k_range'], 
                optimization_results['inertia'], 
                optimization_results['silhouette']
            ):
                print(f"  k={k}: Inertia={inertia:.2f}, Silhouette={silhouette:.4f}")
            
            self.results['optimization'] = optimization_results
            
            # Apply K-Means with specified k
            print(f"\nApplying K-Means with k={n_clusters}...")
            self.clustered_df = clusterer.apply_kmeans(n_clusters)
            
        elif algorithm.lower() == 'dbscan':
            print("Applying DBSCAN...")
            self.clustered_df = clusterer.apply_dbscan(eps=0.8, min_samples=5)
        
        # Get evaluation metrics
        evaluation = clusterer.get_evaluation_metrics()
        cluster_profiles = clusterer.get_cluster_profiles(self.clustered_df)
        
        print(f"\nClustering Evaluation Metrics:")
        print(f"  Number of Clusters: {evaluation['n_clusters']}")
        if evaluation['silhouette_score'] is not None:
            print(f"  Silhouette Score: {evaluation['silhouette_score']:.4f}")
        if evaluation['davies_bouldin_score'] is not None:
            print(f"  Davies-Bouldin Score: {evaluation['davies_bouldin_score']:.4f}")
        if evaluation['calinski_harabasz_score'] is not None:
            print(f"  Calinski-Harabasz Score: {evaluation['calinski_harabasz_score']:.4f}")
        if evaluation['n_noise_points'] > 0:
            print(f"  Noise Points: {evaluation['n_noise_points']}")
        
        print("\nCluster Profiles:")
        print(cluster_profiles)
        
        self.results['evaluation'] = evaluation
        self.results['cluster_profiles'] = cluster_profiles.to_dict()
        
        # Apply PCA for visualization
        print("\nApplying PCA for visualization...")
        pca_data, variance = clusterer.apply_pca(n_components=2)
        print(f"Explained Variance: {variance}")
        
        self.results['pca_data'] = pca_data
        self.results['pca_variance'] = variance
        self.results['clusterer'] = clusterer
        
        return self.clustered_df
    
    def interpret_segments(self) -> pd.DataFrame:
        """
        Interpret clusters as business segments.
        
        Returns:
            Dataframe with segment interpretations
        """
        print("\n" + "=" * 60)
        print("BUSINESS INTERPRETATION")
        print("=" * 60)
        
        cluster_profiles = pd.DataFrame(self.results['cluster_profiles'])
        
        def interpret_cluster(cluster_id):
            """Interpret cluster characteristics."""
            row = cluster_profiles.loc[cluster_id]
            
            r_mean = row['Recency_mean']
            f_mean = row['Frequency_mean']
            m_mean = row['Monetary_mean']
            
            # Get median values for comparison
            r_median = self.rfm_df['Recency'].median()
            f_median = self.rfm_df['Frequency'].median()
            m_median = self.rfm_df['Monetary'].median()
            
            r_recent = r_mean < r_median
            f_high = f_mean > f_median
            m_high = m_mean > m_median
            
            count = int(row['Recency_count'])
            percentage = (count / len(self.rfm_df)) * 100
            
            if r_recent and f_high and m_high:
                segment = "Champions"
                description = "Best customers: Recent, Frequent, High Value"
                strategy = "Reward loyalty, exclusive offers, VIP treatment"
            elif not r_recent and f_high and m_high:
                segment = "Loyal Customers"
                description = "Historically valuable but haven't purchased recently"
                strategy = "Win back campaigns, special incentives"
            elif r_recent and not f_high and m_high:
                segment = "Big Spenders"
                description = "Recent large purchases but infrequent"
                strategy = "Cross-sell, premium products"
            elif r_recent and f_high and not m_high:
                segment = "At Risk"
                description = "Active but low value, may leave"
                strategy = "Upsell, incentives, engagement"
            elif not r_recent and not f_high and m_high:
                segment = "Potential Loyalists"
                description = "High value but disengaged"
                strategy = "Reactivation campaigns"
            elif not r_recent and f_high and not m_high:
                segment = "Need Attention"
                description = "Active but low spending, declining"
                strategy = "Win back, check satisfaction"
            elif r_recent and not f_high and not m_high:
                segment = "New Customers"
                description = "Recent, low frequency, low value"
                strategy = "Nurture, education, onboarding"
            else:
                segment = "Lost"
                description = "No recent purchases"
                strategy = "Re-engagement campaigns, surveys"
            
            return {
                'cluster': cluster_id,
                'segment': segment,
                'count': count,
                'percentage': percentage,
                'avg_recency': r_mean,
                'avg_frequency': f_mean,
                'avg_monetary': m_mean,
                'description': description,
                'strategy': strategy
            }
        
        interpretations = []
        for cluster_id in sorted(self.clustered_df['Cluster'].unique()):
            if cluster_id != -1:  # Skip noise points
                interpretations.append(interpret_cluster(cluster_id))
        
        interpretation_df = pd.DataFrame(interpretations)
        
        for _, row in interpretation_df.iterrows():
            print(f"\n{'─' * 58}")
            print(f"Cluster {int(row['cluster'])}: {row['segment'].upper()}")
            print(f"{'─' * 58}")
            print(f"Customers: {int(row['count'])} ({row['percentage']:.1f}%)")
            print(f"Description: {row['description']}")
            print(f"Avg Recency: {row['avg_recency']:.1f} days")
            print(f"Avg Frequency: {row['avg_frequency']:.1f} purchases")
            print(f"Avg Spending: ${row['avg_monetary']:.2f}")
            print(f"Strategy: {row['strategy']}")
        
        self.results['interpretations'] = interpretation_df
        
        return interpretation_df
    
    def generate_visualizations(self, output_dir: str = 'outputs') -> None:
        """Generate all visualizations."""
        print(f"\nGenerating visualizations in {output_dir}...")
        
        Path(output_dir).mkdir(exist_ok=True)
        
        # Elbow curve
        opt_results = self.results['optimization']
        Visualizer.plot_elbow_curve(
            opt_results['k_range'], 
            opt_results['inertia'], 
            opt_results['silhouette'],
            save_path=f"{output_dir}/01_elbow_curve.png"
        )
        
        # Cluster visualization
        Visualizer.plot_clusters_pca(
            self.results['pca_data'],
            self.clustered_df['Cluster'].values,
            save_path=f"{output_dir}/02_clusters_pca.png"
        )
        
        # RFM distribution
        Visualizer.plot_rfm_distribution(
            self.rfm_df,
            save_path=f"{output_dir}/03_rfm_distribution.png"
        )
        
        # Cluster profiles
        cluster_profiles = pd.DataFrame(self.results['cluster_profiles'])
        Visualizer.plot_cluster_profiles(
            cluster_profiles,
            save_path=f"{output_dir}/04_cluster_profiles.png"
        )
        
        # Segment sizes
        Visualizer.plot_segment_sizes(
            self.clustered_df,
            save_path=f"{output_dir}/05_cluster_sizes.png"
        )
        
        print(f"✓ All visualizations saved to {output_dir}/")
    
    def save_results(self, output_dir: str = 'outputs') -> None:
        """Save results to CSV and JSON."""
        Path(output_dir).mkdir(exist_ok=True)
        
        # Save RFM data
        self.rfm_df.to_csv(f"{output_dir}/rfm_analysis.csv", index=False)
        
        # Save clustered data
        self.clustered_df.to_csv(f"{output_dir}/clustered_customers.csv", index=False)
        
        # Save interpretations
        if 'interpretations' in self.results:
            self.results['interpretations'].to_csv(
                f"{output_dir}/segment_interpretations.csv", index=False
            )
        
        # Save summary report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_customers': len(self.rfm_df),
            'rfm_statistics': self.results['rfm_stats'],
            'clustering_evaluation': {
                k: v for k, v in self.results['evaluation'].items() 
                if k not in ['n_clusters']
            },
            'pca_variance': list(self.results['pca_variance'])
        }
        
        with open(f"{output_dir}/analysis_report.json", 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✓ Results saved to {output_dir}/")
    
    def run_full_pipeline(self, n_clusters: int = 4, output_dir: str = 'outputs') -> dict:
        """
        Run complete segmentation pipeline.
        
        Args:
            n_clusters: Number of clusters
            output_dir: Output directory for results
            
        Returns:
            Results dictionary
        """
        print("\n" + "=" * 60)
        print("CUSTOMER SEGMENTATION PIPELINE")
        print("=" * 60 + "\n")
        
        self.load_data()
        self.perform_rfm_analysis()
        self.apply_clustering(n_clusters=n_clusters)
        self.interpret_segments()
        self.generate_visualizations(output_dir)
        self.save_results(output_dir)
        
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        return self.results


if __name__ == "__main__":
    # Run pipeline
    pipeline = SegmentationPipeline(use_sample=True)
    results = pipeline.run_full_pipeline(n_clusters=4, output_dir='outputs')
