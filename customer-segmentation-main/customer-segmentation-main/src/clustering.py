"""
Clustering Module
Implements K-Means, DBSCAN, and evaluation metrics
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import warnings
warnings.filterwarnings('ignore')


class ClusteringEngine:
    """Handle clustering operations and evaluation."""
    
    def __init__(self, rfm_df: pd.DataFrame):
        """
        Initialize clustering engine.
        
        Args:
            rfm_df: RFM dataframe with Recency, Frequency, Monetary columns
        """
        self.rfm_df = rfm_df.copy()
        self.scaler = StandardScaler()
        self.scaled_data = None
        self.labels = None
        self.model = None
        self.pca_data = None
        
    def scale_data(self) -> np.ndarray:
        """
        Scale RFM data using StandardScaler.
        
        Returns:
            Scaled RFM data
        """
        rfm_features = self.rfm_df[['Recency', 'Frequency', 'Monetary']].values
        self.scaled_data = self.scaler.fit_transform(rfm_features)
        return self.scaled_data
    
    def find_optimal_clusters(self, max_k: int = 10) -> dict:
        """
        Use Elbow Method to find optimal number of clusters.
        
        Args:
            max_k: Maximum number of clusters to test
            
        Returns:
            Dictionary with inertia and silhouette scores for each k
        """
        if self.scaled_data is None:
            self.scale_data()
        
        inertias = []
        silhouette_scores = []
        k_range = range(2, max_k + 1)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(self.scaled_data)
            inertias.append(kmeans.inertia_)
            
            score = silhouette_score(self.scaled_data, kmeans.labels_)
            silhouette_scores.append(score)
        
        return {
            'k_range': list(k_range),
            'inertia': inertias,
            'silhouette': silhouette_scores
        }
    
    def apply_kmeans(self, n_clusters: int) -> pd.DataFrame:
        """
        Apply K-Means clustering.
        
        Args:
            n_clusters: Number of clusters
            
        Returns:
            DataFrame with cluster labels
        """
        if self.scaled_data is None:
            self.scale_data()
        
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.labels = self.model.fit_predict(self.scaled_data)
        
        result = self.rfm_df.copy()
        result['Cluster'] = self.labels
        return result
    
    def apply_dbscan(self, eps: float = 0.5, min_samples: int = 5) -> pd.DataFrame:
        """
        Apply DBSCAN clustering.
        
        Args:
            eps: Maximum distance between samples
            min_samples: Minimum samples in neighborhood
            
        Returns:
            DataFrame with cluster labels
        """
        if self.scaled_data is None:
            self.scale_data()
        
        self.model = DBSCAN(eps=eps, min_samples=min_samples)
        self.labels = self.model.fit_predict(self.scaled_data)
        
        result = self.rfm_df.copy()
        result['Cluster'] = self.labels
        return result
    
    def get_evaluation_metrics(self) -> dict:
        """
        Calculate clustering evaluation metrics.
        
        Returns:
            Dictionary with evaluation metrics
        """
        if self.labels is None or self.scaled_data is None:
            raise ValueError("Run clustering first before evaluation")
        
        # Filter out noise points for DBSCAN (label -1)
        mask = self.labels != -1
        valid_labels = self.labels[mask]
        valid_data = self.scaled_data[mask]
        
        if len(np.unique(valid_labels)) < 2:
            return {
                'silhouette_score': None,
                'davies_bouldin_score': None,
                'calinski_harabasz_score': None,
                'n_clusters': len(np.unique(valid_labels)),
                'n_noise_points': np.sum(self.labels == -1)
            }
        
        return {
            'silhouette_score': silhouette_score(valid_data, valid_labels),
            'davies_bouldin_score': davies_bouldin_score(valid_data, valid_labels),
            'calinski_harabasz_score': calinski_harabasz_score(valid_data, valid_labels),
            'n_clusters': len(np.unique(valid_labels)),
            'n_noise_points': np.sum(self.labels == -1)
        }
    
    def apply_pca(self, n_components: int = 2) -> np.ndarray:
        """
        Apply PCA for dimensionality reduction.
        
        Args:
            n_components: Number of PCA components
            
        Returns:
            PCA-transformed data
        """
        if self.scaled_data is None:
            self.scale_data()
        
        pca = PCA(n_components=n_components)
        self.pca_data = pca.fit_transform(self.scaled_data)
        
        return self.pca_data, pca.explained_variance_ratio_
    
    def get_cluster_profiles(self, clustered_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate cluster profile statistics.
        
        Args:
            clustered_df: DataFrame with cluster labels
            
        Returns:
            Cluster profile statistics
        """
        cluster_profiles = clustered_df.groupby('Cluster').agg({
            'Recency': ['mean', 'median', 'count'],
            'Frequency': ['mean', 'median'],
            'Monetary': ['mean', 'median']
        }).round(2)
        
        # Flatten multi-level columns
        cluster_profiles.columns = ['_'.join(col).strip() for col in cluster_profiles.columns.values]
        
        return cluster_profiles
