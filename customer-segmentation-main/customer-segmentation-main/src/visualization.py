"""
Visualization Module
Create plots for RFM analysis, clustering, and business insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class Visualizer:
    """Create visualizations for customer segmentation."""
    
    @staticmethod
    def plot_elbow_curve(k_range: list, inertia: list, silhouette: list, 
                         save_path: Optional[str] = None) -> None:
        """
        Plot Elbow Method and Silhouette Score.
        
        Args:
            k_range: Range of k values
            inertia: Inertia values for each k
            silhouette: Silhouette scores for each k
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Elbow curve
        ax1.plot(k_range, inertia, 'bo-', linewidth=2, markersize=8)
        ax1.set_xlabel('Number of Clusters (k)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Inertia', fontsize=12, fontweight='bold')
        ax1.set_title('Elbow Method for Optimal K', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Silhouette curve
        ax2.plot(k_range, silhouette, 'go-', linewidth=2, markersize=8)
        ax2.set_xlabel('Number of Clusters (k)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Silhouette Score', fontsize=12, fontweight='bold')
        ax2.set_title('Silhouette Score by K', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def plot_clusters_pca(pca_data: np.ndarray, labels: np.ndarray, 
                         title: str = "Customer Clusters (PCA 2D Projection)",
                         save_path: Optional[str] = None) -> None:
        """
        Plot clusters using PCA projection.
        
        Args:
            pca_data: 2D PCA transformed data
            labels: Cluster labels
            title: Plot title
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Filter out noise points (label -1) for visualization
        mask = labels != -1
        scatter = ax.scatter(pca_data[mask, 0], pca_data[mask, 1], 
                           c=labels[mask], cmap='viridis', s=100, alpha=0.6, edgecolors='k')
        
        # Plot noise points separately if they exist
        if np.any(~mask):
            ax.scatter(pca_data[~mask, 0], pca_data[~mask, 1], 
                      c='red', marker='x', s=200, alpha=0.8, label='Noise Points')
        
        ax.set_xlabel('First Principal Component', fontsize=12, fontweight='bold')
        ax.set_ylabel('Second Principal Component', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Cluster', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def plot_rfm_distribution(rfm_df: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """
        Plot RFM distributions.
        
        Args:
            rfm_df: RFM dataframe
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Recency
        axes[0, 0].hist(rfm_df['Recency'], bins=50, color='skyblue', edgecolor='black')
        axes[0, 0].set_xlabel('Recency (days)', fontsize=11, fontweight='bold')
        axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Distribution of Recency', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Frequency
        axes[0, 1].hist(rfm_df['Frequency'], bins=50, color='lightcoral', edgecolor='black')
        axes[0, 1].set_xlabel('Frequency (purchases)', fontsize=11, fontweight='bold')
        axes[0, 1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Distribution of Frequency', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Monetary
        axes[1, 0].hist(rfm_df['Monetary'], bins=50, color='lightgreen', edgecolor='black')
        axes[1, 0].set_xlabel('Monetary (spending)', fontsize=11, fontweight='bold')
        axes[1, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Distribution of Monetary', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Box plots
        box_data = [rfm_df['Recency'], rfm_df['Frequency'], rfm_df['Monetary']]
        axes[1, 1].boxplot(box_data, labels=['Recency', 'Frequency', 'Monetary'])
        axes[1, 1].set_ylabel('Normalized Value', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('RFM Box Plot', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def plot_cluster_profiles(cluster_profiles: pd.DataFrame, 
                             save_path: Optional[str] = None) -> None:
        """
        Plot cluster profile statistics.
        
        Args:
            cluster_profiles: Cluster statistics dataframe
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        # Recency by cluster
        recency_data = cluster_profiles['Recency_mean'].sort_values()
        axes[0].barh(range(len(recency_data)), recency_data.values, color='skyblue', edgecolor='black')
        axes[0].set_yticks(range(len(recency_data)))
        axes[0].set_yticklabels([f"Cluster {i}" for i in recency_data.index])
        axes[0].set_xlabel('Mean Recency (days)', fontsize=11, fontweight='bold')
        axes[0].set_title('Mean Recency by Cluster', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='x')
        
        # Frequency by cluster
        frequency_data = cluster_profiles['Frequency_mean'].sort_values()
        axes[1].barh(range(len(frequency_data)), frequency_data.values, color='lightcoral', edgecolor='black')
        axes[1].set_yticks(range(len(frequency_data)))
        axes[1].set_yticklabels([f"Cluster {i}" for i in frequency_data.index])
        axes[1].set_xlabel('Mean Frequency (purchases)', fontsize=11, fontweight='bold')
        axes[1].set_title('Mean Frequency by Cluster', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='x')
        
        # Monetary by cluster
        monetary_data = cluster_profiles['Monetary_mean'].sort_values()
        axes[2].barh(range(len(monetary_data)), monetary_data.values, color='lightgreen', edgecolor='black')
        axes[2].set_yticks(range(len(monetary_data)))
        axes[2].set_yticklabels([f"Cluster {i}" for i in monetary_data.index])
        axes[2].set_xlabel('Mean Monetary (spending)', fontsize=11, fontweight='bold')
        axes[2].set_title('Mean Spending by Cluster', fontsize=12, fontweight='bold')
        axes[2].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def plot_segment_sizes(segment_df: pd.DataFrame, save_path: Optional[str] = None) -> None:
        """
        Plot segment/cluster size distribution.
        
        Args:
            segment_df: DataFrame with segment/cluster column
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Get segment/cluster column
        if 'Segment' in segment_df.columns:
            counts = segment_df['Segment'].value_counts()
            title = 'Customer Segments Distribution'
            label = 'Segment'
        else:
            counts = segment_df['Cluster'].value_counts().sort_index()
            title = 'Cluster Size Distribution'
            label = 'Cluster'
        
        # Bar plot
        counts.plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
        ax1.set_xlabel(label, fontsize=11, fontweight='bold')
        ax1.set_ylabel('Number of Customers', fontsize=11, fontweight='bold')
        ax1.set_title(f'{title} (Bar Chart)', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Pie chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(counts)))
        ax2.pie(counts.values, labels=counts.index, autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax2.set_title(f'{title} (Pie Chart)', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
