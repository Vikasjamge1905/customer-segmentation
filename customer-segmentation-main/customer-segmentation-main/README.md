# Customer Segmentation - RFM Analysis System

A professional customer segmentation platform using RFM (Recency, Frequency, Monetary) analysis combined with K-Means clustering. Features a modern Flask web dashboard for real-time analysis and business insights.

## 📋 Project Overview

This project implements a complete end-to-end customer segmentation pipeline:

1. **Data Cleaning**: Remove nulls, duplicates, and invalid transactions
2. **RFM Analysis**: Calculate Recency, Frequency, and Monetary metrics
3. **Clustering**: Apply K-Means with Elbow Method optimization
4. **Evaluation**: Silhouette Score, Davies-Bouldin Index, Calinski-Harabasz Score
5. **Business Interpretation**: Assign segment labels with actionable insights
6. **Dashboard**: Interactive Flask web application with professional UI

## 🏗️ Project Structure

```
CustomerSegmentation/
├── dashboard.py                    # Flask web server with API endpoints
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore configuration
├── README.md                       # Project documentation
├── templates/
│   └── index.html                 # Web dashboard UI (professional design)
├── src/                           # Source code modules
│   ├── rfm_analysis.py           # RFM calculation engine
│   ├── clustering.py             # Clustering algorithms & evaluation
│   ├── visualization.py          # Matplotlib plotting utilities
│   ├── main_pipeline.py          # Complete pipeline orchestrator
│   └── data_loader.py            # Excel/CSV data loading & preprocessing
└── uploads/                      # Temporary file storage for uploads
```

## 🛠️ Technology Stack

- **Backend**: Flask, Pandas, NumPy, Scikit-learn
- **Frontend**: HTML5, CSS3 (Gradient Design), Chart.js, Vanilla JavaScript
- **Data Processing**: Excel/CSV support with auto-standardization
- **ML Algorithms**: K-Means Clustering, PCA, Silhouette Analysis
- **Python 3.8+**: Core language

## 📦 Installation

1. **Clone/Download the project**:
```bash
cd CustomerSegmentation
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Start the Web Dashboard

```bash
python dashboard.py
```

Then open your browser to `http://localhost:5000`

**Dashboard Features:**
- 📁 Upload custom Excel/CSV data or load sample dataset
- 📊 Interactive RFM analysis with real-time statistics
- 🎯 Cluster optimization with elbow curve visualization
- 💡 Automatic segment interpretation with business strategies
- 📈 Professional metrics display (Silhouette, Davies-Bouldin, Calinski-Harabasz)
- 💾 Export results as CSV or JSON

### Dashboard Workflow

1. **Load Data**: Click "Load Sample Data" or upload your Excel/CSV file
2. **Analyze RFM**: View automatic RFM calculations and statistics
3. **Optimize Clusters**: See elbow curve and silhouette analysis
4. **Generate Segments**: Click "Generate Interpretations" for business insights
5. **Export Results**: Download customer segments and analysis results

## 📊 RFM Metrics

| Metric | Definition | Business Meaning |
|--------|-----------|-----------------|
| **Recency (R)** | Days since last purchase | Recent customers are more valuable |
| **Frequency (F)** | Number of purchases | Loyal customers purchase more often |
| **Monetary (M)** | Total amount spent | High spenders have higher lifetime value |

## 🎯 Customer Segments

The system identifies 8 customer segments:

| Segment | Characteristics | Strategy |
|---------|-----------------|----------|
| **Champions** | High R, High F, High M | Reward loyalty, VIP treatment |
| **Loyal Customers** | Low R, High F, High M | Win-back campaigns |
| **Big Spenders** | High R, Low F, High M | Cross-sell premium products |
| **At Risk** | High R, High F, Low M | Upsell, engagement initiatives |
| **Potential Loyalists** | Low R, Low F, High M | Reactivation campaigns |
| **Need Attention** | Low R, High F, Low M | Check satisfaction, incentives |
| **New Customers** | High R, Low F, Low M | Nurture, onboarding |
| **Lost** | Low R, Low F, Low M | Re-engagement campaigns |

## 📈 Clustering Evaluation Metrics

- **Silhouette Score** (-1 to 1): Higher is better. Measures cohesion and separation.
- **Davies-Bouldin Index**: Lower is better. Ratio of within to between-cluster distances.
- **Calinski-Harabasz Score**: Higher is better. Ratio of between to within-cluster dispersion.

## 🎨 Visualizations

The system generates:

