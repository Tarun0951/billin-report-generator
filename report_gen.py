import pandas as pd
from report import generate_report

def generate_text_report(df, analytics_results, ai_insights):
    report = []

    # Add title
    report.append("# Comprehensive Billing Audit Report")
    report.append("=" * 40)
    report.append("\n")

    # Overview and Summary Statistics
    report.append("## Overview and Summary Statistics")
    report.append("-" * 20)
    report.append(f"- **Total Billing Amount:** ${df['Amount'].sum():,.2f}")
    report.append(f"- **Number of Transactions:** {len(df)}")
    report.append(f"- **Date Range:** {df['Billing Date'].min().date()} to {df['Billing Date'].max().date()}")
    report.append(f"- **Number of Unique Customers:** {df['Account ID'].nunique()}")
    report.append(f"- **Top Department by Amount:** {df.groupby('Department')['Amount'].sum().idxmax()}")
    report.append(f"- **Pending Transactions:** {df[df['Status'] == 'Pending'].shape[0]}")
    report.append(f"- **High-Cost Transactions:** {df[df['Amount'] > df['Amount'].quantile(0.95)].shape[0]}")
    report.append(f"- **Duplicate Transactions:** {df[df.duplicated(subset=['Account ID', 'Billing Date', 'Amount'])].shape[0]}")
    report.append(f"- **Non-Standard Statuses:** {df[~df['Status'].isin(['Completed', 'Pending', 'Cancelled'])].shape[0]}")
    report.append(f"- **Different Amounts on Same Day:** {df[df.duplicated(subset=['Account ID', 'Billing Date'], keep=False)].shape[0]}")
    report.append(f"- **Unexpected Descriptions:** {df[df['Description'].str.contains('unexpected', case=False)].shape[0]}")
    report.append(f"- **Inconsistent Departments:** {df['Department'].isna().sum()}")
    report.append("\n")

    # Billing Cycle Analysis
    report.append("## Billing Cycle Analysis")
    report.append("-" * 20)
    df['Billing Date'] = pd.to_datetime(df['Billing Date'])
    avg_billing_cycle = df.groupby('Account ID')['Billing Date'].apply(lambda x: (x.max() - x.min()).days / x.nunique()).mean()
    report.append(f"### Average Billing Cycle Time")
    report.append(f"- **Average Billing Cycle Time:** {avg_billing_cycle:.2f} days")
    report.append("\n")

    # Payment Behavior Analysis
    report.append("## Payment Behavior Analysis")
    report.append("-" * 20)
    late_payments = df[df['Status'] == 'Late'].shape[0]
    overdue_payments = df[df['Status'] == 'Overdue'].shape[0]
    report.append(f"- **Late Payments:** {late_payments}")
    report.append(f"- **Overdue Payments:** {overdue_payments}")
    report.append("\n")

    # Detailed Insights from Analytics Results
    report.append("## Detailed Insights from Analytics Results")
    report.append("-" * 20)
    insights = generate_report(df, analytics_results)
    report.append(insights)
    report.append("\n")

    # AI-Generated Insights
    report.append("## AI-Generated Insights")
    report.append("-" * 20)
    report.append(f"{ai_insights}")
    report.append("\n")
    

    # Overall Insights and Recommendations
    report.append("## Overall Insights and Recommendations")
    report.append("-"*20)
    insights = generate_report(df, analytics_results)
    report.append(insights)
    report.append("\n")

    return "\n".join(report)

def save_text_report(report, filename):
    with open(filename, "w") as file:
        file.write(report)
