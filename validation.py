import pandas as pd

REQUIRED_COLUMNS = ['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']

def validate_telco_data(df):
    results = []

    missing_count = int(df[REQUIRED_COLUMNS].isna().sum().sum())
    results.append({
        'Check': 'Missing values',
        'Rule': 'No missing values in required columns',
        'Result': 'PASS' if missing_count == 0 else 'FAIL',
        'Issue Count': missing_count
    })

    duplicate_count = int(df.duplicated(subset=['customerID']).sum())
    results.append({
        'Check': 'Duplicate customer IDs',
        'Rule': 'customerID must be unique',
        'Result': 'PASS' if duplicate_count == 0 else 'FAIL',
        'Issue Count': duplicate_count
    })

    total_charges_numeric = pd.to_numeric(df['TotalCharges'], errors='coerce')
    hidden_missing_count = int(total_charges_numeric.isna().sum())
    results.append({
        'Check': 'TotalCharges numeric conversion',
        'Rule': 'TotalCharges must convert to numeric',
        'Result': 'PASS' if hidden_missing_count == 0 else 'FAIL',
        'Issue Count': hidden_missing_count
    })

    invalid_range_count = int(
        ((df['tenure'] < 0) |
         (df['tenure'] > 72) |
         (df['MonthlyCharges'] < 0)).sum()
    )
    results.append({
        'Check': 'Value ranges',
        'Rule': 'tenure 0-72 and MonthlyCharges >= 0',
        'Result': 'PASS' if invalid_range_count == 0 else 'FAIL',
        'Issue Count': invalid_range_count
    })

    invalid_target_count = int((~df['Churn'].isin(['Yes', 'No'])).sum())
    results.append({
        'Check': 'Target values',
        'Rule': 'Churn must be Yes or No',
        'Result': 'PASS' if invalid_target_count == 0 else 'FAIL',
        'Issue Count': invalid_target_count
    })

    return pd.DataFrame(results)

if __name__ == '__main__':
    telco_df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    print(validate_telco_data(telco_df).to_string(index=False))