1. **Elbow Curve**: Identifies optimal number of clusters
2. **Silhouette Score**: Evaluates cluster quality
3. **PCA 2D Projection**: Visual cluster separation
4. **RFM Distribution**: Histogram and box plots
5. **Cluster Profiles**: RFM means by cluster
6. **Segment Distribution**: Size and composition

## 💾 Input Data Format

Required CSV columns:
```
CustomerID,InvoiceID,InvoiceDate,Quantity,UnitPrice
1001,INV00001,2023-01-15,2,29.99
1002,INV00002,2023-01-15,5,14.99
...
```

## 📁 Output Files

After running the pipeline:

- **rfm_analysis.csv**: Raw RFM metrics for each customer
- **clustered_customers.csv**: Customers with assigned clusters
- **segment_interpretations.csv**: Cluster labels and characteristics
- **analysis_report.json**: Summary statistics and metrics
- **Visualizations** (PNG): 5 high-resolution plots

## 🔧 Configuration

### Main Pipeline Options

```python
pipeline = SegmentationPipeline(use_sample=True)
results = pipeline.run_full_pipeline(
    n_clusters=4,           # Number of clusters
    output_dir='outputs'    # Output directory
)
```

### Clustering Parameters

```python
# K-Means
clusterer.apply_kmeans(n_clusters=4)

# DBSCAN
clusterer.apply_dbscan(eps=0.8, min_samples=5)
```

## 📊 Example Results

### RFM Statistics
```
Total Customers: 500
Recency (Mean): 45.2 days
Frequency (Mean): 10.1 purchases
Monetary (Mean): $1,234.56
Total Revenue: $617,280.00
```

### Clustering Metrics (k=4)
```
Silhouette Score: 0.4532
Davies-Bouldin Score: 0.8234
Calinski-Harabasz Score: 156.78
```

### Segment Distribution
```
Cluster 0: 125 customers (25.0%) - Champions
Cluster 1: 145 customers (29.0%) - Loyal Customers
Cluster 2: 110 customers (22.0%) - Big Spenders
Cluster 3: 120 customers (24.0%) - At Risk
```

## 🚀 Advanced Features

### 1. Custom Data Input
```python
df = pd.read_csv('your_data.csv')
pipeline = SegmentationPipeline()
pipeline.df = df
pipeline.perform_rfm_analysis()
```

### 2. Compare Algorithms
```python
clusterer.apply_kmeans(n_clusters=4)
clusterer.apply_dbscan(eps=0.5, min_samples=5)
```

### 3. Export for Power BI
```python
# All CSVs are Power BI compatible
# Import clustered_customers.csv directly
```

## 📈 Business Applications

- **Targeted Marketing**: Different campaigns for each segment
- **Customer Retention**: Identify at-risk customers early
- **Revenue Optimization**: Focus on high-value segments
- **Resource Allocation**: Efficient budget distribution
- **Product Recommendation**: Tailor offers by segment
- **Churn Prediction**: Monitor movement between segments

## 🎓 Learning Outcomes

After completing this project, you will understand:

✅ RFM analysis methodology and implementation
✅ K-Means clustering algorithm and optimization
✅ Clustering evaluation metrics and interpretation
✅ PCA for dimensionality reduction
✅ Data preprocessing and feature engineering
✅ Building interactive dashboards with Streamlit
✅ Business interpretation of ML results
✅ End-to-end ML pipeline development

## 🔗 References

- [RFM Analysis Wikipedia](https://en.wikipedia.org/wiki/RFM_(customer_value))
- [K-Means Clustering](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Scikit-learn Metrics](https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation)

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Add new clustering algorithms
- Enhance visualizations

## ❓ FAQ

**Q: What if my data has missing values?**
A: The pipeline automatically removes rows with null CustomerID and InvoiceDate. For other columns, modify the `clean_data()` method.

**Q: How do I choose the optimal k?**
A: Use the Elbow Method curve. Look for the "elbow" point where adding more clusters doesn't significantly reduce inertia. The Silhouette Score helps confirm the choice.

**Q: Can I use my own data format?**
A: Yes! Modify the column names in `rfm_analysis.py` to match your data. Ensure you have CustomerID, purchase date, quantity, and price.

**Q: What's the ideal number of clusters?**
A: Typically 3-5 clusters work well. Use the optimization curves to guide your choice based on your business needs.

**Q: Can I export for use in other tools?**
A: Yes! All results are saved as CSV files compatible with Excel, Power BI, Tableau, and other analytics tools.

---

**Built with ❤️ for customer segmentation and business intelligence**
