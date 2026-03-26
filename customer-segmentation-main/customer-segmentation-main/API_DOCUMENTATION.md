# API Documentation

## Module Reference

### rfm_analysis.py

#### RFMAnalysis Class

```python
class RFMAnalysis:
    """Perform RFM analysis on transaction data."""
    
    def __init__(self, df: pd.DataFrame, reference_date: datetime = None)
    def calculate_rfm(self) -> pd.DataFrame
    def assign_rfm_scores(self, q: int = 4) -> pd.DataFrame
    def get_statistics(self) -> Dict
    def segment_by_percentile(self) -> pd.DataFrame
```

**Methods:**

- `calculate_rfm()`: Calculates Recency, Frequency, and Monetary metrics
- `assign_rfm_scores(q=4)`: Assigns RFM scores based on quantiles
- `get_statistics()`: Returns summary statistics
- `segment_by_percentile()`: Creates 8 customer segments based on RFM

**Example:**
```python
from src.rfm_analysis import RFMAnalysis

rfm = RFMAnalysis(df)
rfm_df = rfm.calculate_rfm()
stats = rfm.get_statistics()
print(f"Total Revenue: ${stats['total_revenue']:.2f}")
```

---

### clustering.py

#### ClusteringEngine Class

```python
class ClusteringEngine:
    """Handle clustering operations and evaluation."""
    
    def __init__(self, rfm_df: pd.DataFrame)
    def scale_data(self) -> np.ndarray
    def find_optimal_clusters(self, max_k: int = 10) -> dict
    def apply_kmeans(self, n_clusters: int) -> pd.DataFrame
    def apply_dbscan(self, eps: float = 0.5, min_samples: int = 5) -> pd.DataFrame
    def get_evaluation_metrics(self) -> dict
    def apply_pca(self, n_components: int = 2) -> np.ndarray
    def get_cluster_profiles(self, clustered_df: pd.DataFrame) -> pd.DataFrame
```

**Methods:**

- `scale_data()`: Normalize RFM values using StandardScaler
- `find_optimal_clusters()`: Use Elbow Method to find optimal K
- `apply_kmeans(n_clusters)`: Apply K-Means clustering
- `apply_dbscan()`: Apply DBSCAN clustering
- `get_evaluation_metrics()`: Calculate Silhouette, Davies-Bouldin, Calinski-Harabasz scores
- `apply_pca()`: Reduce to 2D for visualization
- `get_cluster_profiles()`: Generate cluster statistics

**Example:**
```python
from src.clustering import ClusteringEngine

clusterer = ClusteringEngine(rfm_df)
clusterer.scale_data()

# Find optimal k
optimization = clusterer.find_optimal_clusters(max_k=10)

# Apply K-Means
clustered = clusterer.apply_kmeans(n_clusters=4)

# Evaluate
metrics = clusterer.get_evaluation_metrics()
print(f"Silhouette Score: {metrics['silhouette_score']:.4f}")
```

---

### visualization.py

#### Visualizer Class

```python
class Visualizer:
    """Create visualizations for customer segmentation."""
    
    @staticmethod
    def plot_elbow_curve(k_range, inertia, silhouette, save_path=None)
    @staticmethod
    def plot_clusters_pca(pca_data, labels, title="...", save_path=None)
    @staticmethod
    def plot_rfm_distribution(rfm_df, save_path=None)
    @staticmethod
    def plot_cluster_profiles(cluster_profiles, save_path=None)
    @staticmethod
    def plot_segment_sizes(segment_df, save_path=None)
```

**Methods:**

- `plot_elbow_curve()`: Elbow method and silhouette score curves
- `plot_clusters_pca()`: 2D PCA projection of clusters
- `plot_rfm_distribution()`: RFM histograms and box plots
- `plot_cluster_profiles()`: RFM means by cluster
- `plot_segment_sizes()`: Segment distribution pie and bar charts

**Example:**
```python
from src.visualization import Visualizer

Visualizer.plot_clusters_pca(
    pca_data, 
    labels, 
    save_path='output.png'
)
```

---

### main_pipeline.py

#### DataPreprocessor Class

```python
class DataPreprocessor:
    @staticmethod
    def clean_data(df, verbose=True) -> pd.DataFrame
    @staticmethod
    def load_sample_data() -> pd.DataFrame
```

#### SegmentationPipeline Class

