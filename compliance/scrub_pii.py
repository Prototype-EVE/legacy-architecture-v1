import pandas as pd
import hashlib

def anonymize_telemetry(df):
    """
    Scrubs PII (Personally Identifiable Information) from game logs 
    to ensure Phase 1 Compliance.
    """
    # 1. Hash Hardware IDs (HWID) so they are unique but untraceable
    df['hwid_hash'] = df['hwid'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    
    # 2. Drop sensitive direct identifiers
    sensitive_cols = ['ip_address', 'email', 'account_id', 'billing_zip']
    df_clean = df.drop(columns=sensitive_cols)
    
    # 3. Add 'Audit_Timestamp' for Phase 1 Data Retention compliance
    df_clean['scrubbed_at'] = pd.Timestamp.now()
    
    return df_clean
