import boto3
import botocore
import os
import sys
from urllib.parse import unquote_plus
import urllib.request

import requests
import json
import datetime
from requests.auth import HTTPBasicAuth

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

thousandeyes_user = os.environ['THOUSANDEYES_USER']
thousandeyes_token = os.environ['THOUSANDEYES_TOKEN']
tousanndeyes_agentname = 'thousandeyes-va'
if ('THOUSANDEYES_AGENTNAME' in os.environ):
    tousanndeyes_agentname = os.environ['THOUSANDEYES_AGENTNAME']

# LINE notify's API
LINE_TOKEN = os.environ['LINE_TOKEN']
LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"
line_ok_msg = os.environ['LINE_OK_MSG']
line_ng_msg = os.environ['LINE_NG_MSG']

s3_bucket = os.environ['S3_BUCKET']

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

def send_info(msg):
    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}
    payload = {"message": msg}
    try:
        payload = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)

def agent_status():

    url = "https://api.thousandeyes.com/v6/agents.json"

    # Initialize the requests session
    api_session = requests.Session()

    response = api_session.request("GET", url, auth=HTTPBasicAuth(thousandeyes_user, thousandeyes_token), verify=False)

    # If successfully able to get list of flows
    if (response.status_code == 200):

        agents = json.loads(response.content)["agents"]
        for agent in agents:
            #print(json.dumps(flow, indent=4)) # formatted print
            if (agent['agentName'] == tousanndeyes_agentname):
                print(agent['agentState'])
                print(agent['lastSeen'])
                if (agent['agentState'] == 'Offline'):
                    print('Offline line_ng_msg: %s' % line_ng_msg)
                    try:
                        s3.Object(s3_bucket, 'status_ng').load()
                    except botocore.exceptions.ClientError as e:
                        if e.response['Error']['Code'] == "404":
                            # The object does not exist.
                            print('send NG message')
                            s3.Object(s3_bucket, 'status_ng').put()
                            send_info(line_ng_msg)
                        else:
                            # Something else has gone wrong.
                            raise
                    else:
                        # The object does exist.
                        print('continue NG')
                elif (agent['agentState'] == 'Online'):
                    print('Online line_ok_msg: %s' % line_ok_msg)
                    try:
                        s3.Object(s3_bucket, 'status_ng').load()
                    except botocore.exceptions.ClientError as e:
                        if e.response['Error']['Code'] == "404":
                            # The object does not exist.
                            print('continue OK')
                        else:
                            # Something else has gone wrong.
                            raise
                    else:
                        # The object does exist.
                        print('send OK message')
                        s3.Object(s3_bucket, 'status_ng').delete()
                        send_info(line_ok_msg)

    else:
        print("An error has ocurred, while fetching agentlists, with the following code {}".format(response.status_code))

def lambda_handler(event, context):
    agent_status()
