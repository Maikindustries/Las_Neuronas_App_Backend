import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('spaceTrips')

def write_to_dynamo(contenido, resultado):
    data = {}
    data['uuid'] = uuid.uuid1().hex
    data['cryoSleep'] = contenido['cryoSleep']
    data['age'] = contenido['age']
    data['vip'] = contenido['vip']
    data['destination'] = contenido['destination']
    data['transported'] = resultado
    x = table.put_item(Item=mydict)
    #print(x)

def print_db_items():
    items = table.scan()
    print(items)
