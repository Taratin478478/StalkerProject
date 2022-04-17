import requests
from pprint import pprint
import json
import numpy as np
from scipy.optimize import fsolve

class InexactFloat(float):
    def __eq__(self, other):
        try:
            return abs(self.real - other) / (0.5 * (abs(self.real) + abs(other))) < 0.01
        except ZeroDivisionError:
            # Could do another inexact comparison here, this is just an example:
            return self.real == other

    def __ne__(self, other):
        return not self.__eq__(other)

class Anomaly:
    def __init__(self, id, coords, rate):
        self.id = id
        self.coords = coords
        self.rate = rate


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
            raw_anomalies[anomaly["id"]].append([detector["coords"], anomaly["rate"]])
        else:
            raw = [[detector["coords"], anomaly["rate"]]]
            raw_anomalies[anomaly["id"]] = raw
pprint(raw_anomalies)
for anomaly in raw_anomalies.values():
    print(anomaly)
    br = False
    x1, y1 = anomaly[0][0]
    x2, y2 = anomaly[1][0]
    x3, y3 = anomaly[2][0]
    for x in range(40):
        for y in range(30):
            for k in range(0, 1000):
                k = k / 100
                r1 = (k / anomaly[0][1]) ** 0.5
                r2 = (k / anomaly[1][1]) ** 0.5
                r3 = (k / anomaly[2][1]) ** 0.5
                if InexactFloat((x1 - x) ** 2 + (y1 - y) ** 2) == InexactFloat((r1 * k) ** 2)\
                        and InexactFloat((x2 - x) ** 2 + (y2 - y) ** 2) == InexactFloat((r2 * k) ** 2)\
                        and InexactFloat((x3 - x) ** 2 + (y3 - y) ** 2) == InexactFloat((r3 * k) ** 2):
                    print(x, y, k)
                    br = True
                    break
            if br:
                break
        if br:
            break

# (x1 - xc) ** 2 + (y1 - yc) ** 2 = (r1 * k) ** 2
# (x2 - xc) ** 2 + (y2 - yc) ** 2 = (r2 * k) ** 2
# (x3 - xc) ** 2 + (y3 - yc) ** 2 = (r3 * k) ** 2
#
#
#
