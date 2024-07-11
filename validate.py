from great_expectations.dataset import PandasDataset

def validate_data(df):
    ge_df = PandasDataset(df)
    ge_df.expect_column_values_to_not_be_null('Account ID')
    ge_df.expect_column_values_to_be_between('Amount', min_value=0, max_value=1000000)
    ge_df.expect_column_values_to_be_in_set('Status', ['pending', 'paid', 'overdue'])
    results = ge_df.validate()
    return results