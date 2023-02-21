from flask import Flask,g, render_template, request, url_for, session, redirect
import pyrebase
import random
import string
import json
import urllib
from datetime import datetime, timedelta

class Admin:
    def __init__(self, Name, userid, password):
        self.username = Name
        self.userid = userid
        self.password = password
        
    def getId(self):
        return self.userid
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
       
class Database:
    instance = None
    database = None
    firebaseConfig = { "apiKey": "AIzaSyAQLecwEpL7BsfFyofqFElqYwqSTk3V8rI",
                         "authDomain": "yusir-5dde8.firebaseapp.com",
                         "projectId": "yusir-5dde8",
                         "storageBucket": "yusir-5dde8.appspot.com",
                         "messagingSenderId": "156912255880",
                         "appId": "1:156912255880:web:b57af8723161a92032703d",
                         "measurementId": "G-YPJ5FF9FLE",
                         "databaseURL": "https://yusir-5dde8-default-rtdb.europe-west1.firebasedatabase.app/"}       
    def __init__(self):
        self.instance = pyrebase.initialize_app(self.firebaseConfig)
        print("Initialized")
        
    def connect(self):
        try:
            print ("Connecting")
            self.database = self.instance.database()
        except Exception as e:
            print("Connection failed")

    def StoreData(self, table, key, value):
        try:
            self.database.child(table).child(key).set(value)
            print("stored")
        except Exception as e:
            print("Store failed "+ str(e))

    def RetriveData(self, table, key):
        try:
            return self.database.child(table).child(key).get().val()
        except Exception as e:
            print("Retrive failed")
    
    def RetriveTable(self, table):
        try:
            return self.database.child(table).get().val()
        except Exception as e:
            print("Retrive failed")
    
    def UpdateData(self, table, key, value): # value should be a dictionary in json format
        try:
            self.firebase.child(table).child(key).update(value)
        except Exception as e:
            print("Update failed")
        
    def DeleteData(self, table, key):
        try:
            self.firebase.child(table).child(key).remove()
        except Exception as e:
            print("Update failed")
    
    def DatabaseTestURL(self):
        status = urllib.request.urlopen(self.firebaseConfig["databaseURL"]).getcode()
        if status == 200:
            return "Database Exists"
        else:
            return "Database Not Found"   
    def __str__(self) -> str:
        pass
           
def randomID(chars = string.ascii_uppercase + string.digits + string.ascii_lowercase, N=10):
	    return ''.join(random.choice(chars) for _ in range(N))
 
class intersection:
    
    def __init__(self, intersectionName, originPosition, line1Position, line2position, line3position, line4position, is_Work, admin_id):
        self.intersectionID = randomID()
        self.intersectionName = intersectionName
        self.position = originPosition
        self.line1Position = line1Position
        self.line2Position = line2position
        self.line3Position = line3position
        self.line4Position = line4position
        self.is_Work = is_Work
        self.admin_id = admin_id
        
    def addIntersectionToSystem(self, connection):
        #using db object to store traffic light data
        connection.StoreData("Intersection", self.intersectionID, {"intersectionID": str(self.intersectionID), 
                                                                   "intersectionName": str(self.intersectionName), 
                                                                   "position":str(json.dumps(self.position.__dict__)),
                                                                   "line1Position":str(json.dumps(self.line1Position.__dict__)), 
                                                                   "line2Position":str(json.dumps(self.line2Position.__dict__)), 
                                                                   "line3Position":str(json.dumps(self.line3Position.__dict__)), 
                                                                   "line4Position":str(json.dumps(self.line4Position.__dict__)), 
                                                                   "is_Work":str(self.is_Work), "admin_id":str(self.admin_id)})

    def deleteIntersection(self, connection):
        connection.deleteData("Intersection", self.intersectionID)

    def updateIntersection(self, connection):
        connection.updateData("Intersection", self.intersectionID, {"intersectionID": str(self.intersectionID), 
                                                                   "intersectionName": str(self.intersectionName), 
                                                                   "position":str(self.position), 
                                                                   "line1Position":str(self.line1Position), 
                                                                   "line2Position":str(self.line2Position), 
                                                                   "line3Position":str(self.line3Position), 
                                                                   "line4Position":str(self.line4Position), 
                                                                   "is_Work":str(self.is_Work), "admin_id":str(self.admin_id)})
        
    def getIntersection(self, connection):
        connection.RetriveData("Intersection", self.intersectionID)

class Location:
    
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class highResults:
    def __init__(self, timeOfReult, greenTime, intersectionID):
        self.timeOfResult = timeOfReult
        self.greenTime = greenTime
        self.intersectionID = intersectionID
        
    def addHighResultsToSystem(self, connection):
        connection.StoreData("HighResults", self.timeOfResult, {"greenTime": str(self.greenTime), "intersectionID": str(self.intersectionID)})
########################################################################################################################

conn = Database()
conn.connect()
#print (conn.DatabaseTestURL())
timestamp = 0 #it should be set before take data from google maps api
admins = []
################################################################################################################
#########Store google maps api information######
def saveGoogleMapsData(time , speed, Location_of_data, intersection_id):
    GoogleMapData = {"arrival_time": speed, "Location_of_data": Location_of_data, "intersection_id": intersection_id}
    conn.StoreData("GoogleMapsData", time, GoogleMapData)
