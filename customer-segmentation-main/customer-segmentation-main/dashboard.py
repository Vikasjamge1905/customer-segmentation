"""
Corporate Analytics Dashboard
Flask-based web application with professional UI
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
from pathlib import Path
import io
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import DataLoader
from src.main_pipeline import DataPreprocessor
from src.rfm_analysis import RFMAnalysis
from src.clustering import ClusteringEngine
from src.visualization import Visualizer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Global variables for caching
cached_data = {
    'df': None,
    'rfm_df': None,
    'clustered_df': None,
    'cluster_profiles': None,
    'interpretations': None,
    'optimization': None
}


def reset_analysis_cache():
    """Clear analysis outputs when dataset changes."""
    cached_data['rfm_df'] = None
    cached_data['clustered_df'] = None
    cached_data['cluster_profiles'] = None
    cached_data['interpretations'] = None
    cached_data['optimization'] = None


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file extension
        allowed_extensions = {'.csv', '.xlsx', '.xls'}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': f'File type not supported. Use: CSV, XLSX, or XLS'}), 400
        
        # Create upload directory if it doesn't exist
        upload_dir = Path(__file__).parent / 'uploads'
        upload_dir.mkdir(exist_ok=True)
        
        # Save file with unique name
        import uuid
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_path = upload_dir / unique_filename
        
        try:
            file.save(str(temp_path))
        except Exception as save_error:
            return jsonify({'error': f'Failed to save file: {str(save_error)}'}), 400
        
        try:
            # Load data
            df = DataLoader.prepare_data(str(temp_path))
            cached_data['df'] = df
            reset_analysis_cache()
            
            # Clean up temp file
            temp_path.unlink(missing_ok=True)
            
            return jsonify({
                'success': True,
                'message': f'Loaded {len(df)} transactions from {df["CustomerID"].nunique()} customers',
                'rows': len(df),
                'customers': df['CustomerID'].nunique(),
                'date_range': f"{df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}"
            })
        except Exception as load_error:
            # Clean up temp file on error
            temp_path.unlink(missing_ok=True)
            return jsonify({'error': f'Failed to process file: {str(load_error)}'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Upload error: {str(e)}'}), 400


@app.route('/api/sample-data', methods=['GET'])
def load_sample_data():
    """Load sample data."""
    try:
        # Use built-in synthetic dataset so sample flow works on any machine.
        df = DataPreprocessor.load_sample_data()
        df = DataPreprocessor.clean_data(df, verbose=False)
        cached_data['df'] = df
        reset_analysis_cache()
        
        return jsonify({
            'success': True,
            'message': f'Loaded {len(df)} transactions',
            'rows': len(df),
            'customers': df['CustomerID'].nunique(),
            'date_range': f"{df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/rfm-analysis', methods=['GET'])
def rfm_analysis():
    """Perform RFM analysis."""
    try:
        if cached_data['df'] is None:
            return jsonify({'error': 'No data loaded'}), 400
        
        df = cached_data['df']
        rfm = RFMAnalysis(df)
        rfm_df = rfm.calculate_rfm()
        cached_data['rfm_df'] = rfm_df
        
        stats = rfm.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_customers': int(stats['total_customers']),
                'total_revenue': f"${stats['total_revenue']:.2f}",
                'recency_mean': f"{stats['recency_mean']:.1f}",
                'recency_median': f"{stats['recency_median']:.1f}",
                'frequency_mean': f"{stats['frequency_mean']:.1f}",
                'frequency_median': f"{stats['frequency_median']:.1f}",
                'monetary_mean': f"${stats['monetary_mean']:.2f}",
                'monetary_median': f"${stats['monetary_median']:.2f}"
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/cluster', methods=['POST'])
def cluster():
    """Perform clustering."""
    try:
        if cached_data['rfm_df'] is None:
            return jsonify({'error': 'RFM analysis required first'}), 400
        
        data = request.json
        n_clusters = int(data.get('n_clusters', 4))
        
        rfm_df = cached_data['rfm_df']
        if len(rfm_df) < 3:
            return jsonify({'error': 'Need at least 3 customers for clustering'}), 400

        n_clusters = max(2, min(n_clusters, len(rfm_df) - 1))

        clusterer = ClusteringEngine(rfm_df)
        clusterer.scale_data()
        
        # Optimization
        optimization = clusterer.find_optimal_clusters(max_k=min(10, len(rfm_df) - 1))
        cached_data['optimization'] = optimization
        
        # Clustering
        clustered_df = clusterer.apply_kmeans(n_clusters=n_clusters)
        cached_data['clustered_df'] = clustered_df
        
        # Evaluation
        metrics = clusterer.get_evaluation_metrics()
        profiles = clusterer.get_cluster_profiles(clustered_df)
        cached_data['cluster_profiles'] = profiles
        
        return jsonify({
            'success': True,
            'metrics': {
                'silhouette_score': f"{metrics.get('silhouette_score', 0):.4f}",
                'davies_bouldin_score': f"{metrics.get('davies_bouldin_score', 0):.4f}",
                'calinski_harabasz_score': f"{metrics.get('calinski_harabasz_score', 0):.1f}",
                'n_clusters': metrics['n_clusters']
            },
            'optimization': {
                'k_range': optimization['k_range'],
                'inertia': [float(x) for x in optimization['inertia']],
                'silhouette': [float(x) for x in optimization['silhouette']]
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/interpret', methods=['GET'])
def interpret():
    """Interpret segments."""
    try:
        if cached_data['clustered_df'] is None:
            return jsonify({'error': 'Clustering required first'}), 400
        
        clustered_df = cached_data['clustered_df']
        rfm_df = cached_data['rfm_df']
        
        # Get cluster profiles
        cluster_profiles = cached_data['cluster_profiles']
        
        segments = []
        
        for cluster_id in sorted(clustered_df['Cluster'].unique()):
            if cluster_id == -1:
                continue
            
            cluster_data = clustered_df[clustered_df['Cluster'] == cluster_id]
            count = len(cluster_data)
            percentage = (count / len(clustered_df)) * 100
            
            row = cluster_profiles.loc[cluster_id]
            r_mean = row['Recency_mean']
            f_mean = row['Frequency_mean']
            m_mean = row['Monetary_mean']
            
            r_median = rfm_df['Recency'].median()
            f_median = rfm_df['Frequency'].median()
            m_median = rfm_df['Monetary'].median()
            
            r_recent = r_mean < r_median
            f_high = f_mean > f_median
            m_high = m_mean > m_median
            
            # Segment logic
            if r_recent and f_high and m_high:
                name = "Champions"
                desc = "Best customers: Recent, Frequent, High Value"
                strategy = "🏆 VIP treatment, exclusive offers, loyalty rewards"
            elif not r_recent and f_high and m_high:
                name = "Loyal Customers"
                desc = "Historically valuable but haven't purchased recently"
                strategy = "💌 Win-back campaigns, special incentives, re-engagement"
            elif r_recent and not f_high and m_high:
                name = "Big Spenders"
                desc = "Recent large purchases but infrequent"
                strategy = "🎁 Cross-sell premium products, bundle offers"
            elif r_recent and f_high and not m_high:
                name = "At Risk"
                desc = "Active but low value, may leave"
                strategy = "📈 Upsell, engagement campaigns, value bundling"
            elif not r_recent and not f_high and m_high:
                name = "Potential Loyalists"
                desc = "High value but disengaged"
                strategy = "🔄 Reactivation campaigns, special offers"
            elif not r_recent and f_high and not m_high:
                name = "Need Attention"
                desc = "Active but low spending, declining"
                strategy = "❓ Check satisfaction, special promotions"
            elif r_recent and not f_high and not m_high:
                name = "New Customers"
                desc = "Recent, low frequency, low value"
                strategy = "👋 Welcome campaigns, education, onboarding"
            else:
                name = "Lost"
                desc = "No recent purchases"
                strategy = "📣 Re-engagement campaigns, surveys, incentives"
            
            segments.append({
                'cluster': int(cluster_id),
                'name': name,
                'description': desc,
                'strategy': strategy,
                'count': count,
                'percentage': f"{percentage:.1f}%",
                'avg_recency': f"{r_mean:.1f}",
                'avg_frequency': f"{f_mean:.1f}",
                'avg_spending': f"${m_mean:.2f}"
            })
        
        cached_data['interpretations'] = segments
        
        return jsonify({
            'success': True,
            'segments': segments
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/export-csv', methods=['GET'])
def export_csv():
    """Export results as CSV."""
    try:
        if cached_data['clustered_df'] is None:
            return jsonify({'error': 'No analysis results'}), 400
        
        df = cached_data['clustered_df']
        
        # Create CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # Return CSV
        return df.to_csv(index=False), 200, {
            'Content-Disposition': 'attachment; filename=customer_segments.csv',
            'Content-Type': 'text/csv'
        }
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/export-json', methods=['GET'])
def export_json():
    """Export results as JSON."""
    try:
        if cached_data['interpretations'] is None:
            return jsonify({'error': 'No analysis results'}), 400
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'segments': cached_data['interpretations']
        }
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/status', methods=['GET'])
def status():
    """Get current analysis status."""
    return jsonify({
        'has_data': cached_data['df'] is not None,
        'has_rfm': cached_data['rfm_df'] is not None,
        'has_clustering': cached_data['clustered_df'] is not None,
        'has_interpretation': cached_data['interpretations'] is not None
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("CORPORATE ANALYTICS DASHBOARD")
    print("="*60)
    print("\nStarting server on http://localhost:5000")
    print("\nPress CTRL+C to stop\n")
    
    app.run(debug=True, port=5000, use_reloader=False)
