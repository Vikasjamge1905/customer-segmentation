"""
Main Entry Point - Choose Between Batch Processing and Web Dashboard
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    print("\n" + "="*70)
    print(" " * 15 + "CUSTOMER SEGMENTATION SYSTEM")
    print(" " * 10 + "Choose Your Interface")
    print("="*70)
    print("\n1. 🌐  WEB DASHBOARD (Interactive - Recommended)")
    print("   - Professional UI with charts")
    print("   - Real-time analysis")
    print("   - Upload custom data")
    print("   - Export results")
    print("\n2. 📊 BATCH PROCESSING (Command Line)")
    print("   - Load and process your data")
    print("   - Generate full report")
    print("   - Export to files")
    print("\n3. 🧪 TEST INSTALLATION")
    print("   - Verify all components")
    print("\n0. ❌ EXIT")
    print("\n" + "="*70)
    
    choice = input("\nSelect option (0-3): ").strip()
    
    if choice == '1':
        start_web_dashboard()
    elif choice == '2':
        start_batch_processing()
    elif choice == '3':
        run_tests()
    elif choice == '0':
        print("\n👋 Goodbye!")
        sys.exit(0)
    else:
        print("\n❌ Invalid option. Please try again.")
        main()


def start_web_dashboard():
    """Start the Flask web dashboard."""
    print("\n" + "="*70)
    print("🌐 STARTING WEB DASHBOARD")
    print("="*70)
    
    # Check if Flask is installed
    try:
        import flask
    except ImportError:
        print("\n⚠️  Flask not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "-q"])
    
    print("\n✓ Flask ready")
    print("\n🚀 Dashboard starting at http://localhost:5000")
    print("   Press CTRL+C to stop\n")
    
    from dashboard import app
    app.run(debug=True, port=5000, use_reloader=False)


def start_batch_processing():
    """Start batch processing pipeline."""
    print("\n" + "="*70)
    print("📊 BATCH PROCESSING")
    print("="*70)
    
    import pandas as pd
    from data_loader import DataLoader
    from src.main_pipeline import SegmentationPipeline
    
    print("\n1. Load Sample Data (Online Retail Dataset)")
    print("2. Load Custom Data (Excel or CSV)")
    print("0. Cancel")
    
    choice = input("\nSelect option (0-2): ").strip()
    
    if choice == '1':
        print("\nLoading sample data...")
        file_path = r'C:\Users\ASUS\Downloads\archive (1)\Online Retail.xlsx'
        
        try:
            df = DataLoader.prepare_data(file_path)
            
            print(f"\n✓ Dataset loaded:")
            print(f"  - Transactions: {len(df):,}")
            print(f"  - Customers: {df['CustomerID'].nunique():,}")
            print(f"  - Date Range: {df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}")
            
            pipeline = SegmentationPipeline()
            pipeline.df = df
            
            print("\nStarting analysis...")
            results = pipeline.run_full_pipeline(n_clusters=4, output_dir='outputs')
            
            print("\n" + "="*70)
            print("✓ ANALYSIS COMPLETE!")
            print("="*70)
            print("\nResults saved to: outputs/")
            print("\nGenerated files:")
            print("  ✓ rfm_analysis.csv")
            print("  ✓ clustered_customers.csv")
            print("  ✓ segment_interpretations.csv")
            print("  ✓ analysis_report.json")
            print("  ✓ [5 visualization PNG files]")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    elif choice == '2':
        file_path = input("\nEnter file path (CSV or Excel): ").strip()
        
        try:
            df = DataLoader.prepare_data(file_path)
            
            print(f"\n✓ Dataset loaded:")
            print(f"  - Transactions: {len(df):,}")
            print(f"  - Customers: {df['CustomerID'].nunique():,}")
            
            n_clusters = input("\nNumber of clusters (default 4): ").strip()
            n_clusters = int(n_clusters) if n_clusters else 4
            
            pipeline = SegmentationPipeline()
            pipeline.df = df
            
            print("\nStarting analysis...")
            results = pipeline.run_full_pipeline(n_clusters=n_clusters, output_dir='outputs')
            
            print("\n" + "="*70)
            print("✓ ANALYSIS COMPLETE!")
            print("="*70)
            print("\nResults saved to: outputs/")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")


def run_tests():
    """Run installation verification tests."""
    print("\n" + "="*70)
    print("🧪 TESTING INSTALLATION")
    print("="*70)
    
    import subprocess
    result = subprocess.run([sys.executable, "verify_installation.py"], cwd=Path(__file__).parent)
    sys.exit(result.returncode)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
