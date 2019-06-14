#!/usr/bin/python

import argparse
import requests
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument("--io",  type=lambda x: x.split(":"), action='append')
parser.add_argument("--ssl", action='append', default=None)
parser.add_argument("--username", type=lambda x: x.split(":"), action='append')
parser.add_argument("--password", type=lambda x: x.split(":"), action='append')
parser.add_argument('--sleep', default=0.05, type=float)
args = parser.parse_args()

class GudeDevice:
    def getJson(self, cgiParams):
        if self.ssl:
            url = 'https://'
        else:
            url = 'http://'

        url += self.host + '/' + 'status.json'

        if self.username is not None and self.password is not None:
            auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        else:
            auth = None

        r = requests.get(url, params=cgiParams, verify=False, auth=auth)

        if r.status_code == 200:
            return json.loads(r.text)
        else:
            raise ValueError("http request error {0}".format(r.status))

    def setOutput(self, output, outputState):
        json = self.getJson({'components': 1, 'cmd' : 1, 'p' : output, 's' : outputState})
        return json["outputs"][output-1]["state"]

    def getInputs(self):
        self.inputs = self.getJson({'components': 2})["inputs"]
        return self.inputs

    def setSsl(self, ssl):
        self.ssl = ssl

    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def setHost(self, host):
        self.host = host

    def __init__(self, host, ssl=False, username=None, password=None):
        self.inputs = []
        self.host = host
        self.ssl = ssl
        self.username = username
        self.password = password

devices = {}
for iocfg in args.io:
    for i in [0, 2]:
        if not devices.get(iocfg[i]):
            devices[iocfg[i]] = GudeDevice(iocfg[i])

if args.ssl is not None:
    for ssl in args.ssl:
        if ssl in devices:
            devices[ssl].setSsl(True)

if args.username is not None:
    for auth in args.username:
        if auth[0] in devices:
            devices[auth[0]].setUsername(auth[1])

if args.password is not None:
    for auth in args.password:
        if auth[0] in devices:
            devices[auth[0]].setPassword(auth[1])

while True:
    inputs = {}
    for iocfg in args.io:
        if not iocfg[0] in inputs:
            inputs[iocfg[0]] = devices[iocfg[0]].inputs
            devices[iocfg[0]].getInputs()
            if not len(inputs[iocfg[0]]):
                for i in range(0, len(devices[iocfg[0]].inputs)):
                    inputs[iocfg[0]].append(-1)

        if inputs[iocfg[0]][int(iocfg[1])-1] != devices[iocfg[0]].inputs[int(iocfg[1])-1]:
            devices[iocfg[2]].setOutput(int(iocfg[3]), int(devices[iocfg[0]].inputs[int(iocfg[1])-1]["state"]))
            print("{0} {1} input {2} : {3} -> {4} output {5}".format(time.strftime("%Y-%m-%d %H:%M:%S"), iocfg[0], iocfg[1], devices[iocfg[0]].inputs[int(iocfg[1]) - 1]["state"], iocfg[2], iocfg[3]))

    time.sleep(args.sleep)
