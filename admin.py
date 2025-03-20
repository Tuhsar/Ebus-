from mymongo import db
import logging
logging.basicConfig(filename='ebus.log', level=logging.DEBUG)


class Admin:
    def __init__(self, adminid, password):
      self.id = adminid
      self.password = password
       
       
    def login(self):      
      admin = db['admin']
      detail = admin.find_one({'admin id': self.id})
      try: 
            logging.info("Admin is Trying to LogIn")
            len(detail)
            logging.info('Admin id found, trying to match password')
      except:
            logging.info('no matching id for admin')
            return 0
      if self.password == detail['password'] :
            logging.info('admin logged in')
            return 1
      else :
            logging.info('invalid password by admin')
            return 2
   
    def createdriver(adminid, driverid, password):
      data = {'driver id': driverid, 'password': password, 'Under admin': adminid}
      drivers =  db['driver']
      detail = drivers.find_one({'driver id': data['driver id']})
      try:
         len(detail)
         logging.info('driver id is exist cannot add this driver with this id')
         return 0
      except:
         drivers.insert_one(data)
         logging.info('Driver added successfully')
         return 1
     
     # this method is not implemented due to complexity
     # hence while The Person assigning Admin Id at the same point of a time 
     # an Agency is Given by default
    def createagency(self, agencyname):
       agency = db['agency']
       detail = agency.find_one({'admin id': self.id,'agency': agencyname.strip()})
       try:
          len(detail)
       except:
          agency.insert_one({'admin id': self.id, 'agency': agencyname.strip()})
          logging.info(f'"{self.id}" admin added a agency {agencyname}')
          return 1
       else:
          logging.info('Agency name already exist cannot create the same')
          return 0
       
    def agency(self):
       agency = db['agency']
       detail = agency.find_one({'admin id': self.id})
       agencyname = detail['agency']
       return agencyname
