# Customer Segmentation - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run the Pipeline
```bash
# Generate outputs in the outputs/ folder
python src/main_pipeline.py
```

### 3. Launch Dashboard
```bash
# Start interactive web app
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

---

## 📋 File Guide

| File | Purpose |
|------|---------|
| `src/rfm_analysis.py` | RFM calculation engine |
| `src/clustering.py` | K-Means and DBSCAN clustering |
| `src/visualization.py` | Plotting utilities |
| `src/main_pipeline.py` | Complete analysis workflow |
| `app.py` | Streamlit dashboard |
| `config.py` | Project configuration |
| `data_generator.py` | Generate sample data |

---

## 🎯 Key Concepts

### RFM Analysis
- **Recency**: Days since last purchase
- **Frequency**: Total number of purchases
- **Monetary**: Total amount spent

### Clustering
- Find natural customer groups using K-Means
- Evaluate with Silhouette Score
- Visualize with PCA

### Business Segments
- **Champions**: Best customers
- **Loyal Customers**: High value, at risk
- **Big Spenders**: Large but infrequent purchases
- **At Risk**: Active but low spending
- And 4 more segments...

---

## 💡 Example Code

### Using the Pipeline Directly

```python
from src.main_pipeline import SegmentationPipeline

# Create pipeline
pipeline = SegmentationPipeline(use_sample=True)

# Run full analysis
results = pipeline.run_full_pipeline(
    n_clusters=4,
    output_dir='outputs'
)

# Access results
rfm_data = results['rfm_stats']
cluster_profiles = results['cluster_profiles']
interpretations = results['interpretations']
```

### Using Individual Modules

```python
from src.rfm_analysis import RFMAnalysis
from src.clustering import ClusteringEngine

# RFM Analysis
rfm = RFMAnalysis(df)
rfm_df = rfm.calculate_rfm()

# Clustering
clusterer = ClusteringEngine(rfm_df)
clusterer.scale_data()
optimization = clusterer.find_optimal_clusters(max_k=10)
clustered = clusterer.apply_kmeans(n_clusters=4)
metrics = clusterer.get_evaluation_metrics()
```

---

## 📊 Output Files

After running `main_pipeline.py`, you'll find in `outputs/`:

```
outputs/
├── rfm_analysis.csv                 # RFM metrics for each customer
├── clustered_customers.csv          # Customers with cluster labels
├── segment_interpretations.csv      # Segment definitions
├── analysis_report.json             # Summary statistics
├── 01_elbow_curve.png              # Optimization chart
├── 02_clusters_pca.png             # 2D cluster visualization
├── 03_rfm_distribution.png         # RFM histograms
├── 04_cluster_profiles.png         # RFM means by cluster
└── 05_cluster_sizes.png            # Segment distribution
```

---

## 🔧 Customization

### Use Your Own Data
```python
import pandas as pd
from src.main_pipeline import SegmentationPipeline

df = pd.read_csv('your_data.csv')

pipeline = SegmentationPipeline(use_sample=False)
pipeline.df = df
results = pipeline.run_full_pipeline(n_clusters=4)
```

### Adjust Number of Clusters
```python
# Try different k values
for k in [3, 4, 5, 6]:
    results = pipeline.run_full_pipeline(n_clusters=k)
```

### Use DBSCAN Instead
```python
from src.clustering import ClusteringEngine

clusterer = ClusteringEngine(rfm_df)
clusterer.scale_data()
clustered = clusterer.apply_dbscan(eps=0.8, min_samples=5)
```

---

## 📈 Next Steps

1. ✅ Run the pipeline with sample data
2. ✅ Explore the Streamlit dashboard
3. ✅ Review generated visualizations
4. ✅ Prepare your own retail data
5. ✅ Run analysis on real data
6. ✅ Use insights for marketing campaigns

---

## ❓ Troubleshooting

**Issue**: Streamlit not found
```bash
pip install streamlit==1.28.1
```

**Issue**: Import errors
```bash
# Ensure you're in the correct directory
cd CustomerSegmentation
python src/main_pipeline.py
```

**Issue**: Data not loading
```python
# Check data path and column names
print(df.columns)
print(df.head())
```

---

## 📚 Resources

- [RFM Analysis Guide](https://en.wikipedia.org/wiki/RFM_(customer_value))
- [Scikit-learn K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Streamlit Tutorial](https://docs.streamlit.io/library/get-started)

---

**Happy Segmenting! 🎯📊**
