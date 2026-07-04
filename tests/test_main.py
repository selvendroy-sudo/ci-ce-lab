import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validation import validate_telco_data

def test_validation_returns_expected_checks():
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    result = validate_telco_data(df)

    assert len(result) == 5
    assert set(result['Check']) == {
        'Missing values',
        'Duplicate customer IDs',
        'TotalCharges numeric conversion',
        'Value ranges',
        'Target values'
    }

def test_customer_id_has_no_duplicates():
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    result = validate_telco_data(df)

    duplicate_row = result[result['Check'] == 'Duplicate customer IDs'].iloc[0]

    assert duplicate_row['Result'] == 'PASS'
    assert duplicate_row['Issue Count'] == 0

def test_total_charges_hidden_missing_values_detected():
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    result = validate_telco_data(df)

    total_row = result[result['Check'] == 'TotalCharges numeric conversion'].iloc[0]

    assert total_row['Result'] == 'FAIL'
    assert total_row['Issue Count'] == 11
