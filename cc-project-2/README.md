# Cloud-Computing-Project-2-Code-Geeks
ASU Cloud Computing Project PaaS using AWS Lambda, ECR, S3 and DynamoDB


# Group Member names : 
Aditya Goyal (1225689049)
Anshul Lingarkar (1225118687)
Vibhor Agarwal (1225408366)


# Members' Tasks are as follows : 

Aditya Goyal (1225689049)
1.	Did the setup for AWS Lambda and Amazon Elastic Container Registry.
2.	Created the Docker image in Amazon ECR and created the AWS Lambda function using the Docker image from Amazon ECR.
3.	Worked on uploading the student_data.json file into the DynamoDB database.

Anshul Lingarkar (1225118687)
1.	Implemented the code to download the video uploaded by the user in S3 bucket.
2.	Implemented the code to extract the first frame from video and store it in /tmp/ folder on AWS Lambda.

Vibhor Agarwal (1225408366)
1.	Implemented the face_recognition_handler function to work on the frames extracted from the video uploaded in S3 input bucket.
2.	Implemented the code to create csv file for the result data and upload it to S3 Output bucket.


# AWS credentials : 

AWS_ACCESS_KEY_ID='XXXXX'
AWS_SECRET_ACCESS_KEY='XXXXX'

REGION_NAME='us-east-1'


# S3 Buckets Details : 

INPUT_BUCKET_NAME = test-proj-cc-4

OUTPUT_BUCKET_NAME = demo-output-csv-1


# DynamoDB Details : 

DynamoDB Table name = student


# Lambda Function Details : 

Lambda Function Name = test-proj-4


# Amazon ECR Details : 

Container Name on Amazon Elastic Container Registry = test-cc-proj


# AMI Tag Details :

TAG_VALUE = App-Tier-code-geeks

# Steps to install and run the code:

1.	Create a Docker Container with the encodings file and handler.py file. The main code of our application will be present in the handler.py file.
2.	Build the Docker image using the following command:
a.	docker build -t test-cc-proj .
3.	Use the command from AWS Console to login to the AWS Account and push the Docker image to the AWS Elastic Container Registry.
a.	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 341967751550.dkr.ecr.us-east-1.amazonaws.com
b.	docker tag test-cc-proj:latest 341967751550.dkr.ecr.us-east-1.amazonaws.com/test-cc-proj:latest
c.	docker push 341967751550.dkr.ecr.us-east-1.amazonaws.com/test-cc-proj:latest
4.	Create an input bucket with the name “test-proj-cc-4” and an output bucket with the name “demo-output-csv-1” in S3.
5.	Create a DynamoDB table with the name – “student” and load the “student_data.json” file in this table.
6.	Create AWS Lambda function using the docker image from ECR and set the trigger point to S3 input bucket – “test-proj-cc-4”.
7.	Increase the memory and timeout for AWS Lambda to 1024 MB and 1 minute respectively.
8.	Now you can invoke the workload generator which will upload the video files to the S3 input bucket. Once the video is available in the S3 input bucket, the AWS Lambda function will be triggered.
9.	AWS Lambda function will process the image, run the face-recognition module and store the student details in CSV file to the S3 output bucket.


