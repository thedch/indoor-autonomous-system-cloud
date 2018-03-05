from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call
import datetime 
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = '/root/ians_cloud/app/db/database.db'
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

@app.route('/v1/robot_go')
def robot_go():
	#call(['echo', 'robot_go'])
    call(['mosquitto_pub', '-t', 'robot/killSwitch', '-m', 'robot go'])
    return redirect("http://35.229.88.91", code=302)

@app.route('/v1/robot_stop')
def robot_stop():
	#call(['echo', 'robot_stop'])
    call(['mosquitto_pub', '-t', 'robot/killSwitch', '-m', 'robot stop'])
    return redirect("http://35.229.88.91", code=302)

@app.route('/v1/robot_receive_map', methods=['POST'])
def robot_receive_map():
    #database = get_db()
   # imagefile = request.files.get('imagefile', '')
    #request.form['image'].save('/file.jpg')
    #filename_build = "map-" + datetime.date.today().strftime("%B-%d-%Y") 
    request.files['map.png'].save('./app/static/map.png') 
    
    #minspec return, no checking
    return "wassup" 
#    print( request.form['name'])


'''
@app.route('/v1/updateDst', methods = ['POST'])
def updateDst():
	call(['mosquitto_pub', '-t', 'robot/dst', '-m', request.form])
'''

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)


