import numpy as np
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def perform_analytics(df):
    # Time series decomposition
    ts_decomposition = seasonal_decompose(df.set_index('Billing Date')['Amount'], model='additive', period=30)
    
    # Anomaly detection
    df['Amount_Zscore'] = np.abs(stats.zscore(df['Amount'], nan_policy='omit'))
    anomalies = df[df['Amount_Zscore'] > 3]
    
    # Customer segmentation with imputation and scaling
    segmentation_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('kmeans', KMeans(n_clusters=3, random_state=42))
    ])
    
    # Select features for segmentation
    segmentation_features = ['Amount', '30_Day_Avg', 'Is_Repeat_Customer']
    
    # Fit and predict segments
    df['Customer_Segment'] = segmentation_pipeline.fit_predict(df[segmentation_features])
    
    # Pareto analysis
    df_sorted = df.sort_values('Amount', ascending=False)
    df_sorted['Cumulative_Percentage'] = df_sorted['Amount'].cumsum() / df_sorted['Amount'].sum() * 100
    pareto_threshold = df_sorted[df_sorted['Cumulative_Percentage'] >= 80].index[0]
    
    return {
        'ts_decomposition': ts_decomposition,
        'anomalies': anomalies,
        'customer_segments': df['Customer_Segment'].value_counts(),
        'pareto_threshold': pareto_threshold
    }

def cross_validate_segmentation(df):
    X = df[['Amount', '30_Day_Avg', 'Is_Repeat_Customer']]
    
    segmentation_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('kmeans', KMeans(n_clusters=3, random_state=42))
    ])
    
    scores = cross_val_score(segmentation_pipeline, X, cv=5)
    return scores.mean()