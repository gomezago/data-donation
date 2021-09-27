import requests
import time
import datetime

THING_URL = "https://dwd.tudelft.nl/bucket/api/things"

def new_thing(name, description, data):
    thing = {
        'name' : name,
        'description' : description,
        'type' : data,
        'pem' : None,
    }
    return thing

def new_property(name, description, type):
    property = {
        'name' : name,
        'description' : description,
        'type' : type,
        'typeId' : type,
    }
    return property

def new_consent(subjects, actions):
    consent = {
        'subjects' : subjects,
        'actions' : actions,
    }
    return consent

def new_group(id, members):
    group = {
        'id' : 'dcd:groups:'+id,
        'members' : members,
    }
    return group

def create_thing(thing, token):
    hed = {'Authorization': 'bearer ' + token['access_token']}
    response = requests.post(THING_URL, json=thing, headers=hed)
    return response

def get_thing_count(token):
    COUNT_THING_URL = f'https://dwd.tudelft.nl/bucket/api/things/count/'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'from' : 0, 'to': round(time.time()*1000)}
    response = requests.get(COUNT_THING_URL,headers=hed, params=par)
    return response

def delete_thing(thingId, token):

    DELETE_THING_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId}
    response = requests.delete(DELETE_THING_URL,headers=hed, params=par)
    return response

def create_property(thingId, property, token,):

    CREATE_PROPERTY_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId}
    response = requests.post(CREATE_PROPERTY_URL, json=property, headers=hed, params=par)
    return response

def delete_property(thingId, propertyId, token):

    DELETE_PROPERTY_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId, 'propertyId': propertyId}
    response = requests.delete(DELETE_PROPERTY_URL, json=property, headers=hed, params=par)
    return response

def update_property(thingId, propertyId, values, token):
    UPDATE_PROPERTY_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId, 'propertyId': propertyId}

    response = requests.put(UPDATE_PROPERTY_URL, json=values, headers=hed, params=par)
    return response


def grant_consent(thingId, propertyId, consent, token):

    GRANT_CONSENT_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}/consents'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId, 'propertyId': propertyId}

    response = requests.post(GRANT_CONSENT_URL, json=consent, headers=hed, params=par)
    return response


def list_consent(thingId, propertyId, token):

    LIST_CONSENT_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}/consents'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId, 'propertyId': propertyId}

    response = requests.get(LIST_CONSENT_URL, headers=hed, params=par)
    return response

def create_group(group, token):

    CREATE_GROUP_URL = "https://dwd.tudelft.nl/profile/api/groups/"

    hed = {'Authorization': 'bearer ' + token['access_token']}

    response = requests.post(CREATE_GROUP_URL, json=group, headers=hed)
    return response

def get_groups(token):

    CREATE_GROUP_URL = "https://dwd.tudelft.nl/profile/api/groups/"

    hed = {'Authorization': 'bearer ' + token['access_token']}

    response = requests.get(CREATE_GROUP_URL, headers=hed)
    return response

def list_property_types(token):

    LIST_PROPERTY_TYPE_URL = "https://dwd.tudelft.nl/bucket/api/types/"

    hed = {'Authorization': 'bearer ' + token['access_token']}

    response = requests.get(LIST_PROPERTY_TYPE_URL, headers=hed)
    return response

def read_property_data(thingId, propertyId, token):

    READ_PROPERTY_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId, 'propertyId': propertyId, 'from' : 0, 'to': round(time.time()*1000)} # Start and End Timestamps
    response = requests.get(READ_PROPERTY_URL, headers=hed, params=par)

    return response

def read_property_data_month(thingId, propertyId, token):
        READ_PROPERTY_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}'

        start = int((datetime.datetime.now() - datetime.timedelta(days=30)).timestamp() * 1000)
        end = int((datetime.datetime.now().timestamp() * 1000))

        hed = {'Authorization': 'bearer ' + token['access_token']}
        par = {'thingId': thingId, 'propertyId': propertyId, 'from': start,
               'to': end}  # Start and End Timestamps
        response = requests.get(READ_PROPERTY_URL, headers=hed, params=par)

        return response

def get_property_count(thingId, propertyId, token):

    COUNT_PROPERTY_URL = f'https://dwd.tudelft.nl/bucket/api/things/{thingId}/properties/{propertyId}/count/'

    hed = {'Authorization': 'bearer ' + token['access_token']}
    par = {'thingId': thingId, 'propertyId': propertyId, 'from' : 0} # From the start...
    response = requests.get(COUNT_PROPERTY_URL, headers=hed, params=par)

    return response