```python
class SegmentationPipeline:
    """Complete customer segmentation pipeline."""
    
    def __init__(self, data_path=None, use_sample=True)
    def load_data(self) -> pd.DataFrame
    def perform_rfm_analysis(self) -> pd.DataFrame
    def apply_clustering(self, n_clusters=4, algorithm='kmeans') -> pd.DataFrame
    def interpret_segments(self) -> pd.DataFrame
    def generate_visualizations(self, output_dir='outputs') -> None
    def save_results(self, output_dir='outputs') -> None
    def run_full_pipeline(self, n_clusters=4, output_dir='outputs') -> dict
```

**Example:**
```python
from src.main_pipeline import SegmentationPipeline

pipeline = SegmentationPipeline(use_sample=True)
results = pipeline.run_full_pipeline(n_clusters=4, output_dir='outputs')
```

---

## Data Formats

### Input Data Format

Required CSV columns:
```
CustomerID,InvoiceID,InvoiceDate,Quantity,UnitPrice
1001,INV00001,2023-01-15,2,29.99
1002,INV00002,2023-01-15,5,14.99
```

### RFM Output Format

```
CustomerID,Recency,Frequency,Monetary
1001,15,12,359.76
1002,5,8,224.95
```

### Clustered Output Format

```
CustomerID,Recency,Frequency,Monetary,Cluster
1001,15,12,359.76,2
1002,5,8,224.95,0
```

### Evaluation Metrics Output

```json
{
  "silhouette_score": 0.4532,
  "davies_bouldin_score": 0.8234,
  "calinski_harabasz_score": 156.78,
  "n_clusters": 4,
  "n_noise_points": 0
}
```

---

## Configuration Options

### Clustering Parameters

```python
# K-Means
KMEANS_PARAMS = {
    'n_clusters': 4,           # Number of clusters
    'random_state': 42,        # For reproducibility
    'n_init': 10,              # Number of initializations
}

# DBSCAN
DBSCAN_PARAMS = {
    'eps': 0.8,                # Distance threshold
    'min_samples': 5,          # Minimum samples in neighborhood
}
```

### Visualization Parameters

```python
VIZ_PARAMS = {
    'figsize_single': (12, 6),
    'figsize_double': (14, 5),
    'figsize_triple': (16, 5),
    'dpi': 300,
    'cmap': 'viridis',
}
```

---

## Error Handling

### Common Errors and Solutions

**Error**: `ValueError: No features to scale`
- **Cause**: RFM data is empty
- **Solution**: Ensure data has valid transactions

**Error**: `KeyError: 'CustomerID'`
- **Cause**: Column name mismatch
- **Solution**: Check CSV column names match expected format

**Error**: `No valid features for clustering`
- **Cause**: All RFM values are identical
- **Solution**: Verify data quality and variation

**Error**: `Silhouette score cannot be computed`
- **Cause**: Only one cluster found
- **Solution**: Increase max_k or check data

---

## Performance Notes

### Dataset Size Guidelines

| Customers | Transactions | Time | Memory |
|-----------|-------------|------|--------|
| 100 | 500 | <1s | <50MB |
| 1,000 | 5,000 | ~1s | ~50MB |
| 10,000 | 50,000 | ~5s | ~200MB |
| 100,000 | 500,000 | ~30s | ~500MB |

### Optimization Tips

1. **Use sample data** for initial exploration
2. **Cache results** when iterating on parameters
3. **Increase n_init** for K-Means on large datasets
4. **Use DBSCAN** for varying cluster sizes
5. **Monitor memory** with large datasets

---

## Best Practices

1. **Always check data quality** before analysis
2. **Use Elbow Method** to find optimal k
3. **Compare multiple clustering algorithms**
4. **Validate results** with domain experts
5. **Monitor cluster stability** over time
6. **Update segments** regularly (monthly/quarterly)

---

## Troubleshooting

### Dashboard Not Starting
```bash
# Clear Streamlit cache
streamlit cache clear

# Reinstall Streamlit
pip install --upgrade streamlit
```

### Memory Issues
```python
# Process data in chunks
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    # Process chunk
    pass
```

### Slow Clustering
```python
# Reduce max_k in optimization
optimization = clusterer.find_optimal_clusters(max_k=6)

# Use DBSCAN for faster results
clusterer.apply_dbscan(eps=0.8, min_samples=5)
```

---

## Version History

### v1.0.0 (Current)
- Initial release
- RFM analysis
- K-Means and DBSCAN clustering
- Streamlit dashboard
- Comprehensive visualization

---

## Support & Contributing

For issues, suggestions, or contributions:
1. Review README.md
2. Check QUICKSTART.md
3. Run examples.py
4. Review API documentation (this file)
