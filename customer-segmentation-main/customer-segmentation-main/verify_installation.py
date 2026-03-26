"""
Verification and Testing Script
Tests all components of the customer segmentation system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_imports():
    """Test all imports work correctly."""
    print("\n" + "=" * 60)
    print("TEST 1: Verifying Imports")
    print("=" * 60)
    
    try:
        from src.rfm_analysis import RFMAnalysis
        print("✓ RFMAnalysis imported successfully")
    except Exception as e:
        print(f"✗ Failed to import RFMAnalysis: {e}")
        return False
    
    try:
        from src.clustering import ClusteringEngine
        print("✓ ClusteringEngine imported successfully")
    except Exception as e:
        print(f"✗ Failed to import ClusteringEngine: {e}")
        return False
    
    try:
        from src.visualization import Visualizer
        print("✓ Visualizer imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Visualizer: {e}")
        return False
    
    try:
        from src.main_pipeline import SegmentationPipeline, DataPreprocessor
        print("✓ SegmentationPipeline and DataPreprocessor imported successfully")
    except Exception as e:
        print(f"✗ Failed to import pipeline components: {e}")
        return False
    
    return True


def test_data_generation():
    """Test data generation."""
    print("\n" + "=" * 60)
    print("TEST 2: Data Generation")
    print("=" * 60)
    
    try:
        from src.main_pipeline import DataPreprocessor
        
        df = DataPreprocessor.load_sample_data()
        print(f"✓ Generated sample data: {len(df)} rows")
        print(f"  Customers: {df['CustomerID'].nunique()}")
        print(f"  Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
        return True
    except Exception as e:
        print(f"✗ Data generation failed: {e}")
        return False


def test_data_cleaning():
    """Test data cleaning."""
    print("\n" + "=" * 60)
    print("TEST 3: Data Cleaning")
    print("=" * 60)
    
    try:
        from src.main_pipeline import DataPreprocessor
        
        df = DataPreprocessor.load_sample_data()
        original_count = len(df)
        
        df_cleaned = DataPreprocessor.clean_data(df, verbose=False)
        cleaned_count = len(df_cleaned)
        
        print(f"✓ Data cleaning successful")
        print(f"  Original rows: {original_count}")
        print(f"  Cleaned rows: {cleaned_count}")
        print(f"  Rows removed: {original_count - cleaned_count}")
        return True
    except Exception as e:
        print(f"✗ Data cleaning failed: {e}")
        return False


def test_rfm_analysis():
    """Test RFM analysis."""
    print("\n" + "=" * 60)
    print("TEST 4: RFM Analysis")
    print("=" * 60)
    
    try:
        from src.main_pipeline import DataPreprocessor
        from src.rfm_analysis import RFMAnalysis
        
        df = DataPreprocessor.load_sample_data()
        df = DataPreprocessor.clean_data(df, verbose=False)
        
        rfm = RFMAnalysis(df)
        rfm_df = rfm.calculate_rfm()
        
        print(f"✓ RFM analysis successful")
        print(f"  RFM records: {len(rfm_df)}")
        print(f"  Recency range: {rfm_df['Recency'].min():.0f} - {rfm_df['Recency'].max():.0f} days")
        print(f"  Frequency range: {rfm_df['Frequency'].min()} - {rfm_df['Frequency'].max()}")
        print(f"  Monetary range: ${rfm_df['Monetary'].min():.2f} - ${rfm_df['Monetary'].max():.2f}")
        
        stats = rfm.get_statistics()
        print(f"  Total revenue: ${stats['total_revenue']:.2f}")
        return True
    except Exception as e:
        print(f"✗ RFM analysis failed: {e}")
        return False


def test_clustering():
    """Test clustering."""
    print("\n" + "=" * 60)
    print("TEST 5: Clustering")
    print("=" * 60)
    
    try:
        from src.main_pipeline import DataPreprocessor
        from src.rfm_analysis import RFMAnalysis
        from src.clustering import ClusteringEngine
        
        df = DataPreprocessor.load_sample_data()
        df = DataPreprocessor.clean_data(df, verbose=False)
        
        rfm = RFMAnalysis(df)
        rfm_df = rfm.calculate_rfm()
        
        clusterer = ClusteringEngine(rfm_df)
        clusterer.scale_data()
        print("✓ Data scaling successful")
        
        optimization = clusterer.find_optimal_clusters(max_k=6)
        print(f"✓ Optimization completed (tested k=2 to k=6)")
        
        clustered = clusterer.apply_kmeans(n_clusters=4)
        print(f"✓ K-Means clustering completed")
        print(f"  Clusters: {clustered['Cluster'].nunique()}")
        
        metrics = clusterer.get_evaluation_metrics()
        print(f"  Silhouette Score: {metrics['silhouette_score']:.4f}")
        print(f"  Davies-Bouldin Score: {metrics['davies_bouldin_score']:.4f}")
        
        return True
    except Exception as e:
        print(f"✗ Clustering failed: {e}")
        return False


def test_pca():
    """Test PCA visualization."""
    print("\n" + "=" * 60)
    print("TEST 6: PCA Visualization")
    print("=" * 60)
    
    try:
        from src.main_pipeline import DataPreprocessor
        from src.rfm_analysis import RFMAnalysis
        from src.clustering import ClusteringEngine
        
        df = DataPreprocessor.load_sample_data()
        df = DataPreprocessor.clean_data(df, verbose=False)
        
        rfm = RFMAnalysis(df)
        rfm_df = rfm.calculate_rfm()
        
        clusterer = ClusteringEngine(rfm_df)
        clusterer.scale_data()
        clusterer.apply_kmeans(n_clusters=4)
        
        pca_data, variance = clusterer.apply_pca(n_components=2)
        
        print(f"✓ PCA transformation successful")
        print(f"  PCA shape: {pca_data.shape}")
        print(f"  Explained variance: {variance}")
        return True
    except Exception as e:
        print(f"✗ PCA failed: {e}")
        return False


def test_pipeline():
    """Test complete pipeline."""
    print("\n" + "=" * 60)
    print("TEST 7: Complete Pipeline")
    print("=" * 60)
    
    try:
        from src.main_pipeline import SegmentationPipeline
        
        pipeline = SegmentationPipeline(use_sample=True)
        pipeline.load_data()
        print("✓ Data loaded")
        
        pipeline.perform_rfm_analysis()
        print("✓ RFM analysis completed")
        
        pipeline.apply_clustering(n_clusters=4)
        print("✓ Clustering completed")
        
        pipeline.interpret_segments()
        print("✓ Segments interpreted")
        
        return True
    except Exception as e:
        print(f"✗ Pipeline failed: {e}")
        return False


def test_file_structure():
    """Test project file structure."""
    print("\n" + "=" * 60)
    print("TEST 8: Project File Structure")
    print("=" * 60)
    
    required_files = [
        'src/rfm_analysis.py',
        'src/clustering.py',
        'src/visualization.py',
        'src/main_pipeline.py',
        'src/__init__.py',
        'app.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'API_DOCUMENTATION.md',
    ]
    
    from pathlib import Path
    project_root = Path(__file__).parent
    
    all_exist = True
    for file in required_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_exist = False
    
    required_dirs = ['src', 'data', 'outputs']
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ (directory)")
        else:
            print(f"✗ {dir_name}/ - MISSING")
            all_exist = False
    
    return all_exist


def test_dependencies():
    """Test required dependencies."""
    print("\n" + "=" * 60)
    print("TEST 9: Dependencies")
    print("=" * 60)
    
    dependencies = [
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('sklearn', 'Scikit-learn'),
        ('matplotlib', 'Matplotlib'),
        ('seaborn', 'Seaborn'),
    ]
    
    all_installed = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {display_name}")
        except ImportError:
            print(f"✗ {display_name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CUSTOMER SEGMENTATION - VERIFICATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Data Generation", test_data_generation),
        ("Data Cleaning", test_data_cleaning),
        ("RFM Analysis", test_rfm_analysis),
        ("Clustering", test_clustering),
        ("PCA Visualization", test_pca),
        ("Complete Pipeline", test_pipeline),
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} - FAILED: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python src/main_pipeline.py")
        print("2. Or run: streamlit run app.py")
        print("3. Visit: http://localhost:8501")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
