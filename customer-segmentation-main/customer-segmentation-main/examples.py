"""
Advanced Examples and Use Cases
Demonstrates various ways to use the customer segmentation system
"""

def example_1_basic_pipeline():
    """Example 1: Run the complete pipeline with default settings."""
    from src.main_pipeline import SegmentationPipeline
    
    print("=" * 60)
    print("EXAMPLE 1: Basic Pipeline Execution")
    print("=" * 60)
    
    pipeline = SegmentationPipeline(use_sample=True)
    results = pipeline.run_full_pipeline(n_clusters=4, output_dir='outputs')
    
    return results


def example_2_custom_data():
    """Example 2: Run analysis on custom data."""
    from src.main_pipeline import SegmentationPipeline
    import pandas as pd
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Custom Data Analysis")
    print("=" * 60)
    
    # Load your data
    # df = pd.read_csv('data/your_data.csv')
    
    pipeline = SegmentationPipeline(use_sample=True)  # Use sample for demo
    
    # Run analysis
    results = pipeline.run_full_pipeline(n_clusters=5, output_dir='outputs_custom')
    
    # Access specific results
    print(f"RFM Statistics: {results['rfm_stats']}")
    print(f"Silhouette Score: {results['evaluation']['silhouette_score']}")


def example_3_compare_algorithms():
    """Example 3: Compare K-Means with DBSCAN."""
    from src.main_pipeline import SegmentationPipeline, DataPreprocessor
    from src.rfm_analysis import RFMAnalysis
    from src.clustering import ClusteringEngine
    
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Comparing Clustering Algorithms")
    print("=" * 60)
    
    # Load data
    df = DataPreprocessor.load_sample_data()
    df = DataPreprocessor.clean_data(df, verbose=False)
    
    # RFM Analysis
    rfm_analyzer = RFMAnalysis(df)
    rfm_df = rfm_analyzer.calculate_rfm()
    
    print("\nK-MEANS CLUSTERING:")
    print("-" * 60)
    
    # K-Means
    clusterer_km = ClusteringEngine(rfm_df.copy())
    clusterer_km.scale_data()
    kmeans_result = clusterer_km.apply_kmeans(n_clusters=4)
    kmeans_metrics = clusterer_km.get_evaluation_metrics()
    
    print(f"Silhouette Score: {kmeans_metrics['silhouette_score']:.4f}")
    print(f"Davies-Bouldin Score: {kmeans_metrics['davies_bouldin_score']:.4f}")
    print(f"Number of Clusters: {kmeans_metrics['n_clusters']}")
    
    print("\nDBSCAN CLUSTERING:")
    print("-" * 60)
    
    # DBSCAN
    clusterer_db = ClusteringEngine(rfm_df.copy())
    clusterer_db.scale_data()
    dbscan_result = clusterer_db.apply_dbscan(eps=0.8, min_samples=5)
    dbscan_metrics = clusterer_db.get_evaluation_metrics()
    
    print(f"Silhouette Score: {dbscan_metrics['silhouette_score']:.4f}")
    print(f"Davies-Bouldin Score: {dbscan_metrics['davies_bouldin_score']:.4f}")
    print(f"Number of Clusters: {dbscan_metrics['n_clusters']}")
    print(f"Noise Points: {dbscan_metrics['n_noise_points']}")
    
    print("\nRECOMMENDATION:")
    if kmeans_metrics['silhouette_score'] > dbscan_metrics['silhouette_score']:
        print("✓ K-Means performs better for this dataset")
    else:
        print("✓ DBSCAN performs better for this dataset")


def example_4_find_optimal_k():
    """Example 4: Detailed analysis to find optimal K."""
    from src.main_pipeline import DataPreprocessor
    from src.rfm_analysis import RFMAnalysis
    from src.clustering import ClusteringEngine
    import pandas as pd
    
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Finding Optimal K Value")
    print("=" * 60)
    
    # Prepare data
    df = DataPreprocessor.load_sample_data()
    df = DataPreprocessor.clean_data(df, verbose=False)
    
    rfm_analyzer = RFMAnalysis(df)
    rfm_df = rfm_analyzer.calculate_rfm()
    
    # Run optimization
    clusterer = ClusteringEngine(rfm_df)
    clusterer.scale_data()
    optimization = clusterer.find_optimal_clusters(max_k=10)
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'K': optimization['k_range'],
        'Inertia': optimization['inertia'],
        'Silhouette': optimization['silhouette']
    })
    
    print("\nCluster Optimization Results:")
    print(results_df.to_string(index=False))
    
    # Find best k by Silhouette Score
    best_k = results_df.loc[results_df['Silhouette'].idxmax(), 'K']
    print(f"\n✓ Optimal K (by Silhouette): {int(best_k)}")


