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
@app.route('/v1/register/')	# obsolete; will likely remove 
def register():
	pi_ip_port = (request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'])
	print("pi_ip_port = " + str(pi_ip_port))
	pi_ip_port_file = open('/root/car-cloud/pi_ip_port.txt', 'w')
	pi_ip_port_file.write(str(pi_ip_port))
	pi_ip_port_file.close()
	#call(['echo', 'Pi address registered'])
	return Response(status=200)
	

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)


