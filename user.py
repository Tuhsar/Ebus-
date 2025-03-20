from mymongo import db
import logging
logging.basicConfig(filename='ebus.log', level=logging.DEBUG)
from flask import render_template
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
    def register(self, firstname, lastname, email, password):
        logging.info('User is Registring')
        users = db['users']
        record = users.count_documents({'email': email})
        if record==0:
            users.insert_one({'firstname': firstname, 'lastname':lastname, 'email': email , 'password': password})
            logging.info('User Registered Successfully')
            return 1
        else: 
            logging.info('User mail already exist')
            return 0
   
    def login(self):
        logging.info('User is Logging in')
        users = db['users']
        record = users.find_one({'email': self.email})
        
        try: 
            len(record)
        except:
            logging.debug('Not a valid email')
            return 0
        if self.password == record['password']:
            return 1
        else: 
            logging.info('Invalid Credentials')        
            return 2

    def searchbus(self, source,destination):
        bus= db['bus']
        results = bus.find({ "info.0": source , "info.1": destination })
        size = bus.count_documents({ "info.0": source , "info.1": destination })
        if size > 0 :
            return results
        else:
            return 0    

    
# below code will be transferred to application module
