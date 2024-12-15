import boto3
import csv

def get_bucket_details_with_arn(output_csv_file):
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    # Get the bucket list
    response = s3_client.list_buckets()

    # Prepare CSV headers
    csv_headers = ['Bucket Name', 'Bucket ARN', 'Owner ID', 'Size (GB)', 'Creation Date']
    
    # Open the CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

        # Iterate through each bucket
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            creation_date = bucket['CreationDate']
            owner_id = response.get('Owner', {}).get('ID', 'N/A')
            bucket_arn = f"arn:aws:s3:::{bucket_name}"

            # Calculate bucket size
            bucket_size_bytes = 0
            try:
                bucket_objects = s3_resource.Bucket(bucket_name).objects.all()
                for obj in bucket_objects:
                    bucket_size_bytes += obj.size
            except Exception as e:
                print(f"Could not access bucket {bucket_name}: {e}")
                continue

            # Convert size to GB
            bucket_size_gb = bucket_size_bytes / (1024 ** 3)

            # Write bucket details to the CSV file
            writer.writerow([bucket_name, bucket_arn, owner_id, round(bucket_size_gb, 2), creation_date])

    print(f"Bucket details with ARN have been exported to {output_csv_file}")

if __name__ == "__main__":
    # Specify the output CSV file name
    output_csv = "s3_buckets_with_arn.csv"
    get_bucket_details_with_arn(output_csv)
