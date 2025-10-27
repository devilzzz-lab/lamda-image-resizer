import boto3
import os
from PIL import Image
from io import BytesIO

s3 = boto3.client("s3")
OUTPUT_BUCKET = "devil-output-bucket"

def lambda_handler(event, context):
    # Get bucket and object key from event
    input_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    input_key = event["Records"][0]["s3"]["object"]["key"]

    try:
        # Download image from input bucket
        response = s3.get_object(Bucket=input_bucket, Key=input_key)
        image_data = response["Body"].read()

        # Open and resize image
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGB")
        image.thumbnail((800, 800))  # Resize to max 800x800

        # Save to buffer
        buffer = BytesIO()
        image.save(buffer, "JPEG")
        buffer.seek(0)

        # Upload resized image to output bucket
        output_key = f"resized-{os.path.basename(input_key)}"
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=buffer,
            ContentType="image/jpeg"
        )

        print(f"✅ Successfully processed and uploaded: {output_key}")
        return {"status": "success", "file": output_key}

    except Exception as e:
        print(f"❌ Error: {e}")
        raise e
