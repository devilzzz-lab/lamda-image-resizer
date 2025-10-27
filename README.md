<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

  <h1>🖼️ AWS Lambda Image Resizer Project</h1>

  <h2>📘 Overview</h2>
  <p>
    This project demonstrates how to build a <b>serverless image processing system</b> using 
    <b>AWS Lambda</b>, <b>Amazon S3</b>, and <b>Python (Pillow)</b>.<br>
    Whenever a new image is uploaded to the <b>input S3 bucket</b>, a Lambda function automatically resizes it and stores the output in another bucket.
  </p>

  <hr>

  <h2>🏗️ Architecture</h2>

  <h3>Flow:</h3>
  <ol>
    <li>User uploads an image to <b>devil-input-bucket</b></li>
    <li>S3 triggers a <b>Lambda Function</b></li>
    <li>Lambda downloads the image, resizes it using <b>Pillow</b></li>
    <li>Resized image is uploaded to <b>devil-output-bucket</b></li>
    <li>Logs and results are visible in <b>CloudWatch</b></li>
  </ol>

  <h3>Services Used:</h3>
  <ul>
    <li>🪣 Amazon S3</li>
    <li>🧠 AWS Lambda</li>
    <li>🔐 IAM Roles &amp; Permissions</li>
    <li>📜 Amazon CloudWatch</li>
  </ul>

  <hr>

  <h2>⚙️ Setup Instructions</h2>

  <h3>1️⃣ Create S3 Buckets</h3>
  <ul>
    <li><code>devil-input-bucket</code></li>
    <li><code>devil-output-bucket</code></li>
  </ul>
  <p>Enable <b>event notification</b> on <code>devil-input-bucket</code> for <b>PUT (ObjectCreated)</b> → trigger your Lambda.</p>

  <h3>2️⃣ Create an IAM Role for Lambda</h3>
  <p>Attach the following permissions:</p>
  <ul>
    <li><b>AWSLambdaBasicExecutionRole</b></li>
    <li><b>AmazonS3FullAccess</b> (for demo purposes; limit later for production)</li>
  </ul>

  <h3>3️⃣ Create the Lambda Function</h3>
  <ul>
    <li><b>Runtime:</b> Python 3.12</li>
    <li><b>Architecture:</b> x86_64</li>
    <li><b>Handler:</b> lambda_function.lambda_handler</li>
    <li><b>Timeout:</b> 10 seconds</li>
    <li><b>Memory:</b> 256 MB</li>
  </ul>
  <p>Attach the IAM role created above.</p>

  <h3>4️⃣ Add the Pillow Layer</h3>
  <p>For <b>Python 3.12 (x86_64)</b>:</p>
  <code>arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p312-Pillow:7</code>

  <h3>5️⃣ Lambda Function Code</h3>

  <pre><code>import boto3
import os
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')
OUTPUT_BUCKET = 'devil-output-bucket'

def lambda_handler(event, context):
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    input_key = event['Records'][0]['s3']['object']['key']

    try:
        # Download image from input bucket
        response = s3.get_object(Bucket=input_bucket, Key=input_key)
        image_data = response['Body'].read()

        # Open and resize image
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')
        image.thumbnail((800, 800))  # Resize to max 800x800

        # Save resized image to buffer
        buffer = BytesIO()
        image.save(buffer, 'JPEG')
        buffer.seek(0)

        # Upload to output bucket
        output_key = f"resized-{os.path.basename(input_key)}"
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=buffer,
            ContentType='image/jpeg'
        )

        print(f"✅ Successfully processed: {output_key}")
        return {"status": "success", "file": output_key}

    except Exception as e:
        print(f"❌ Error: {e}")
        raise e
  </code></pre>

  <h3>6️⃣ Testing</h3>
  <ol>
    <li>Go to S3 → <b>devil-input-bucket</b></li>
    <li>Upload an image (e.g., <code>test.jpg</code>)</li>
    <li>Wait for a few seconds</li>
    <li>Check <b>devil-output-bucket</b></li>
    <li>You should see <code>resized-test.jpg</code></li>
    <li>Open CloudWatch Logs → check “✅ Successfully processed…” message</li>
  </ol>

  <h3>📊 CloudWatch Example Log</h3>
  <pre><code>START RequestId: abc123 Version: $LATEST
✅ Successfully processed: resized-test.jpg
END RequestId: abc123
REPORT RequestId: abc123 Duration: 500 ms Memory Used: 45 mb
  </code></pre>

  <h2>🧠 Learning Outcomes</h2>
  <ul>
    <li>Understanding AWS Lambda triggers and events</li>
    <li>Handling S3 operations via Boto3</li>
    <li>Using Layers to include dependencies (Pillow)</li>
    <li>Managing permissions using IAM Roles</li>
    <li>Working with serverless image processing systems</li>
  </ul>

  <h2>🧾 Author</h2>
  <p>
    <b>Name:</b> Devil<br>
    <b>Project:</b> AWS Serverless Image Resizer<br>
    <b>Tools:</b> AWS Lambda, S3, CloudWatch, Python, Pillow<br>
    <b>Region:</b> us-east-1
  </p>

</body>
</html>
