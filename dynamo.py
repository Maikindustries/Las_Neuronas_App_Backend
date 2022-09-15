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
    data['transported'] = int(resultado)
    x = table.put_item(Item=data)
    #print(x)

def print_db_items():
    items = table.scan()
    print(items)

def serve_surv_stats():
    response = table.query(
        KeyConditionExpression=Key('transported').eq(1)
        )
    #print(response['Items'])
    return response['Items']

def serve_death_stats():
    response = table.query(
        KeyConditionExpression=Key('transported').eq(0)
        )
    #print(response['Items'])
    return response['Items']

def serve_planet_stats():
    data = serve_surv_stats()
    print(data)

def serve_stats():
    serve_planet_stats()