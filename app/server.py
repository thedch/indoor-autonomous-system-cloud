from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call

app = Flask(__name__)

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
'''
@app.route('/v1/updateDst', methods = ['POST'])
def updateDst():
	call(['mosquitto_pub', '-t', 'robot/dst', '-m', request.form])
'''

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)


