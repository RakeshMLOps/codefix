import boto3
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3')

def list_buckets_with_encryption():
    try:
        # List all S3 buckets
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])

        for bucket in buckets:
            bucket_name = bucket['Name']
            print(f"\nBucket: {bucket_name}")

            try:
                # Get bucket encryption
                encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
                rules = encryption.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
                for rule in rules:
                    sse_algorithm = rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm', '')
                    kms_key_id = rule.get('ApplyServerSideEncryptionByDefault', {}).get('KMSMasterKeyID', 'Default KMS Key')
                    print(f"  - SSE Algorithm: {sse_algorithm}")
                    if sse_algorithm == 'aws:kms':
                        print(f"  - KMS Key ID: {kms_key_id}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    print("  - No server-side encryption configured.")
                else:
                    print(f"  - Error fetching encryption: {e}")
    except ClientError as e:
        print(f"Error: {e}")

# Execute the function
list_buckets_with_encryption()
