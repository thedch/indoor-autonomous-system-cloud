from flask import Flask
from flask import request, redirect, url_for
from flask import Response
from subprocess import call
import datetime 
import os
from flask import g, session, abort, render_template, flash

SERVER_ADDR = "http://35.197.98.244"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods = ['GET', 'POST'])
def homepage():
    try:
        map_file = open("current_map.txt", "r")
        current_map = map_file.read().strip('\n')
        map_file.close()
    except IOError:
        # if there is no current_map.txt, assume BE1 and create the file
        current_map = "be1"
        map_file = open("current_map.txt", "w")
        map_file.write(current_map)
        map_file.close()
    return render_template('map_rendering.html', current_map=current_map) 

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
    request.files['map.png'].save('./app/static/map.png') 
    
    #minspec return, no checking
    return "success" 
    #print(request.form.get['name'])

@app.route('/v1/robot_submit', methods=['POST'])
def send_goal_and_initial_pose():
    # check that method is POST
    if request.method != "POST":
        return "bad request"
    # get params from request, convert to strings of floats and send to robot
    dst = str(request.form.get('dst'))
    # get current map
    try:
        map_file = open("current_map.txt", "r")
        current_map = map_file.read().strip('\n')
        map_file.close()
    except IOError:
        # if there is no current_map.txt, assume BE1 and create the file
        current_map = "be1"
        map_file = open("current_map.txt", "w")
        map_file.write(current_map)
        map_file.close()

    initial_position = str(request.form.get('initial_position'))
    # map from point number to its coordinates
    if current_map == "be3":
        if initial_position == "1":
            initial_position = "-43.3 14.4"
        if initial_position == "2":
            initial_position = "-67.5 1.5"
        if initial_position == "3":
            initial_position = "-12.1 2.25"
    if current_map == "be1":
        if initial_position == "1":
            initial_position = "19.1 14.9"
        if initial_position == "2":
            initial_position = "-38.6 4.0"
        if initial_position == "3":
            initial_position = "-37.6 27.6"
        if initial_position == "4":
            initial_position = "-5.4 -3.4"

    call(['mosquitto_pub', '-t', 'robot/initial_pose', '-m', initial_position])

    # translate from point number to its coordinates
    if current_map == "be3":
        if dst == "1":
            dst = "-43.3 14.4"
        if dst == "2":
            dst = "-67.5 1.5"
        if dst == "3":
            dst = "-12.1 2.25"
    if current_map == "be1":
        if dst == "1":
            dst = "19.1 14.9"
        if dst == "2":
            dst = "-38.6 4.0"
        if dst == "3":
            dst = "-37.6 27.6"
        if dst == "4":
            dst = "-5.4 -3.4"

    call(['mosquitto_pub', '-t', 'robot/dst', '-m', dst])


    return redirect(SERVER_ADDR, code=302)

@app.route('/v1/robot_select_map', methods=['POST'])
def select_map():
    if request.method != "POST":
        return "bad request"
    current_map = str(request.form.get('choose_map'))
    map_file = open("current_map.txt", "w")
    map_file.write(current_map)
    map_file.close()
    return redirect(SERVER_ADDR, code=302)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80) 


