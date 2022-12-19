from ast import Param
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import boto3
import time


AWS_ACCESS_KEY_ID='XX'


AWS_SECRET_ACCESS_KEY='XX'
REGION_NAME='us-east-1'

s3 = boto3.client('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key= AWS_SECRET_ACCESS_KEY
                     )

BUCKET_NAME='input-img-cloud-computing-3'
s4 = boto3.resource('s3')

client_sqs_rcv = boto3.client('sqs', region_name=REGION_NAME,
                    aws_access_key_id=AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                    
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/341967751550/input-file-info.fifo'
OP_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/341967751550/output-file-info.fifo'
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

def is_file_extension_valid(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cross_origin()
@app.route('/', methods=['GET'])
def index():  
    return jsonify({"response": "success", "message": "Web Tier Application Started Successfully."})

@cross_origin()
@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'myfile' not in request.files:
            return jsonify({"response": "failed", "message": "File not found"})
        file = request.files['myfile']
        if file.filename == '':
            return jsonify({"response": "failed", "message": "File name should not be empty"})
        if file and is_file_extension_valid(file.filename):
            file_name = secure_filename(file.filename)
            category_folder = os.path.join(app.config['UPLOAD_FOLDER'])
            os.makedirs(category_folder, exist_ok=True)
            file.save(file_name)
            s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=file_name,
                    Key = file_name
                )
            send_message(file_name)
            os.remove(file_name)   
            return jsonify({"response": "success", "message": "File uploaded successfully"})
    else:
         return jsonify({"response": "failed", "message": request.method + "is not allowed"})  

def send_message(file_name):
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    message = {"file_key": file_name, "file_name": file_name}
    response = sqs_client.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message),
        MessageGroupId="codegeeks"
    )
    print(response)

def get_queue_size():
    size = output_queue.attributes.get('ApproximateNumberOfMessages')
    return int(size)

def receive_queue_msg():
    while get_queue_size()>0:
        queue_response = client_sqs_rcv.receive_message(
            QueueUrl=OP_QUEUE_URL,
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
                    file_output=obj['file_output']
                    file_name=obj['file_name']
                    print(file_name)
                    print(file_output)
                    client_sqs_rcv.delete_message(
                    QueueUrl=OP_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                    )

receive_queue_msg() 

app.run(host='0.0.0.0')