def example_5_segment_analysis():
    """Example 5: Detailed segment analysis and interpretations."""
    from src.main_pipeline import SegmentationPipeline
    
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Detailed Segment Analysis")
    print("=" * 60)
    
    pipeline = SegmentationPipeline(use_sample=True)
    pipeline.load_data()
    pipeline.perform_rfm_analysis()
    pipeline.apply_clustering(n_clusters=4)
    interpretations = pipeline.interpret_segments()
    
    print("\nSegment Summary:")
    print(interpretations[['segment', 'count', 'percentage', 'avg_monetary', 'strategy']].to_string(index=False))


def example_6_customer_scoring():
    """Example 6: Score individual customers using RFM."""
    from src.main_pipeline import DataPreprocessor
    from src.rfm_analysis import RFMAnalysis
    import pandas as pd
    
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Customer Scoring")
    print("=" * 60)
    
    df = DataPreprocessor.load_sample_data()
    df = DataPreprocessor.clean_data(df, verbose=False)
    
    rfm_analyzer = RFMAnalysis(df)
    rfm_scored = rfm_analyzer.assign_rfm_scores(q=4)
    
    print("\nTop 10 Customers by RFM Score:")
    top_customers = rfm_scored.nlargest(10, 'RFM_Score')[
        ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score']
    ]
    print(top_customers.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("Segment Distribution:")
    segmented = rfm_analyzer.segment_by_percentile()
    print(segmented['Segment'].value_counts().to_string())


def example_7_predictions():
    """Example 7: Make predictions on new customers."""
    from src.clustering import ClusteringEngine
    from src.main_pipeline import DataPreprocessor
    from src.rfm_analysis import RFMAnalysis
    import numpy as np
    
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Predicting Cluster for New Customers")
    print("=" * 60)
    
    # Train on existing data
    df = DataPreprocessor.load_sample_data()
    df = DataPreprocessor.clean_data(df, verbose=False)
    
    rfm_analyzer = RFMAnalysis(df)
    rfm_df = rfm_analyzer.calculate_rfm()
    
    clusterer = ClusteringEngine(rfm_df)
    clusterer.scale_data()
    model = clusterer.apply_kmeans(n_clusters=4)
    
    # Simulate new customer RFM values
    new_customer_rfm = np.array([[30, 8, 500]])  # [Recency, Frequency, Monetary]
    
    # Scale using the fitted scaler
    new_customer_scaled = clusterer.scaler.transform(new_customer_rfm)
    
    # Predict cluster
    predicted_cluster = clusterer.model.predict(new_customer_scaled)[0]
    
    print(f"\nNew Customer RFM:")
    print(f"  Recency: 30 days")
    print(f"  Frequency: 8 purchases")
    print(f"  Monetary: $500")
    print(f"\n✓ Predicted Cluster: {predicted_cluster}")
    print(f"✓ This customer is most similar to cluster {predicted_cluster}")


def example_8_export_formats():
    """Example 8: Export results in various formats."""
    from src.main_pipeline import SegmentationPipeline
    import json
    
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Exporting Results")
    print("=" * 60)
    
    pipeline = SegmentationPipeline(use_sample=True)
    results = pipeline.run_full_pipeline(n_clusters=4, output_dir='outputs_example8')
    
    print("\nGenerated Files:")
    print("✓ outputs_example8/rfm_analysis.csv")
    print("✓ outputs_example8/clustered_customers.csv")
    print("✓ outputs_example8/segment_interpretations.csv")
    print("✓ outputs_example8/analysis_report.json")
    print("✓ outputs_example8/[5 visualization PNG files]")
    
    # Example: Access JSON report
    with open('outputs_example8/analysis_report.json', 'r') as f:
        report = json.load(f)
        print(f"\nReport Summary:")
        print(f"  Total Customers: {report['total_customers']}")
        print(f"  Analysis Timestamp: {report['timestamp']}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CUSTOMER SEGMENTATION - EXAMPLES")
    print("=" * 60)
    
    # Run examples
    # Uncomment to run specific examples
    
    example_1_basic_pipeline()
    # example_2_custom_data()
    # example_3_compare_algorithms()
    # example_4_find_optimal_k()
    # example_5_segment_analysis()
    # example_6_customer_scoring()
    # example_7_predictions()
    # example_8_export_formats()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
