from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call
import datetime 
import sqlite3
from flask import g
import ssl

SERVER_ADDR = "http://35.197.98.244"
current_map = "be3"

'''
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain('/root/ca/intermediate/certs/ca-chain.cert.pem',
        keyfile='/root/ca/intermediate/private/35.229.88.91.key.pem',
        password="12345")
'''

app = Flask(__name__)

DATABASE = '/root/indoor-autonomous-system-cloud/app/db/database.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/", methods = ['GET', 'POST'])
def homepage():
    return app.send_static_file('index.html') 

@app.route('/v1/robot_start_mapping')
def startMapping():
    #call(['echo', 'robot_go'])
    call(['mosquitto_pub', '-t', 'robot/mapping', '-m', 'robot start mapping'])
    return redirect(SERVER_ADDR, code=302)

@app.route('/v1/robot_stop_mapping')
def stopMapping():
    #call(['echo', 'robot_stop'])
    call(['mosquitto_pub', '-t', 'robot/mapping', '-m', 'robot stop mapping'])
    return redirect(SERVER_ADDR, code=302)

@app.route('/v1/robot_toggle_motor_disable')
def toggleKillSwitch():
    call(['mosquitto_pub', '-t', 'robot/motor_disable', '-m', 'toggle'])
    return redirect(SERVER_ADDR, code=302)

@app.route('/v1/robot_receive_map', methods=['POST'])
def robot_receive_map():
    #database = get_db()
    #imagefile = request.files.get('imagefile', '')
    #request.form.get['image'].save('/file.jpg')
    #filename_build = "map-" + datetime.date.today().strftime("%B-%d-%Y") 
    request.files['map.png'].save('./app/static/map.png') 
    
    #minspec return, no checking
    return "wassup" 
    #print(request.form.get['name'])

@app.route('/v1/robot/submit', methods=['POST'])
def send_goal_and_initial_pose():
    # check that method is POST
    if request.method != "POST":
        return "bad request"
    # get params from request, convert to strings of floats and send to robot
    dst = str(request.form.get('dst'))
    print("dst = " + dst)
    if dst == "1":
        dst = "1.0 1.0"
    if dst == "2":
        dst = "2.0 2.0"
    if dst == "3":
        dst = "3.0 3.0"
    if dst == "4":
        dst = "4.0 4.0"
    call(['mosquitto_pub', '-t', 'robot/dst', '-m', dst])

    initial_position = str(request.form.get('initial_position'))
    if initial_position == "1":
        initial_position = "1.0 1.0"
    if initial_position == "2":
        initial_position = "2.0 2.0"
    if initial_position == "3":
        initial_position = "3.0 3.0"
    if initial_position == "4":
        initial_position = "4.0 4.0"

    facing = str(request.form.get('facing'))
    
    initial_pose = initial_position + " " + facing
    print("initial_pose = " + initial_pose)
    call(['mosquitto_pub', '-t', 'robot/initial_pose', '-m', initial_pose])

    return redirect(SERVER_ADDR, code=302)



if __name__ == '__main__':
    #context = ('/root/indoor-autonomous-system-cloud/server.cert', '/root/indoor-autonomous-system-cloud/server.key') 
    app.run(host="0.0.0.0", port=80) #ssl_context=context)


