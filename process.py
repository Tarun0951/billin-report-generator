import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import timedelta

def load_and_process_data(file_path):
    df = pd.read_csv(file_path)
    df['Billing Date'] = pd.to_datetime(df['Billing Date'])
    df['Day of Week'] = df['Billing Date'].dt.day_name()
    df['Month'] = df['Billing Date'].dt.month_name()
    df['Is Weekend'] = df['Billing Date'].dt.dayofweek.isin([5, 6]).astype(int)
    
    # Handle potential NaN values in rolling averages
    df['7_Day_Avg'] = df.groupby('Account ID')['Amount'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
    df['30_Day_Avg'] = df.groupby('Account ID')['Amount'].rolling(window=30, min_periods=1).mean().reset_index(0, drop=True)
    
    # Handle potential NaN values in Is_Repeat_Customer
    df['Is_Repeat_Customer'] = df.groupby('Account ID').apply(lambda x: (x['Billing Date'].max() - x['Billing Date'].min()) > timedelta(days=30)).astype(int)
    
    scaler = StandardScaler()
    df['Amount_Scaled'] = scaler.fit_transform(df[['Amount']])
    
    return df