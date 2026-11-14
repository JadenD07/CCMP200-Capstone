# CCMP200-Capstone
Serverless image  processing pipeline
This project is an automated image-resizing application built using AWS services. It allows users to upload an image to an Amazon S3 bucket, automatically resize the image using an AWS Lambda function, and save the resized image to a separate S3 bucket.

AWS Step functions is used to orchestrate the image-processing workflow and determine whether the operation completed successfully or failed. Amazon API Gateway provides an HTTP endpoint that allows users to trigger the Step Functions state machine.

## AWS Services Used
The application uses the following AWS services:
 * Amazon S3: Stores the original uploaded images and the resized images in separate buckets.
 * AWS Lambda: Runs python image-processing code.
 * Amazon Step Functions: The state machine that coordinates the workflow and evaluates if the Lambda response using a choice state.
 * Amazon API Gateway: Provides a POST enpoint to start the Step Functions state machine.
 * AWS IAM: Manages the necessary permissions between the AWS services.
 * Amazon CloudWatch: Collects the Lambda logs, and helps monitor execution and troubleshoot errors.

 ## Application Architecture
 The application consists of two related execution paths.

 ### Image Upload and Resizing
 1. A user uploads an image to the original S3 bucket.
 2. Amazon S3 triggers the image-resizing Lambda function through an event notification.
 3. Lambda retrieves the uploaded image from the original S3 bucket.
 4. The Python function uses the Pillow (PIL) library to resize the image to 100 x 100 pixels.
 5. The resized image is converted to JPEG format.
 6. Lambda uploads the resized image to the destination S3 bucket.

 ### Step Functions Workflow
 1. A user sends an HTTP POST reguest to the API Gateway endpoint such as with Postman. An example of the POST request with Postman includes:
        {
            "Records": [
            {
            "s3": {
                "bucket": {
                "name": "ccmp200-original-image-s3"
                },
                "object": {
                "key": "DarthVader.jpeg"
                }
            }
            }
        ]
        }
        
 2. API Gateway invokes the Step Functions StartExecution action.
 3. Step Functions executes the image-processing Lambda task.
 4. Lambda returns a JSON response containing a status code.
 5. The Choice state evaluates the returned status code.
 6. If the status code is 200, the workflow goes into the Success state.
 7. If the status code is 500, the workflow goes into the Fail state.
 8. If there is an unknown error where there is an unfamiliar status code, the workflow goes into the Fail state.

