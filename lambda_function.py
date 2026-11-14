import json
import boto3
from PIL import Image
import io 

def lambda_handler(event, context):
    print("lambda started")
    try:
        # destination bucket for resized image
        destination_bucket = 'ccmp200-resized-image-s3'
        
        # Create S3 client
        s3 = boto3.client('s3')
        
        # Get bucket and object key from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print(f"processing image: {key}")
        print(f"source bucket: {bucket}")
        
        # Download the image from S3
        print("downloading image...")
        response = s3.get_object(Bucket=bucket, Key=key)
        
        image_content = response['Body'].read()
        print("image downloaded successfully")
        # Open the image using PIL
        image = Image.open(io.BytesIO(image_content))
        
        # Resize the image
        resized_image = image.resize((100, 100))

        print("image resized successfully")
        
        # Save the resized image to a BytesIO object
        buffer = io.BytesIO()
        resized_image.convert('RGB').save(buffer, 'JPEG')
        buffer.seek(0)
        
        # Upload the resized image to S3
        s3.put_object(Bucket=destination_bucket, Key=f"resized-{key}", Body=buffer, ContentType='image/jpeg')

        print("image uploaded successfully")
        
        return{
            'statusCode': 200,
            'body': json.dumps('Image resized successfully!')
        }
    except Exception as e:
        return{
            'statusCode':500,
            'body': json.dumps(f'Error: {str(e)}')
        }