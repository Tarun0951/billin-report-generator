import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def generate_report(df, analytics_results):
    summary = f"""
    Dataset Summary:
    - Total Billing Amount: ${df['Amount'].sum():,.2f}
    - Number of Transactions: {len(df)}
    - Date Range: {df['Billing Date'].min().date()} to {df['Billing Date'].max().date()}
    - Number of Unique Customers: {df['Account ID'].nunique()}
    - Top Department: {df.groupby('Department')['Amount'].sum().idxmax()}
    
    Analytics Insights:
    - Anomalies Detected: {len(analytics_results['anomalies'])}
    - Customer Segments: {analytics_results['customer_segments'].to_dict()}
    - Pareto Threshold: {analytics_results['pareto_threshold']} (number of customers accounting for 80% of revenue)
    
    Please provide a comprehensive and very detailed  analysis of the billing data, including key insights, trends, and recommendations for improving the billing process and customer segmentation strategy and many more things to get deeper insights about the data.
    """
    
    response = model.generate_content(summary)
    return response.text

def chat_with_llm(query, df, analytics_results):
    context = f"""
    You are an AI assistant specializing in billing data analysis. You have access to the following information:
    
    Dataset Summary:
    - Total Billing Amount: ${df['Amount'].sum():,.2f}
    - Number of Transactions: {len(df)}
    - Date Range: {df['Billing Date'].min().date()} to {df['Billing Date'].max().date()}
    - Number of Unique Customers: {df['Account ID'].nunique()}
    - Top Department: {df.groupby('Department')['Amount'].sum().idxmax()}
    
    Analytics Insights:
    - Anomalies Detected: {len(analytics_results['anomalies'])}
    - Customer Segments: {analytics_results['customer_segments'].to_dict()}
    - Pareto Threshold: {analytics_results['pareto_threshold']} (number of customers accounting for 80% of revenue)
    
    Please answer the following query based on this information very detailed and comprehensive way for making people understand such analytics so answer anything regarding the data:
    {query}
    """
    
    response = model.generate_content(context)
    return response.text