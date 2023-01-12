from flask import Flask, jsonify, request,render_template
import boto3
import json
from datetime import datetime
import random
import time
import uuid
import pytz

app = Flask(__name__)

tz_bsas = pytz.timezone('America/Argentina/Buenos_Aires')
name_stream = 'awsStream'
list_services = ['lambda', 'S3', 'EC2','ECS','Cloud9','Cloud_Formation','RDS','Dynamo','Fargate','Glue','SNS','ECR','VPC','Athena','Rekognition']

kinesis = boto3.client('kinesis', aws_access_key_id='AWS_ACCESS_KEY',aws_secret_access_key='AWS_SECRET_ACCESS_KEY', region_name = 'us-east-1')

def put_to_stream(kinesis):
    datetime_bsas = datetime.now(tz_bsas)
    record = {
        'id_producto': str(uuid.uuid4()),
        'fecha_reg': datetime_bsas.strftime("%Y-%m-%d %H:%M:%S"),
        'producto': random.choice(list_services)
    }
    print(record)
    kinesis.put_record(
        StreamName = name_stream,
        Data = json.dumps(record),
        PartitionKey = 'a-partition')

@app.route("/load", methods=["GET"])
def start():
    return render_template("index.html")

@app.route("/load", methods = ["POST"])
def load_data():
    if request.method == "POST":
        i = 0
        while i < 20:
            i += 1
            put_to_stream(kinesis)
            time.sleep(.3)
    return jsonify({"message": "Data loaded"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True)