from mymongo import db

def records():
    cities = db['cities']
    cityname = []
    for i in cities.find():
        cityname.append(i['name'])
    
    cityname.sort()
    
    return cityname
# additional functionalities to be addded in this module
# we can add city that does not exist in cities collection

