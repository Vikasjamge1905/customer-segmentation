"""
Configuration and utilities for the customer segmentation project
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Create directories if they don't exist
SRC_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

# Clustering settings
CLUSTERING_DEFAULTS = {
    'n_clusters': 4,
    'kmeans_random_state': 42,
    'kmeans_n_init': 10,
    'dbscan_eps': 0.8,
    'dbscan_min_samples': 5,
}

# Visualization settings
VISUALIZATION_DEFAULTS = {
    'figsize_single': (12, 6),
    'figsize_double': (14, 5),
    'figsize_triple': (16, 5),
    'dpi': 300,
    'style': 'whitegrid',
}

# RFM Settings
RFM_SETTINGS = {
    'quantiles': 4,  # Quartiles for scoring
    'date_format': '%Y-%m-%d',
}
