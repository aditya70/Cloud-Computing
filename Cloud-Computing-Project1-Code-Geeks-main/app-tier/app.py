from ast import Param
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import boto3
import botocore

import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from urllib.request import urlopen
from PIL import Image
import numpy as np
import json
import sys
import time

AWS_ACCESS_KEY_ID='XXXXX'
AWS_SECRET_ACCESS_KEY='XXXXX'

REGION_NAME='us-east-1'

s3 = boto3.client('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key= AWS_SECRET_ACCESS_KEY
                     )
BUCKET_NAME='input-img-cloud-computing'
OP_BUCKET_NAME='output-img-cloud-computing'
s4 = boto3.resource('s3')

client_sqs_rcv = boto3.client('sqs', region_name=REGION_NAME,
                    aws_access_key_id=AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                    
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/774086825232/input-file-info.fifo'
OP_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/774086825232/output-file-info.fifo'
QUEUE_NAME='input-file-info.fifo'
OP_QUEUE_NAME='output-file-info.fifo'

max_queue_messages = 10
message_bodies = []
sqs = boto3.resource('sqs', region_name=REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
output_queue = sqs.get_queue_by_name(QueueName=OP_QUEUE_NAME)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@cross_origin()
@app.route('/', methods=['GET'])
def index():   
    return jsonify({"response": "success", "message": "Image processing application started"})


@cross_origin()
@app.route('/api/v1/s3/downlaod', methods=['GET'])
def downloadFile():  
    file_key = request.args.get('file_key') 
    file_name = request.args.get('file_name')
    os.remove(file_name) 
    return jsonify({"response": "success", "message": "file downloaded ", "output": "adfa"})

def downloadFileFromS3(file_key, file_name):
    print("in donwnloadFileFroms3 method", file_key, file_name)
    try:
        s4.Bucket(BUCKET_NAME).download_file(file_key, file_name)
        print('file downloaded')
        return process_image(file_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise Exception


def createOutputFile(fileName,fileOutput):
    try:
     with open(fileName[0:-5], 'w') as f:
        value = f"{fileName[0:-5]},{fileOutput}"
        f.write(value)
    except FileNotFoundError:
        print("The file does not exist")

def get_queue_size():
    size = queue.attributes.get('ApproximateNumberOfMessages')
    return int(size)

def process_image(file_name):
    url = str(file_name)
    img = Image.open(url)

    model = models.resnet18(pretrained=True)

    model.eval()
    img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
    outputs = model(img_tensor)
    _, predicted = torch.max(outputs.data, 1)

    with open('./imagenet-labels.json') as f:
        labels = json.load(f)
    result = labels[np.array(predicted)[0]]
    img_name = url.split("/")[-1]
    save_name = f"{img_name},{result}"
    createOutputFile(img_name,result)
    s3.upload_file(
                    Bucket = OP_BUCKET_NAME,
                    Filename=img_name[0:-5],
                    Key = img_name[0:-5]
                )
    print(f"{save_name}")
    os.remove(img_name[0:-5])
    os.remove(file_name)
    send_message(img_name, result)
    return save_name

def send_message(file_name, file_output):
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    message = {"file_output": file_output, "file_name": file_name}
    response = sqs_client.send_message(
        QueueUrl=OP_QUEUE_URL,
        MessageBody=json.dumps(message),
        MessageGroupId="opcodegeeks"
    )
    print(response)

def receive_queue_msg():
    while get_queue_size()>0:
        queue_response = client_sqs_rcv.receive_message(
            QueueUrl=QUEUE_URL,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=30,
            WaitTimeSeconds=10
        )
        print(queue_response)
        if queue_response is not None:
            if "Messages" in queue_response:
                Messages=queue_response['Messages']
                if Messages:
                    message = Messages[0]
                    message_body=message['Body']
                    obj = json.loads(message_body)
                    file_key=obj['file_key']
                    file_name=obj['file_name']
                    print(file_name)
                    print(file_key)
                    downloadFileFromS3(file_key, file_name)
                    client_sqs_rcv.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                    )

        else :
            time.sleep(5)

receive_queue_msg()    
app.run(host='0.0.0.0')