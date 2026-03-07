import pandas as pd
import hashlib
import os

def anonymize_telemetry(input_file, output_folder="sanitized_data"):
    """
    AEGIS Phase 1: Data Scrubbing Utility
    Purpose: Remove PII and linkable identifiers before AI training.
    """
    # Load raw telemetry
    df = pd.read_csv(input_file)

    # 1. SHA-256 Hashing of Hardware IDs (HWID)
    # This allows the AI to recognize a "repeat offender" without knowing who they are.
    if 'hwid' in df.columns:
        df['hwid_hash'] = df['hwid'].apply(
            lambda x: hashlib.sha256(str(x).encode()).hexdigest()
        )

    # 2. Strict PII Removal
    # Dropping columns that could identify a specific human or physical location.
    pii_columns = [
        'ip_address', 'email_address', 'account_id', 
        'billing_name', 'street_address', 'hwid'
    ]
    df_clean = df.drop(columns=[col for col in pii_columns if col in df.columns])

    # 3. Precision Reduction (Geo-fencing)
    # We keep 'Country' for regional bias testing but drop 'City' to prevent doxing.
    if 'city' in df_clean.columns:
        df_clean = df_clean.drop(columns=['city'])

    # 4. Compliance Timestamping
    df_clean['audit_scrub_timestamp'] = pd.Timestamp.now()

    # Save sanitized data
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, f"sanitized_{os.path.basename(input_file)}")
    df_clean.to_csv(output_path, index=False)
    
    print(f"✔️ Phase 1 Audit Complete: Data sanitized at {output_path}")
    return df_clean

# Example Usage:
# anonymize_telemetry("raw_battlefield_logs.csv")
