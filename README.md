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
customer-segmentation-main/
└── customer-segmentation-main/
    ├── app.py                    # Main Streamlit dashboard UI
    ├── streamlit_app.py          # Streamlit Cloud entrypoint
    ├── dashboard.py              # Old Flask dashboard backend
    ├── data_loader.py            # CSV/Excel loading and preprocessing
    ├── data_generator.py         # Sample data generation utilities
    ├── config.py                 # Project configuration
    ├── requirements.txt          # Python dependencies for deployment
    ├── README.md                 # Project documentation
    ├── QUICKSTART.md             # Quick start guide
    ├── API_DOCUMENTATION.md      # API reference for Flask routes
    ├── PROJECT_SUMMARY.md        # Project overview
    ├── INDEX.md                  # Documentation index
    ├── MANIFEST.md               # File manifest
    ├── COMPLETION_CHECKLIST.md   # Project completion checklist
    ├── verify_installation.py    # Installation verification script
    ├── examples.py               # Example usage
    ├── run.py                    # Local launcher script
    ├── .gitignore                # Git ignore configuration
    ├── .streamlit/
    │   └── config.toml           # Streamlit theme and server config
    ├── templates/
    │   └── index.html            # Old Flask HTML dashboard template
    ├── src/
    │   ├── __init__.py           # Package marker
    │   ├── rfm_analysis.py       # RFM calculation engine
    │   ├── clustering.py         # Clustering algorithms and metrics
    │   ├── visualization.py      # Plotting utilities
    │   └── main_pipeline.py      # End-to-end segmentation pipeline
    ├── uploads/                  # Temporary uploaded files
    ├── outputs/                  # Generated CSVs, JSON, and charts
    └── __pycache__/              # Python cache files

```

## Technology Stack
Frontend: Streamlit
Backend / Data Processing: Pandas, NumPy
Machine Learning: Scikit-learn
Visualization: Matplotlib, Seaborn
File Support: CSV, XLSX, XLS
Deployment: Streamlit Community Cloud
Legacy Support: Flask dashboard remains in the repo
## Installation
Clone the repository
git clone <your-repo-url>
cd customer-segmentation-main/customer-segmentation-main
Create a virtual environment
python -m venv venv
Activate the environment
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
🚀 Usage
Run the Streamlit Dashboard Locally
streamlit run streamlit_app.py
Then open:

http://localhost:8501
Main Deployment Entry Point
For Streamlit Community Cloud, use:

customer-segmentation-main/customer-segmentation-main/streamlit_app.py
## Dashboard Features
Load sample retail data
Upload CSV, XLSX, or XLS files
Perform RFM analysis
Configure cluster count
View optimization and evaluation metrics
Explore customer segments and strategies
Visualize PCA clusters and profiles
Export results as CSV and JSON
## Dashboard Workflow
Load Data from the sidebar
Analyze RFM Metrics
Run Clustering
Review Optimization and Metrics
Inspect Segment Interpretations
Export Results
## RFM Metrics
Metric	Definition	Business Meaning
Recency (R)	Days since last purchase	More recent customers are often more valuable
Frequency (F)	Number of purchases	Frequent buyers indicate loyalty
Monetary (M)	Total amount spent	High spending implies higher customer value
## Customer Segments
The system identifies business-friendly customer groups such as:

Champions
Loyal Customers
Big Spenders
At Risk
Potential Loyalists
Need Attention
New Customers
Lost
These labels are generated from cluster profiles using RFM behavior.

## Clustering Evaluation Metrics
Silhouette Score: Higher is better
Davies-Bouldin Index: Lower is better
Calinski-Harabasz Score: Higher is better
## Visualizations
The Streamlit dashboard includes:

RFM Distribution
Elbow Method Curve
Silhouette Trend
PCA Cluster Projection
Cluster Size Distribution
Cluster Profile Heatmap
## Input Data Format
Required columns:

CustomerID,InvoiceID,InvoiceDate,Quantity,UnitPrice
1001,INV00001,2023-01-15,2,29.99
1002,INV00002,2023-01-15,5,14.99
Supported file types:

.csv
.xlsx
.xls
## Output Files
Generated exports may include:

rfm_analysis.csv
customer_segments.csv
customer_segments.json
The outputs/ folder may also contain pipeline-generated charts and reports when running batch scripts.

🔧 Configuration
Run Pipeline Programmatically
from src.main_pipeline import SegmentationPipeline

pipeline = SegmentationPipeline(use_sample=True)
results = pipeline.run_full_pipeline(
    n_clusters=4,
    output_dir="outputs"
)
Use the Streamlit App Entry Function
from app import main

main()
☁️ Streamlit Cloud Deployment
Push the latest code to GitHub
Open Streamlit Community Cloud
Create a new app
Select your repository and branch
Set the main file path to:
customer-segmentation-main/customer-segmentation-main/streamlit_app.py
Click Deploy
📚 Learning Outcomes
After completing this project, you will understand:

RFM analysis implementation
Customer segmentation with K-Means
Cluster evaluation techniques
PCA-based visualization
Data cleaning and preprocessing
Streamlit dashboard development
End-to-end machine learning workflow deployment
##🔗 References
RFM Analysis Wikipedia
K-Means Clustering
Streamlit Documentation
Scikit-learn Clustering Metrics
📝 License
This project is open source and available for educational and commercial use.

## Contributing
Contributions are welcome. You can help by:

Reporting bugs
Suggesting UI improvements
Improving visualizations
Adding more clustering methods
Enhancing documentation
---
