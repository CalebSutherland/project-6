"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations

import os
import logging
import requests


# Set up Flask app
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)



##################################################
################### API Callers ################## 
##################################################



API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"


def get_brevet():
    """
    Obtains the newest document in the "lists" collection in database
    by calling the RESTful API.
    Returns title (string) and items (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    races = requests.get(f"{API_URL}/brevets").json()

    # lists should be a list of dictionaries.
    # we just need the last one:
    brevet = races[-1]
    return brevet["start_time"], races["brev_dist"], races["ckeckpoints"]


def insert_brevet(start_time, brev_dist, checkpoints):
    """
    Inserts a new to-do list into the database by calling the API.
    
    Inputs a title (string) and items (list of dictionaries)
    """
    _id = requests.post(f"{API_URL}/brevets", json={"start_time": start_time, "brev_dist": brev_dist, "checkpoints": checkpoints}).json()
    return _id



##################################################
################## Flask routes ################## 
##################################################



@app.route("/")
@app.route("/index")
def index():
    """
    Shows the home page.
    HTML interface: responds with an HTML.
    """
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


#################################################
# AJAX request handlers
# These return JSON, rather than rendering pages.
#################################################


@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brev_dist', 200, type=float)
    start_time = request.args.get('start_time', type=str)
    start = arrow.get(start_time, "YYYY-MM-DDTHH:mm")
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    app.logger.debug("start={}".format(start))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    open_time = acp_times.open_time(km, brevet_dist, start).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, start).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_brevet_insert", methods = ["POST"])
def insert():
    """
    /insert : inserts a to-do list into the database.
    Accepts POST requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        start_time = input_json["start_time"]
        brev_dist = input_json["brev_dist"]
        checkpoints = input_json["checkpoints"]

        brevet_id = insert_brevet(start_time, brev_dist, checkpoints)

        return flask.jsonify(result={},
                        message="Inserted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=brevet_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')


@app.route("/_brevet_fetch")
def fetch():
    """
    /fetch : fetches the newest to-do list from the database.
    Accepts GET requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:
        start_time, brev_dist, checkpoints = get_brevet()
        
        return flask.jsonify(
                result={"start_time": start_time, "brev_dist": brev_dist, "checkpoints": checkpoints}, 
                status=1,
                message="Successfully fetched a brevet!")
    except:
        return flask.jsonify(
                result={},
                status=0,
                message="Something went wrong, couldn't fetch any brevets")


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404



##################################################
################# Start Flask App ################ 
##################################################


if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")
