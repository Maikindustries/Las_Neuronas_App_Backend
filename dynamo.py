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
    #print(items)
    return items['Items']

def serve_planet_stats():
    planets = [0, 0, 0]
    items = get_db_items()
    for item in items:
        if item['transported'] == '1':
            planets[int(item['origin'])] += 1
    result = {'Earth': planets[0], "Mars": planets[1], "Europe": planets[2]}
    return result

def serve_destination_stats():
    destinations = [0, 0, 0]
    items = get_db_items()
    for item in items:
        if item['transported'] == '1':
            destinations[int(item['destination'])] += 1
    result = {'55 Cancri e': destinations[0], "TRAPPIST-1e": destinations[1], "PSO J318.5-22": destinations[2]}
    return result
    
def serve_stats():
    serve_planet_stats()