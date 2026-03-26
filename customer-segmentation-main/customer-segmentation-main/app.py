"""
Streamlit dashboard for customer segmentation.
Converted from the Flask HTML dashboard so it can run on Streamlit Cloud.
"""

from __future__ import annotations

import json
import sys
from io import BytesIO, StringIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from clustering import ClusteringEngine
from data_loader import DataLoader
from rfm_analysis import RFMAnalysis
from main_pipeline import DataPreprocessor


st.set_page_config(
    page_title="Corporate Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(132, 90, 223, 0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(69, 142, 255, 0.18), transparent 24%),
                linear-gradient(180deg, #eef2ff 0%, #f8fbff 35%, #ffffff 100%);
        }
        .hero-card {
            background: white;
            padding: 1.6rem 1.8rem;
            border-radius: 20px;
            border-left: 8px solid #5b63f6;
            box-shadow: 0 14px 30px rgba(44, 62, 120, 0.10);
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2.3rem;
            font-weight: 800;
            color: #243b74;
            margin: 0;
        }
        .hero-subtitle {
            color: #5d6785;
            margin-top: 0.35rem;
            font-size: 1rem;
        }
        .step-card {
            background: white;
            border-radius: 18px;
            padding: 1.2rem 1.2rem 1rem 1.2rem;
            box-shadow: 0 10px 24px rgba(44, 62, 120, 0.08);
            border: 1px solid rgba(91, 99, 246, 0.10);
            margin-bottom: 1rem;
        }
        .step-title {
            color: #31457a;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .step-text {
            color: #667085;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }
        .metric-band {
            background: linear-gradient(135deg, #5b63f6 0%, #7c4dff 100%);
            color: white;
            padding: 1rem 1.1rem;
            border-radius: 16px;
            min-height: 112px;
            box-shadow: 0 10px 20px rgba(91, 99, 246, 0.20);
        }
        .metric-band-label {
            font-size: 0.85rem;
            opacity: 0.9;
            margin-bottom: 0.6rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .metric-band-value {
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1.1;
        }
        .segment-box {
            background: white;
            border-radius: 18px;
            padding: 1rem 1.1rem;
            border-left: 6px solid #5b63f6;
            box-shadow: 0 10px 24px rgba(44, 62, 120, 0.08);
            margin-bottom: 1rem;
        }
        .segment-name {
            font-size: 1.15rem;
            font-weight: 800;
            color: #31457a;
        }
        .segment-meta {
            color: #667085;
            margin-top: 0.35rem;
            margin-bottom: 0.55rem;
        }
        .segment-strategy {
            background: #f5f7ff;
            color: #30406c;
            border-radius: 12px;
            padding: 0.7rem 0.85rem;
            margin-top: 0.6rem;
        }
        .small-note {
            color: #667085;
            font-size: 0.9rem;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f3f6ff 0%, #e9efff 100%);
            border-right: 1px solid rgba(49, 69, 122, 0.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    defaults = {
        "df": None,
        "rfm_df": None,
        "rfm_stats": None,
        "clustered_df": None,
        "cluster_profiles": None,
        "optimization": None,
        "evaluation": None,
        "interpretations": None,
        "source_label": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_analysis_state(keep_df: bool = True) -> None:
    preserved_df = st.session_state.df if keep_df else None
    preserved_source = st.session_state.source_label if keep_df else None
    st.session_state.rfm_df = None
    st.session_state.rfm_stats = None
    st.session_state.clustered_df = None
    st.session_state.cluster_profiles = None
    st.session_state.optimization = None
    st.session_state.evaluation = None
    st.session_state.interpretations = None
    if not keep_df:
        st.session_state.df = None
        st.session_state.source_label = None
    else:
        st.session_state.df = preserved_df
        st.session_state.source_label = preserved_source


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(uploaded_file)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Upload CSV, XLSX, or XLS.")

    df = DataLoader.standardize_columns(df)
    required_columns = ["InvoiceID", "CustomerID", "InvoiceDate", "Quantity", "UnitPrice"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return DataPreprocessor.clean_data(df, verbose=False)


@st.cache_data(show_spinner=False)
def get_sample_data() -> pd.DataFrame:
    df = DataPreprocessor.load_sample_data()
    return DataPreprocessor.clean_data(df, verbose=False)


def run_rfm_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    analyzer = RFMAnalysis(df)
    rfm_df = analyzer.calculate_rfm()
    stats = analyzer.get_statistics()
    return rfm_df, stats


def run_clustering(rfm_df: pd.DataFrame, n_clusters: int):
    if len(rfm_df) < 3:
        raise ValueError("Need at least 3 customers for clustering.")

    safe_max_k = max(2, min(10, len(rfm_df) - 1))
    n_clusters = max(2, min(n_clusters, safe_max_k))

    clusterer = ClusteringEngine(rfm_df)
    clusterer.scale_data()
    optimization = clusterer.find_optimal_clusters(max_k=safe_max_k)
    clustered_df = clusterer.apply_kmeans(n_clusters=n_clusters)
    clusterer.apply_pca(n_components=2)
    evaluation = clusterer.get_evaluation_metrics()
    cluster_profiles = clusterer.get_cluster_profiles(clustered_df)

    return clustered_df, optimization, evaluation, cluster_profiles, clusterer


def interpret_segments(rfm_df: pd.DataFrame, clustered_df: pd.DataFrame, cluster_profiles: pd.DataFrame):
    segments = []
    r_median = rfm_df["Recency"].median()
    f_median = rfm_df["Frequency"].median()
    m_median = rfm_df["Monetary"].median()

    for cluster_id in sorted(clustered_df["Cluster"].unique()):
        if cluster_id == -1:
            continue

        cluster_data = clustered_df[clustered_df["Cluster"] == cluster_id]
        row = cluster_profiles.loc[cluster_id]

        r_mean = row["Recency_mean"]
        f_mean = row["Frequency_mean"]
        m_mean = row["Monetary_mean"]

        r_recent = r_mean < r_median
        f_high = f_mean > f_median
        m_high = m_mean > m_median

        if r_recent and f_high and m_high:
            name = "Champions"
            description = "Best customers: recent, frequent, and high value."
            strategy = "Reward loyalty with VIP treatment, exclusives, and early access."
        elif not r_recent and f_high and m_high:
            name = "Loyal Customers"
            description = "Historically valuable customers who have gone quiet recently."
            strategy = "Run win-back campaigns with personalized reminders and premium offers."
        elif r_recent and not f_high and m_high:
            name = "Big Spenders"
            description = "Customers making large recent purchases but buying less often."
            strategy = "Promote premium bundles, cross-sells, and concierge-style recommendations."
        elif r_recent and f_high and not m_high:
            name = "At Risk"
            description = "Engaged customers with weaker spend who may drift away."
            strategy = "Increase engagement through upsell paths, loyalty nudges, and value bundles."
        elif not r_recent and not f_high and m_high:
            name = "Potential Loyalists"
            description = "High-value customers who are currently disengaged."
            strategy = "Use reactivation offers and tailored campaigns to rebuild momentum."
        elif not r_recent and f_high and not m_high:
            name = "Need Attention"
            description = "Active customers with modest spend and declining quality signals."
            strategy = "Check satisfaction, remove friction, and test targeted incentives."
        elif r_recent and not f_high and not m_high:
            name = "New Customers"
            description = "Recently acquired customers with low purchase history."
            strategy = "Focus on onboarding, education, and a strong second-purchase journey."
        else:
            name = "Lost"
            description = "Customers with low recent engagement across the board."
            strategy = "Try re-engagement campaigns, surveys, or sunset them from high-cost channels."

        count = len(cluster_data)
        percentage = (count / len(clustered_df)) * 100

        segments.append(
            {
                "cluster": int(cluster_id),
                "name": name,
                "description": description,
                "strategy": strategy,
                "count": int(count),
                "percentage": percentage,
                "avg_recency": float(r_mean),
                "avg_frequency": float(f_mean),
                "avg_spending": float(m_mean),
            }
        )

    return segments


def metric_band(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-band">
            <div class="metric-band-label">{label}</div>
            <div class="metric-band-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">📊 Corporate Analytics Dashboard</div>
            <div class="hero-subtitle">
                Advanced customer segmentation, RFM analysis, cluster optimization, and export-ready insights.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> int:
    st.sidebar.markdown("## Configuration")
    data_source = st.sidebar.radio(
        "Select Data Source:",
        ["Use Sample Data", "Upload CSV or Excel"],
    )

    if data_source == "Use Sample Data":
        st.sidebar.info("Loads a built-in retail dataset with 500 customers and 5000 transactions.")
        if st.sidebar.button("Load Sample Dataset", use_container_width=True):
            with st.spinner("Loading sample dataset..."):
                st.session_state.df = get_sample_data()
                st.session_state.source_label = "Sample retail dataset"
                reset_analysis_state(keep_df=True)
            st.sidebar.success("Sample dataset loaded.")
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload CSV, XLSX, or XLS",
            type=["csv", "xlsx", "xls"],
            help="Required columns: CustomerID, InvoiceDate, Quantity, UnitPrice, InvoiceID",
        )
        if uploaded_file is not None:
            if st.sidebar.button("Load Uploaded File", use_container_width=True):
                try:
                    with st.spinner("Uploading and cleaning data..."):
                        st.session_state.df = load_uploaded_data(uploaded_file)
                        st.session_state.source_label = uploaded_file.name
                        reset_analysis_state(keep_df=True)
                    st.sidebar.success(f"{uploaded_file.name} loaded successfully.")
                except Exception as exc:
                    st.sidebar.error(str(exc))

    n_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=4)

    if st.session_state.df is not None:
        df = st.session_state.df
        st.sidebar.markdown("### Dataset Status")
        st.sidebar.write(f"Source: `{st.session_state.source_label}`")
        st.sidebar.write(f"Transactions: `{len(df):,}`")
        st.sidebar.write(f"Customers: `{df['CustomerID'].nunique():,}`")
        st.sidebar.write(
            f"Date Range: `{df['InvoiceDate'].min().date()}` to `{df['InvoiceDate'].max().date()}`"
        )

    return n_clusters


def render_step_controls(n_clusters: int) -> None:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Step 1: RFM Analysis</div>
                <div class="step-text">Calculate recency, frequency, monetary metrics and summary statistics.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Analyze RFM Metrics", use_container_width=True, type="primary"):
            if st.session_state.df is None:
                st.error("Load a dataset first.")
            else:
                with st.spinner("Running RFM analysis..."):
                    rfm_df, stats = run_rfm_analysis(st.session_state.df)
                    st.session_state.rfm_df = rfm_df
                    st.session_state.rfm_stats = stats
                    st.session_state.clustered_df = None
                    st.session_state.cluster_profiles = None
                    st.session_state.optimization = None
                    st.session_state.evaluation = None
                    st.session_state.interpretations = None
                st.success("RFM analysis complete.")

    with col2:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Step 2: Clustering & Interpretation</div>
                <div class="step-text">Optimize clusters, evaluate quality, and generate business-ready segment narratives.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start Clustering", use_container_width=True):
            if st.session_state.rfm_df is None:
                st.error("Run RFM analysis first.")
            else:
                try:
                    with st.spinner("Clustering customers..."):
                        clustered_df, optimization, evaluation, cluster_profiles, _ = run_clustering(
                            st.session_state.rfm_df, n_clusters
                        )
                        st.session_state.clustered_df = clustered_df
                        st.session_state.optimization = optimization
                        st.session_state.evaluation = evaluation
                        st.session_state.cluster_profiles = cluster_profiles
                        st.session_state.interpretations = interpret_segments(
                            st.session_state.rfm_df,
                            clustered_df,
                            cluster_profiles,
                        )
                    st.success("Clustering complete.")
                except Exception as exc:
                    st.error(str(exc))


def render_rfm_tab() -> None:
    st.subheader("RFM Analysis")
    if st.session_state.rfm_df is None:
        st.info("Run Step 1 to generate RFM metrics.")
        return

    stats = st.session_state.rfm_stats
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_band("Total Customers", f"{stats['total_customers']:,}")
    with m2:
        metric_band("Total Revenue", f"${stats['total_revenue']:,.2f}")
    with m3:
        metric_band("Avg Recency", f"{stats['recency_mean']:.1f} days")
    with m4:
        metric_band("Avg Frequency", f"{stats['frequency_mean']:.1f}")

    m5, m6 = st.columns(2)
    with m5:
        metric_band("Median Recency", f"{stats['recency_median']:.1f} days")
    with m6:
        metric_band("Avg Spending", f"${stats['monetary_mean']:.2f}")

    st.markdown("### RFM Distribution")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    rfm_df = st.session_state.rfm_df

    axes[0, 0].hist(rfm_df["Recency"], bins=40, color="#7bc6f6", edgecolor="black")
    axes[0, 0].set_title("Recency Distribution")

    axes[0, 1].hist(rfm_df["Frequency"], bins=40, color="#ff8b8b", edgecolor="black")
    axes[0, 1].set_title("Frequency Distribution")

    axes[1, 0].hist(rfm_df["Monetary"], bins=40, color="#8fe3b6", edgecolor="black")
    axes[1, 0].set_title("Monetary Distribution")

    axes[1, 1].boxplot(
        [rfm_df["Recency"], rfm_df["Frequency"], rfm_df["Monetary"]],
        tick_labels=["Recency", "Frequency", "Monetary"],
    )
    axes[1, 1].set_title("RFM Box Plot")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("### Data Preview")
    st.dataframe(rfm_df.head(15), use_container_width=True)


def render_optimization_tab() -> None:
    st.subheader("Optimization & Metrics")
    if st.session_state.clustered_df is None:
        st.info("Run Step 2 to generate clustering results.")
        return

    optimization = st.session_state.optimization
    evaluation = st.session_state.evaluation

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(optimization["k_range"], optimization["inertia"], marker="o", color="#5b63f6")
        ax.set_title("Elbow Method")
        ax.set_xlabel("Number of Clusters")
        ax.set_ylabel("Inertia")
        ax.grid(True, alpha=0.25)
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(optimization["k_range"], optimization["silhouette"], marker="o", color="#7c4dff")
        ax.set_title("Silhouette Trend")
        ax.set_xlabel("Number of Clusters")
        ax.set_ylabel("Silhouette Score")
        ax.grid(True, alpha=0.25)
        st.pyplot(fig)

    m1, m2, m3 = st.columns(3)
    with m1:
        metric_band("Silhouette Score", f"{evaluation.get('silhouette_score', 0) or 0:.4f}")
    with m2:
        metric_band("Davies-Bouldin", f"{evaluation.get('davies_bouldin_score', 0) or 0:.4f}")
    with m3:
        metric_band("Calinski-Harabasz", f"{evaluation.get('calinski_harabasz_score', 0) or 0:.1f}")

    st.markdown("### Cluster Profiles")
    st.dataframe(st.session_state.cluster_profiles, use_container_width=True)


def render_segments_tab() -> None:
    st.subheader("Customer Segments & Strategies")
    if st.session_state.interpretations is None:
        st.info("Run Step 2 to generate segment interpretations.")
        return

    for segment in st.session_state.interpretations:
        st.markdown(
            f"""
            <div class="segment-box">
                <div class="segment-name">Cluster {segment['cluster']}: {segment['name']}</div>
                <div class="segment-meta">
                    {segment['count']} customers • {segment['percentage']:.1f}% of base
                </div>
                <div>{segment['description']}</div>
                <div class="segment-strategy"><strong>Strategy:</strong> {segment['strategy']}</div>
                <div class="small-note">
                    Avg Recency: {segment['avg_recency']:.1f} days |
                    Avg Frequency: {segment['avg_frequency']:.1f} purchases |
                    Avg Spending: ${segment['avg_spending']:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_visualization_tab(n_clusters: int) -> None:
    st.subheader("Visual Analytics")
    if st.session_state.clustered_df is None:
        st.info("Run Step 2 to unlock visual analytics.")
        return

    clustered_df, _, _, cluster_profiles, clusterer = run_clustering(st.session_state.rfm_df, n_clusters)

    fig, ax = plt.subplots(figsize=(10, 6))
    pca_data = clusterer.pca_data
    labels = clustered_df["Cluster"].values
    scatter = ax.scatter(
        pca_data[:, 0],
        pca_data[:, 1],
        c=labels,
        cmap="viridis",
        s=90,
        alpha=0.75,
        edgecolors="black",
        linewidths=0.4,
    )
    ax.set_title("Customer Clusters in PCA Space")
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    ax.grid(True, alpha=0.2)
    plt.colorbar(scatter, ax=ax, label="Cluster")
    st.pyplot(fig)

    left, right = st.columns(2)
    with left:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        counts = clustered_df["Cluster"].value_counts().sort_index()
        counts.plot(kind="bar", color="#7bc6f6", edgecolor="black", ax=ax)
        ax.set_title("Cluster Size Distribution")
        ax.set_xlabel("Cluster")
        ax.set_ylabel("Customers")
        ax.grid(True, axis="y", alpha=0.2)
        st.pyplot(fig)

    with right:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.heatmap(
            cluster_profiles[[c for c in cluster_profiles.columns if c.endswith("_mean")]],
            annot=True,
            fmt=".1f",
            cmap="Blues",
            ax=ax,
        )
        ax.set_title("Cluster Profile Heatmap")
        st.pyplot(fig)


def render_export_tab() -> None:
    st.subheader("Export Results")
    if st.session_state.clustered_df is None:
        st.info("Run clustering before exporting results.")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            label="Download RFM CSV",
            data=st.session_state.rfm_df.to_csv(index=False),
            file_name="rfm_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            label="Download Clustered CSV",
            data=st.session_state.clustered_df.to_csv(index=False),
            file_name="customer_segments.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c3:
        payload = {
            "source": st.session_state.source_label,
            "segments": st.session_state.interpretations,
        }
        st.download_button(
            label="Download Segments JSON",
            data=json.dumps(payload, indent=2),
            file_name="customer_segments.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("### Results Preview")
    st.dataframe(st.session_state.clustered_df.head(20), use_container_width=True)


def main() -> None:
    inject_styles()
    init_state()
    n_clusters = render_sidebar()
    render_hero()
    render_step_controls(n_clusters)

    if st.session_state.df is None:
        st.info("Load sample data or upload your file from the sidebar to begin.")
        return

    tabs = st.tabs(["RFM Analysis", "Optimization", "Segments", "Visualization", "Export"])
    with tabs[0]:
        render_rfm_tab()
    with tabs[1]:
        render_optimization_tab()
    with tabs[2]:
        render_segments_tab()
    with tabs[3]:
        render_visualization_tab(n_clusters)
    with tabs[4]:
        render_export_tab()


if __name__ == "__main__":
    main()
