from mymongo import db
import logging
logging.basicConfig(filename='ebus.log', level=logging.DEBUG)

class Driver:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        
        
    def login(self):
        drivers =  db['driver']
        detail = drivers.find_one({'driver id': self.id})
        try: 
            len(detail)
            logging.info('Matched DID for driver')
        except:
            logging.info('no matching id for driver')
            return 0
        if self.password == detail['password'] :
            logging.info('driver logged in')
            return 1
        else :
            logging.info('invalid password for driver')
            return 2
        
    def postbusinfo(driverid, type, contact, *info):
       try:
        bus = db['bus']
        details = {'driver id': driverid, 'info': info, 'type' : type, 'contact': contact }
        bus.insert_one(details)
        logging.info('Bus info added')
        return 1
       except:
           logging.info('Bus info addition failed')
           return 0
       
       
#this similar code moves to application module
