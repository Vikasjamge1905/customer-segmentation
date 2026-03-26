"""
Customer Segmentation Package
End-to-end RFM analysis and clustering for customer segmentation
"""

__version__ = "1.0.0"
__author__ = "Customer Insights Team"

from .rfm_analysis import RFMAnalysis
from .clustering import ClusteringEngine
from .visualization import Visualizer

__all__ = ['RFMAnalysis', 'ClusteringEngine', 'Visualizer']
