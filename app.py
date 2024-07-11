import streamlit as st
import pandas as pd
from process import load_and_process_data
from validate import validate_data
from analytics import perform_analytics
from visual import create_visualizations
from report_gen import generate_text_report, save_text_report
from report import chat_with_llm, generate_report

def main():
    st.set_page_config(page_title="Billing Audit Dashboard", layout="wide")
    
    st.title("🧾Billing Audit Dashboard")
    
    # Load and process data
    df = load_and_process_data('data.csv')
    
    # Validate data
    validation_results = validate_data(df)
    
    # Perform analytics
    analytics_results = perform_analytics(df)
    
    # Create visualizations
    visualizations = create_visualizations(df, analytics_results)
    
    # Sidebar for filtering
    st.sidebar.header("Filters")
    selected_department = st.sidebar.multiselect("Select Department", options=df['Department'].unique())
    date_range = st.sidebar.date_input("Select Date Range", [df['Billing Date'].min(), df['Billing Date'].max()])
    
    # Filter data based on selections
    filtered_df = df[
        (df['Department'].isin(selected_department) if selected_department else True) &
        (df['Billing Date'].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])))
    ]
    
    # Chat with AI Analyst
    st.subheader("💬 Chat with  Analytics")
    user_query = st.text_input("Ask a question about the billing data analysis:")
    if user_query:
        ai_response = chat_with_llm(user_query, df, analytics_results)
        st.markdown(ai_response)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Billing", f"${filtered_df['Amount'].sum():,.2f}")
    col2.metric("Avg. Transaction", f"${filtered_df['Amount'].mean():,.2f}")
    col3.metric("Unique Customers", filtered_df['Account ID'].nunique())
    col4.metric("Anomalies", len(analytics_results['anomalies']))
    
    # Visualizations
    st.subheader("Billing Trend")
    st.plotly_chart(visualizations['trend'], use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Department-wise Billing")
        st.plotly_chart(visualizations['department'], use_container_width=True)
    with col2:
        st.subheader("Customer Segmentation")
        st.plotly_chart(visualizations['segments'], use_container_width=True)
    
    st.subheader("Anomaly Detection")
    st.plotly_chart(visualizations['anomalies'], use_container_width=True)
    
    st.subheader("Monthly Billing Distribution")
    st.plotly_chart(visualizations['monthly_distribution'], use_container_width=True)
    
    st.subheader("Customer Loyalty vs Billing Amount")
    st.plotly_chart(visualizations['customer_loyalty'], use_container_width=True)
    
    st.subheader("Day of Week Analysis")
    st.plotly_chart(visualizations['day_of_week'], use_container_width=True)
    
    # Generate and save text report
    st.subheader("📊 Generate Comprehensive Text Report")
    if st.button("Generate Text Report"):
        st.info("Generating report, please wait...")
        ai_insights = chat_with_llm("Provide insights for report", filtered_df, analytics_results)  # Example query
        text_report = generate_text_report(filtered_df, analytics_results,  ai_insights)
        filename = "billing_audit_report.txt"  # Use .md extension for Markdown
        save_text_report(text_report, filename)
        st.success("Report generated successfully!")
        st.download_button(
            label="Download Text Report",
            data=open(filename, "rb").read(),
            file_name=filename,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
