from fileinput import filename
from boto3 import client as boto3_client
import face_recognition
import pickle
import urllib.parse
import boto3
import botocore
import os
import ffmpeg
import csv

# input bucket name is test-proj-cc-4 which is linked with lambda
output_bucket = "demo-output-csv-1"

s3 = boto3.client('s3')
s4 = boto3.resource('s3')

resource = boto3.resource(
    'dynamodb'
)
table = resource.Table('student')

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):
    print("entered facerecognition handler")
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        video_name = download_video_from_s3(bucket,key,key)
        video_name = video_name[0:-4]
        image_path = '/tmp/' + key
        image = get_image_frame(image_path,"/tmp/")
        print("after creating frames")
        print(image)
        match_name = process_image(image)
        print("recognition result")
        print(match_name)
        data_response = table.get_item(Key={'name': match_name})
        print(data_response)
        if 'Item' in data_response:
            responseItem = data_response["Item"]
            print(responseItem)
            name = responseItem["name"]
            major = responseItem["major"]
            year = responseItem["year"]
            file_name = create_csv_file(name,major,year,video_name)
            print(file_name, name, major, year)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


def download_video_from_s3(bucket,file_name,file_key):
    print("in donwnloadFileFroms3 method", file_key, file_name)
    try:
        filepath = '/tmp/' + file_key
        s4.Bucket(bucket).download_file(file_key, filepath)
        print('file downloaded')
        return file_key
    except botocore.exceptions.ClientError as e:
        print("excpetion is ",e)
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise Exception

def process_image(img_path):
    image_files = face_recognition.load_image_file(img_path)
    image_file_encoding = face_recognition.face_encodings(image_files)[0]
    # get known face encodings from file
    with open("encoding.dat", 'rb') as f: 
        known_face_encodings = pickle.load(f)
        known_names = list(known_face_encodings.keys())
        face_encodings = list(known_face_encodings.values())
        known_names = face_encodings[0]
    face_encodings = known_face_encodings['encoding']
    # compare known face with unknown face encodings
    result = face_recognition.compare_faces(face_encodings, image_file_encoding)
    for ans in result:
        if ans:
            idx = result.index(ans)
            return (known_names[idx])

def get_image_frame(video_path,image_path):
	os.system("ffmpeg -i "  + str(video_path) + " -vframes 1 " + str(image_path) + "image-%3d.jpeg")
	return image_path+"image-001.jpeg"

def create_csv_file(name,major,year,video_name):
    print("creating csv file")
    filename = video_name+".csv"
    filepath = '/tmp/' + filename
    with open(filepath, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)                    
        filewriter.writerow(['Name','Major','Year'])
        filewriter.writerow([name,major,year])
    print("upload file started")
    s3.upload_file(
                    Bucket = output_bucket,
                    Filename = filepath,
                    Key = filename
                )  
    print("upload file completed")      
    os.remove(filepath)  
    return filename    
   