import base64
import json
import boto3

sns = boto3.client("sns", aws_access_key_id='AWS_ACCESS_KEY', aws_secret_access_key='AWS_SECRET_ACCESS_KEY', region_name='us-east-1')
dynamo = boto3.resource('dynamodb')


def lambda_handler(event, context):

    item = None
    table = dynamo.Table('productos')

    decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
    deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]

    with table.batch_writer() as batch_writer:
        for item in deserialized_data:
            batch_writer.put_item(Item={'id_producto': item['id_producto'], 'fecha_reg': item['fecha_reg'], 'producto': item['producto']})

            if item['producto'] == 'EC2':
                sns.publish(
                    TopicArn='arn:aws:sns:us-east-1:052372658767:snsCompras',
                    Subject='Alerta de producto',
                    Message='El sistema funciona correctamente.')
