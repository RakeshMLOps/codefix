import boto3

def list_buckets_with_details():
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    # Get the list of buckets
    response = s3_client.list_buckets()

    print(f"{'Bucket Name':<30}{'Bucket ARN':<50}{'Owner ID':<40}{'Size (GB)':<10}{'Creation Date':<30}")
    print("="*150)

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        creation_date = bucket['CreationDate']
        owner_id = response.get('Owner', {}).get('ID', 'N/A')
        bucket_arn = f"arn:aws:s3:::{bucket_name}"

        # Calculate the size of the bucket
        bucket_size_bytes = 0
        try:
            bucket_objects = s3_resource.Bucket(bucket_name).objects.all()
            for obj in bucket_objects:
                bucket_size_bytes += obj.size
        except Exception as e:
            print(f"Could not access bucket {bucket_name}: {e}")
            continue

        bucket_size_gb = bucket_size_bytes / (1024 ** 3)
        print(f"{bucket_name:<30}{bucket_arn:<50}{owner_id:<40}{bucket_size_gb:<10.2f}{creation_date}")

if __name__ == "__main__":
    list_buckets_with_details()
