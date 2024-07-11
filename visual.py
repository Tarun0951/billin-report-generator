import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy import stats

def create_visualizations(df, analytics_results):
    # 1. Billing Trend Over Time
    fig_trend = px.line(df, x='Billing Date', y='Amount', title='Billing Trend Over Time')
    fig_trend.add_trace(px.line(df.resample('W', on='Billing Date')['Amount'].mean().reset_index(), 
                                x='Billing Date', y='Amount', line_shape='spline').data[0])
    fig_trend.update_layout(legend_title_text='Trend')
    fig_trend.data[0].name = 'Daily'
    fig_trend.data[1].name = 'Weekly Average'

    # 2. Department-wise Billing
    dept_data = df.groupby('Department')['Amount'].agg(['sum', 'mean', 'count']).reset_index()
    dept_data.columns = ['Department', 'Total Amount', 'Average Amount', 'Transaction Count']
    fig_dept = px.sunburst(dept_data, path=['Department'], values='Total Amount', 
                           color='Average Amount', hover_data=['Transaction Count'],
                           title='Department-wise Billing Analysis')

    # 3. Customer Segmentation
    df['Is_Repeat_Customer_Filled'] = df['Is_Repeat_Customer'].fillna(0) + 1
    
    fig_segments = px.scatter(df, x='Amount', y='30_Day_Avg', color='Customer_Segment',
                              size='Is_Repeat_Customer_Filled', hover_data=['Account ID'],
                              title='Customer Segmentation Analysis')
    fig_segments.update_layout(legend_title_text='Customer Segment')

    # 4. Anomaly Detection
    fig_anomalies = px.scatter(df, x='Billing Date', y='Amount', color='Amount_Zscore',
                               hover_data=['Account ID', 'Department'],
                               title='Anomaly Detection in Billing')
    fig_anomalies.add_hline(y=df['Amount'].mean() + 2*df['Amount'].std(), line_dash="dash", line_color="red",
                            annotation_text="2 Std Dev above Mean")
    fig_anomalies.add_hline(y=df['Amount'].mean() - 2*df['Amount'].std(), line_dash="dash", line_color="red",
                            annotation_text="2 Std Dev below Mean")

    
    

    # 6. Monthly Billing Distribution
    df['Month'] = df['Billing Date'].dt.to_period('M')
    monthly_stats = df.groupby('Month')['Amount'].agg(['mean', 'median', 'std']).reset_index()
    monthly_stats['Month'] = monthly_stats['Month'].astype(str)
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(x=monthly_stats['Month'], y=monthly_stats['mean'], name='Mean'))
    fig_monthly.add_trace(go.Bar(x=monthly_stats['Month'], y=monthly_stats['median'], name='Median'))
    fig_monthly.add_trace(go.Scatter(x=monthly_stats['Month'], y=monthly_stats['std'], name='Std Dev', yaxis='y2'))
    fig_monthly.update_layout(title='Monthly Billing Distribution',
                              yaxis_title='Amount', yaxis2=dict(overlaying='y', side='right', title='Standard Deviation'))

    # 7. Customer Loyalty vs Billing Amount
    df['Loyalty_Score'] = df.groupby('Account ID')['Billing Date'].transform(lambda x: (x.max() - x.min()).days)
    fig_loyalty = px.scatter(df, x='Loyalty_Score', y='Amount', color='Customer_Segment',
                             hover_data=['Account ID', 'Department'],
                             title='Customer Loyalty vs Billing Amount')
    fig_loyalty.update_layout(xaxis_title='Customer Loyalty (days)', yaxis_title='Billing Amount')

    # 8. Day of Week Analysis
    dow_stats = df.groupby('Day of Week')['Amount'].agg(['mean', 'count']).reset_index()
    fig_dow = make_subplots(specs=[[{"secondary_y": True}]])
    fig_dow.add_trace(go.Bar(x=dow_stats['Day of Week'], y=dow_stats['mean'], name='Average Amount'))
    fig_dow.add_trace(go.Scatter(x=dow_stats['Day of Week'], y=dow_stats['count'], name='Transaction Count', line=dict(color='red')), secondary_y=True)
    fig_dow.update_layout(title='Day of Week Analysis', xaxis_title='Day of Week',
                          yaxis_title='Average Amount', yaxis2_title='Transaction Count')

    return {
        'trend': fig_trend,
        'department': fig_dept,
        'segments': fig_segments,
        'anomalies': fig_anomalies,
       
        'monthly_distribution': fig_monthly,
        'customer_loyalty': fig_loyalty,
        'day_of_week': fig_dow
    }