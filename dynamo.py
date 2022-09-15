import boto3
from boto3.dynamodb.conditions import Key
import uuid

dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table('spaceTrips')
table = dynamodb.Table('spaceTitanic')


def write_to_dynamo(contenido, resultado):
    data = {}
    data['uuid'] = uuid.uuid1().hex
    data['cryoSleep'] = contenido['cryoSleep']
    data['age'] = contenido['age']
    data['vip'] = contenido['vip']
    data['origin'] = contenido['origin']
    data['destination'] = contenido['destination']
    data['transported'] = str(resultado)
    x = table.put_item(Item=data)
    #print(x)

def get_db_items():
    items = table.scan()
    print(items)
    return items[0]['Items']

def serve_planet_stats():
    planets = {}
    items = get_db_items()
    for item in items:
        if item.transported:
            planets[item['origin']] += 1
    return planets
    
def serve_stats():
    serve_planet_stats()