import boto3
import time

AWS_ACCESS_KEY_ID='XX'


AWS_SECRET_ACCESS_KEY='XX'
REGION_NAME='us-east-1'

QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/341967751550/input-file-info.fifo'
OP_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/341967751550/output-file-info.fifo'
QUEUE_NAME='input-file-info.fifo'
OP_QUEUE_NAME='output-file-info.fifo'

INSTANCE_STATE_RUNNING="running"
INSTANCE_STATE_PENDING="pending"
INSTANCE_STATE_STOPPED="stopped"
TAG_VALUE="App-Tier-cloud-geeks-1"
MAX_INSTANCES=19
MIN_INSTANCES=0

aws_session = boto3.session.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

sqs = aws_session.resource('sqs')
sqs_client = aws_session.client('sqs')
ec2 = aws_session.resource('ec2')
ec2_client = boto3.client('ec2',region_name = REGION_NAME)

def get_input_queue_size():
    input_queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    input_queue_size = int(input_queue.attributes.get('ApproximateNumberOfMessages'))+int(input_queue.attributes.get('ApproximateNumberOfMessagesNotVisible'))
    print('Size of input SQS is ' + str(input_queue_size))
    get_output_queue_size()
    return input_queue_size

def get_output_queue_size():
    output_queue = sqs.get_queue_by_name(QueueName=OP_QUEUE_NAME)
    output_queue_size = int(output_queue.attributes.get('ApproximateNumberOfMessages'))+int(output_queue.attributes.get('ApproximateNumberOfMessagesNotVisible'))
    print('Size of output SQS is ' + str(output_queue_size))
    return output_queue_size

def total_app_instances_running():
    instances = ec2.instances.all()
    instance_count = 0
    for instance in instances:
        instance_state = instance.state["Name"]
        if (instance_state == INSTANCE_STATE_PENDING or instance_state == INSTANCE_STATE_RUNNING) and instance.tags:
            for tag in instance.tags:
                if TAG_VALUE in tag['Value']:
                    instance_count = instance_count + 1
    print('Total number of running instances =',instance_count)
    return instance_count

def start_instance():
    instances = ec2.instances.all()
    print(instances)
    for instance in instances:
        if instance.state["Name"] == INSTANCE_STATE_STOPPED and instance.tags:
            print("in instance state")
            for tag in instance.tags:
                print("tag name is ", tag)
                if TAG_VALUE in tag['Value']:
                    instance.start(DryRun=False)
                    break
            break

def closeEC2Instance():
    print("closeEC2Instance ")
    instances = ec2.instances.all()
    for instance in instances:
        print("instance going to be stopped ",instance)
        if instance.state["Name"] == INSTANCE_STATE_RUNNING and instance.tags:
            for tag in instance.tags:
                print("tag name is ", tag)
                if TAG_VALUE in tag['Value']:
                    print("tag value matched for app tier")
                    instance.stop(DryRun=False)

def auto_scale_instances():
    input_queue_size = get_input_queue_size()
    instance_size = total_app_instances_running()
    if  input_queue_size > instance_size:
        create_instance(instance_size, input_queue_size)
        time.sleep(5)
    else: 
        print("auto_scaling else block input_queue_size instance_size ",input_queue_size, instance_size)
        if (input_queue_size == 0 and instance_size > MIN_INSTANCES):
            closeEC2Instance()

def create_instance(instance_size, queue_size):
    if queue_size <= MAX_INSTANCES:
        remaining_instances = queue_size-instance_size
    else:
        remaining_instances = MAX_INSTANCES-instance_size
    for instance in range(remaining_instances):
        print("in provision")
        start_instance()
        time.sleep(1)

if __name__ == '__main__':
    while True:
        auto_scale_instances()
        time.sleep(5)