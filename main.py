import requests
from pprint import pprint
import json
import numpy as np
from scipy.optimize import fsolve

class InexactFloat(float):
    def __eq__(self, other):
        try:
            return abs(self.real - other) / (0.5 * (abs(self.real) + abs(other))) < 0.1
        except ZeroDivisionError:
            # Could do another inexact comparison here, this is just an example:
            return self.real == other

    def __ne__(self, other):
        return not self.__eq__(other)

class Anomaly:
    def __init__(self, id, x, y, rate):
        self.id = id
        self.x = x
        self.y = y
        self.rate = rate

    def okradius(self):
        return (k / 2) ** 0.5



'''
def eq1(p, r):
    x1, x2, x3, y1,y2, y3, r1, r2, r3 = p
    xc, yc, k = r
    return (x1 - xc) ** 2 + (y1 - yc) ** 2 - (r1 * k) ** 2, (x2 - xc) ** 2 + (y2 - yc) ** 2 - (r2 * k) ** 2, (x3 - xc) ** 2 + (y3 - yc) ** 2 - (r3 * k) ** 2
'''

data = requests.get('https://dt.miet.ru/ppo_it_final', headers={'X-Auth-Token': 'dzxylhiz'}).json()["message"]
raw_anomalies = dict()
for detector in data:
    for anomaly in detector["swans"]:
        if anomaly["id"] in raw_anomalies.keys():
            raw_anomalies[anomaly["id"]].append([detector["coords"], anomaly["rate"], anomaly["id"]])
        else:
            raw = [[detector["coords"], anomaly["rate"], anomaly["id"]]]
            raw_anomalies[anomaly["id"]] = raw
pprint(raw_anomalies)
anomalies = []
for anomaly in raw_anomalies.values():
    br = False
    x1, y1 = anomaly[0][0]
    x2, y2 = anomaly[1][0]
    x3, y3 = anomaly[2][0]
    for x in range(40):
        for y in range(30):
            for k in range(0, 1000):
                k = k / 10
                r1sq = k / anomaly[0][1]
                r2sq = k / anomaly[1][1]
                r3sq = k / anomaly[2][1]
                if InexactFloat((x1 - x) ** 2 + (y1 - y) ** 2) == InexactFloat(r1sq)\
                        and InexactFloat((x2 - x) ** 2 + (y2 - y) ** 2) == InexactFloat(r2sq)\
                        and InexactFloat((x3 - x) ** 2 + (y3 - y) ** 2) == InexactFloat(r3sq):
                    anomalies.append(Anomaly(anomaly[0][2], x, y, k))
                    br = True
                    break
            if br:
                break
        if br:
            break
for anomaly in anomalies:
    print(anomaly.id, anomaly.x, anomaly.y, anomaly.rate)
# (x1 - xc) ** 2 + (y1 - yc) ** 2 = (r1 * k) ** 2
# (x2 - xc) ** 2 + (y2 - yc) ** 2 = (r2 * k) ** 2
# (x3 - xc) ** 2 + (y3 - yc) ** 2 = (r3 * k) ** 2
#
#
#
