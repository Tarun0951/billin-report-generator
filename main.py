from process import load_and_process_data
from validate import validate_data
from analytics import perform_analytics
from visual import create_visualizations
from report import generate_report, chat_with_llm
import os

def main():
    # Load and process data
    df = load_and_process_data('data.csv')
    
    # Validate data
    validation_results = validate_data(df)
    print("Data Validation Results:", validation_results)
    
    # Perform analytics
    analytics_results = perform_analytics(df)
    
    # Create visualizations
    visualizations = create_visualizations(df, analytics_results)
    
    # Generate report
    report = generate_report(df, analytics_results)
    
    # Save report
    if not os.path.exists('reports'):
        os.makedirs('reports')
    with open('reports/billing_audit_report.txt', 'w') as f:
        f.write(report)
    
    print("Billing audit completed. Report saved in reports/billing_audit_report.txt")

if __name__ == "__main__":
    main()