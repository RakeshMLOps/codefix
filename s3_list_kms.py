import boto3
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3')

def list_buckets_with_kms_status():
    try:
        # Get the list of all S3 buckets
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])

        # Iterate through each bucket
        for bucket in buckets:
            bucket_name = bucket['Name']
            print(f"Bucket: {bucket_name}")

            try:
                # Get bucket encryption configuration
                encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
                rules = encryption.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
                kms_enabled = any(
                    rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm') == 'aws:kms'
                    for rule in rules
                )
                if kms_enabled:
                    print("  KMS Encryption: Enabled")
                else:
                    print("  KMS Encryption: Disabled")
            except ClientError as e:
                # Handle encryption not configured
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    print("  KMS Encryption: Disabled")
                else:
                    print(f"  Error fetching encryption: {e}")
    except ClientError as e:
        print(f"Error: {e}")

# Execute the function
list_buckets_with_kms_status()
