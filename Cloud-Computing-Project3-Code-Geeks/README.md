# Cloud-Computing-Project-Code-Geeks
ASU Cloud Computing Project - Hybrid Cloud setup using Openstack and AWS resources(EC2,SQS,S3)

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
7. Created the web-tier instances and wrote the code to export the AMI to S3 bucket in 2 different formats (.bin and .vmdk).
8. Created role-policy.json and trust-policy.json to enable the access of vimport user to be able to read from EC2 AMI and export it to S3.
9. Created the network router,gateway,interface for the web-tier Nova instance.
10. Tested web-tier with different test cases.

Anshul Lingarkar (1225118687)
1.	Developed the script to instantiate and scale out EC2 instances based on the number of messages in the queue.
2.	Developed the code to scale in EC2 instances by stopping them if the number of messages in the queue is 0.
3.	Developed the script to startup a pre-configured EC2 instance with App-tier’s code already running.
4.	Configured Nginx server to enable reverse-proxy services upon Application startup.
5. Setup the Virtual box with the ubuntu image.
6. Configured SSH for the AMI installed in Openstack to run the web-tier instance.
7. Setup the workload generator to test the web-tier and app-tier instances.
8. Created the security groups for Nova instance.
9. Created the Project report for Submission.

Vibhor Agarwal (1225408366)
1.	Developed a Flask application containing App-tier’s code (NLP algorithm) and deployed it on an EC2 instance.
2.	Developed the code to connect to SQS and push the output message to SQS after processing the image.
3.	Developed the code to create an output file using python script and write the NLP algorithm’s output in it.
4.	Developed the code to connect to S3 and upload the output file after processing the image to S3.
5.	Completed the networking setup for the Nginx server for App-tier’s EC2 instance enabling the users to access the application from anywhere on the           internet.
6. Installed openstack in ubuntu and did the initial configuration for installing open stack by making changes to requirement-constraints file.
7. Created the web-tier instance using Nova by first import the downloaded AMI as an image in openstack and then luanched an instance out of it. 
8. Did the setup for floating IP for Nova instance so that it is accessible publically.
9. Monitored AWS resources (S3,SQS and EC2) to record the testing results.


# AWS credentials : 

AWS_ACCESS_KEY_ID='XX'


AWS_SECRET_ACCESS_KEY='XX'
REGION_NAME='us-east-1'

# PEM key file name
cc-proj-3.pem

# Web Tier's URL (OpenStack instance floating IP)
http://172.24.4.214/api/v1/upload

# Floating IP address 
This will be the public URL of the web-tier's instance. Since, it's dynamic, so it will be based on the automatically generated IPv4 address of the AMI.
http://172.24.4.214/api/v1/upload

# SQS Names : 

Input queue details : 
QUEUE_NAME = input-file-info.fifo
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/341967751550/input-file-info.fifo'

Output queue details : 
OP_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/341967751550/output-file-info.fifo'
OP_QUEUE_NAME= output-file-info.fifo

# S3 Buckets Details : 

INPUT_BUCKET_NAME = input-img-cloud-computing-3

OUTPUT_BUCKET_NAME = output-img-cloud-computing-3

# AMI Tag Details :

TAG_VALUE = App-Tier-cloud-geeks-1

