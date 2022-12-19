# Cloud-Computing-Project-Code-Geeks
ASU Cloud Computing Project Iaas using EC2, SQS and S3

# Group Member names : 
Vibhor Agarwal (1225408366)
Aditya Goyal (1225689049))
Anshul Lingarkar (1225118687)

# Members' Tasks are as follows : 

Aditya Goyal (1225689049)
1.	Developed a Flask Application containing Web-tier’s code and deployed it on an EC2 instance.
2.	Developed the code to connect to the S3 server and upload the user-provided images to it.
3.	Wrote the API endpoint to upload the image to the S3 server.
4.	Developed the code to connect to the SQS service and push the image metadata to the input queue.
5.	Developed a listener that connects to SQS, listens to incoming messages from the output, and displays the output of image processing in the application     console.
6.	Completed the networking setup for the Nginx server for Web-tier’s EC2 instance enabling the users to access the application from anywhere on the           internet.

Anshul Lingarkar (1225118687)
1.	Developed the script to instantiate and scale out EC2 instances based on the number of messages in the queue.
2.	Developed the code to scale in EC2 instances by stopping them if the number of messages in the queue is 0.
3.	Developed the script to startup a pre-configured EC2 instance with App-tier’s code already running.
4.	Configured Nginx server to enable reverse-proxy services upon Application startup.

Vibhor Agarwal (1225408366)
1.	Developed a Flask application containing App-tier’s code (NLP algorithm) and deployed it on an EC2 instance.
2.	Developed the code to connect to SQS and push the output message to SQS after processing the image.
3.	Developed the code to create an output file using python script and write the NLP algorithm’s output in it.
4.	Developed the code to connect to S3 and upload the output file after processing the image to S3.
5.	Completed the networking setup for the Nginx server for App-tier’s EC2 instance enabling the users to access the application from anywhere on the           internet.


# AWS credentials : 

AWS_ACCESS_KEY_ID='XXXXX'
AWS_SECRET_ACCESS_KEY='XXXXX'

REGION_NAME='us-east-1'

# PEM key file name
Test_Key_Pair.pem

# Web Tier's URL 
http://18.207.246.102/api/v1/upload

# Elastic IP address 
This will be the public URL of the web-tier's instance. Since, it's dynamic, so it will be based on the automatically generated IPv4 address of the AMI.


# SQS Names : 

Input queue details : 
QUEUE_NAME = input-file-info.fifo
QUEUE_URL = https://sqs.us-east-1.amazonaws.com/497701912194/input-file-info.fifo

Output queue details : 
OP_QUEUE_URL = https://sqs.us-east-1.amazonaws.com/497701912194/output-file-info.fifo
OP_QUEUE_NAME= output-file-info.fifo

# S3 Buckets Details : 

INPUT_BUCKET_NAME = input-img-cloud-computing

OUTPUT_BUCKET_NAME = output-img-cloud-computing

# AMI Tag Details :

TAG_VALUE = App-Tier-code-geeks

