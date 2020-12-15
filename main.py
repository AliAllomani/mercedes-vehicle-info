#!/usr/bin/python

import os
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import flask
from MBClient import MBClient

app = flask.Flask(__name__)



demo = os.environ.get('MB_IS_DEMO', "false") == "true"

if demo:
    app.logger.warning('RUNNING DEMO MODE')
    api_endpoint = r'https://api.mercedes-benz.com/vehicledata_tryout/v2'
    vin = 'WDB111111ZZZ22222'
else:
    api_endpoint = r'https://api.mercedes-benz.com/vehicledata/v2'
    vin = os.environ.get('MB_VIN')

client_id = os.environ.get('MB_CLIENT_ID')
client_secret = os.environ.get('MB_CLIENT_SECRET')
redirect_uri = os.environ.get('MB_REDIRECT_URL')


client = MBClient(client_id, client_secret, redirect_uri)


@app.route('/callback')
def callback():
    client.state = session.get('oauth_state','')
    session['oauth_token'] = client.get_oauth_token(request.url)
    return flask.redirect(location=url_for("index"))


@app.route('/login')
def login():
    authorization_url, state = client.login()
    session['oauth_state'] = state
    return flask.redirect(location=authorization_url)

@app.route('/')
def index():

    if demo:
        #access_token = {'access_token': '3c3c333c-l123-4123-s123-3c3c333c3c33'}
        access_token = {'access_token': '4c4c444c-v123-4123-s123-4c4c444c4c44'}
    else:
        access_token  = session.get('oauth_token',{})

    if len(access_token) == 0:
        return flask.redirect(location=url_for("login"))

    client.access_token = access_token

    response = {}

    response['resources'] = client.get_resource("{}/vehicles/{}/resources".format(api_endpoint, vin))
    response['vehiclestatus'] = client.get_resource("{}/vehicles/{}/containers/vehiclestatus".format(api_endpoint, vin))
    response['vehiclelockstatus'] = client.get_resource("{}/vehicles/{}/containers/vehiclelockstatus".format(api_endpoint, vin))

    return jsonify(response)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run(host='localhost', port=3000, ssl_context=('cert.pem', 'key.pem'))