#how to invoke
#saveGoogleMapsData(timestamp.strftime("%Y-%m-%d %H:%M:%S") ,"20", str(json.dumps(Location("34.05024","-118.24102").__dict__)),"elZ9BWdVWk")
#########Store results##########################
#before this method we should invoke timestamp of calculate results
def seveResults(time_of_result, greenTime, location_of_result, data_time):
    Results = {"result_timestamp":time_of_result,"Green_Light_Time":greenTime, "Location_of_result": location_of_result, "Data_timestamp": data_time}
    conn.StoreData("Results", time_of_result, Results) 
#how should invoked
#seveResults(timestamp.strftime("%Y-%m-%d %H %M %S"),"62",str(json.dumps(Location("34.05024","-118.24102").__dict__)), str(timestamp - datetime.timedelta(seconds=9)))
##########Store high results####################
# data = highResults("2023-02-09 07:50:15", "79", "elZ9BWdVWk")
# data.addHighResultsToSystem(con)
################################################################################################################
     
app = Flask(__name__)   
app.secret_key = '5#y2L"F4Q8z'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
  
@app.before_request
def before_request():
    g.user = None
    # session.permanent = True
    # app.permanent_session_lifetime = timedelta(minutes=5)
    #########Admins information################ 
    information =  json.loads(json.dumps(conn.RetriveData("Admin","")))
    for i in information:
        admins.append(Admin(information[i]["username"],i ,information[i]["password"]))
    
    if 'user_id' in session:
        users = [x for x in admins if x.userid == session['user_id']][0]
        g.user = users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    print("hi")
    error_statement = " "
    if request.method == 'POST':
        session.pop('user_id', None)
        userid = request.form.get('ID')
        password = request.form.get('Password')
        user = [x for x in admins if x.userid == userid]      
        if user: 
            if user[0].getPassword() == password:
                session['user_id'] = user[0].getId()
                return redirect(url_for('home'))
        else:
            error_statement = 'Invalid username or password'
    return render_template('login.html', error_statement=error_statement)

# Ensure responses aren't cached
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/home', methods=['GET','POST'])
def home():
    if 'user_id' in session:
        a = conn.RetriveTable("Intersection")
        b = conn.RetriveTable("HighResults")
        intersections =[]
        results = []
        for i in a:
            x = intersection(a[i]["intersectionName"],a[i]["position"],a[i]["line1Position"],a[i]["line2Position"],a[i]["line3Position"],a[i]["line4Position"],a[i]["is_Work"],a[i]["admin_id"])
            intersections.append(x.intersectionName) 
        
        for j in b:
            y = highResults(j, b[j]["greenTime"], b[j]["intersectionID"])
            results.append(y.greenTime)
        if len(results) < 7:
            lastIndex = len(results) - 1
            for i in range(lastIndex):
                results.append(0) 
        #here where we should work if we talk about more than one week
        # for j in b:
        #     y = highResults(j, b[j]["greenTime"], b[j]["intersectionID"])
        #     results[(len(results)-1) % 7].append(y.greenTime)
        # if len(results[(len(results)-1) % 7]) < 7:
        #     lastIndex = len(results[(len(results)-1) % 7]) - 1
        #     for i in range(lastIndex):
        #         results[(len(results)-1) % 7].append(0) 
                        
        g.results = results
        
        if intersections == []:
            intersection_name = "Intersection"
        else:
            intersection_name = intersections[0]
        intersection_stat="True"
        if request.method == 'GET':
            if request.args.get('int_name') != None:
                intersection_name = request.args.get('int_name')
                for i in a:
                    x = intersection(a[i]["intersectionName"],a[i]["position"],a[i]["line1Position"],a[i]["line2Position"],a[i]["line3Position"],a[i]["line4Position"],a[i]["is_Work"],a[i]["admin_id"])
                    if x.intersectionName == intersection_name:
                        intersection_name = intersection_name
                        if x.is_Work == "True":
                            intersection_stat="working"
                        else:
                            intersection_stat="Out of service"        
        return render_template('home.html',intersection_name = intersection_name,intersection_stat = intersection_stat,intersections = intersections) 
    
    return redirect(url_for('login') )

@app.route('/terms', methods=['GET','POST'])
def terms():
    return render_template('terms.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/addIntersection', methods=['GET','POST'])
def addIntersection():
    if request.method == 'POST':
        intersectionName = request.form.get("intersectionName")
        intersectionOrigin = Location(request.form.get("latitudeP0"), request.form.get("longitudeP0"))
        Line1 = Location(request.form.get("latitudeP1"), request.form.get("longitudeP1"))
        Line2 = Location(request.form.get("latitudeP2"), request.form.get("longitudeP2"))
        Line3 = Location(request.form.get("latitudeP3"), request.form.get("longitudeP3"))
        Line4 = Location(request.form.get("latitudeP4"), request.form.get("longitudeP4"))
        TL = intersection(intersectionName, intersectionOrigin, Line1, Line2, Line3, Line4, True, g.user.userid)
        TL.addIntersectionToSystem(conn)
    return render_template('addTrifficLight.html')


if __name__ == '__main__':
    app.run()