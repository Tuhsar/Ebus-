from flask import Flask,render_template,request,redirect
import logging
logging.basicConfig(filename='ebus.log', level=logging.DEBUG, format='%(asctime)s -%(levelname)s-%(message)s')
from user import User  
from admin import Admin 
from driver import Driver
from cities import records

application =  Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')


# admin route


@application.route('/adminlogin')
def adminlogin():
   logging.info('admin login page loaded to enter id and paasword') 
   return render_template('adminlogin.html') 
   

@application.route('/admin', methods = ['POST'])
def admin():
  try:
    id = request.form['ID']
    password = request.form['Password']
    a = Admin(id,password)
    result = a.login()
    if result ==1:
        agency = a.agency()
        return render_template('admin.html', agency = agency, adminid = id)
    elif result==0:
        return render_template('adminlogin.html', msg = 'Wrong Admin Id')
    else: 
        return render_template('adminlogin.html', msg = 'Invalid Credentials')
  except:
      logging.warning('Admin Login Failed')
      
      
@application.route('/createdriver/<adminid>', methods=["POST"])
def createdriver(adminid):
  try:  
    driver = request.form['DID']
    password = request.form['Password']
    add = Admin.createdriver(adminid,driver,password)
    if add == 0:
        return render_template('admin.html', adminid=adminid, msg='Driver Already Exist')
    elif add==1:
        return render_template('admin.html', adminid=adminid, msg='Driver Added')
    else:
        return 'Some error occured'
  except:
      logging.warning(f'Driver creation failed by admin id={adminid}')

# ----------------------------------driver route ------------------------------------------------

@application.route('/driverlogin')
def driverlogin():
    return render_template('driverlogin.html')

@application.route('/driver', methods = ['POST'])
def driver():
    id = request.form['DID']
    password = request.form['Password']
    d = Driver(id,password)
    result = d.login()
    if result ==1:
        citynames = records()
        return render_template('driver.html', driverid = id, citynames = citynames)
    elif result==0:
        return render_template('driverlogin.html', msg = 'Wrong Driver Id')
    else: 
        return render_template('driverlogin.html', msg = 'Invalid Credentials')

@application.route('/postbusinfo/<driverid>', methods=['POST'])
def postdetails(driverid):
    source = request.form['source']
    destination = request.form['destination']
    day = request.form['day']
    time = request.form['time']
    bustype = request.form['bus-type']
    contact = request.form['contact']
    info = (source, destination, day,time)
    postdetail = Driver.postbusinfo(driverid, bustype, contact, *info )
    if postdetail == 1:
        return render_template('driver.html',driverid = driverid, msg = 'Bus Details Posted', citynames = records())
    else:
        return render_template('driver.html',driverid = driverid, msg = 'Some issue occured')



# ----------------------------------- user route ----------------------------------------------------


@application.route('/userlogin')
def userlogin():
    return render_template('userlogin.html')


@application.route('/user', methods=["POST"])
def user():
    id = request.form['ID']
    password = request.form['Password']
    u = User(id, password)
    result = u.login()
    if result == 0:
        return render_template('userlogin.html', msg = 'Invalid Id')
    elif result == 1:
        return render_template('user.html', citynames = records() )
    elif result ==2 :
        return render_template('userlogin.html', msg='Invalid credentials')
    
    
@application.route('/busdetails', methods=['POST'])
def busdetails():
    src = request.form['source']
    dest = request.form['destination']
    u = User(None,None)
    result = u.searchbus(src, dest) 
    if result==0:
        return render_template('busdetails.html', msg = 'No Buses between', source = src , destination = dest, condition = False)
    else:
        return render_template('busdetails.html', details = result, condition=True)
    
@application.route('/registration')
def registration():
    return render_template('register.html')
    
@application.route('/register', methods=["POST"])
def register():
    fname = request.form['firstname']
    lname = request.form['lastname']
    email = request.form['email']
    password = request.form['Password']
    u = User(None, None)
    result = u.register(fname,lname,email,password)
    if result == 1:
        return render_template('userlogin.html', msg2 = "Now You Can Login")
    else:
        return render_template('register.html', msg = 'mail provided already exist try to login')
      
        
if __name__ == '__main__':
    application.run(debug=True)