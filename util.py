import time
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv, json
import math
import pylab
ORG = {
    'utime' : 'measurement_datetime',
    'point' : {'x' :'longitude','y' : 'latitude'},
    'ay' : 'accel_y_longitudinal',
    'ax' : 'accel_x_transverse'
}

def request_O_CAR(name,car_id = 1):
    if car_id==1:
        car_name = "patrol01"
        car_data_id = "20151030_162045"
    elif car_id==2:
        car_name = "patrol02"
        car_data_id = "20151027_083459"

    url = "http://www.data4citizen.jp/app/users/openDataOutput/json/get/O_CAR_TRAFFIC_DATA"
    #parameter = {'measurement_hour': 10, 'patrol_car_name': '237', 'limit': 100, 'measurement_date': '2014/02/28',"gps_error_meter" : 2}
    parameter = {'car_name': car_name, 'measurement_data_id': car_data_id, 'limit': 10000 }

    r = requests.post(url,parameter).json()
    if str(r["result"]) == u"fail":
        print("failed")
        return
    jsonData = r["data"]
    csvData = json2csv(jsonData)
    f = open(name,"w")
    f.write(csvData)
    f.close()

def json2csv(jsonData):
    jsonKey=list(jsonData[0].keys())
    csvData = ""
    for i,key in enumerate(jsonKey):
        if i < len(jsonKey)-1:
            csvData=csvData+'"'+key+'"'+','
        elif i== len(jsonKey)-1:
            csvData=csvData+'"'+key+'"'+'\n'

    for i,value in enumerate(jsonData):
        for ii,key in enumerate(jsonKey):
            if ii < len(jsonKey)-1:
                csvData=csvData+'"'+str(value[key])+'",'
            elif ii== len(jsonKey)-1:
                csvData=csvData+'"'+str(value[key])+'"\n'
    return csvData

def plotMAP(jsonArray):
    if jsonArray is None:
        return
    x = list()
    y = list()
    for r in jsonArray:
        x.append(float(r[ORG["point"]["x"]]))
        y.append(float(r[ORG["point"]["y"]]))
    plt.plot(x, y,alpha = 0.3)

def sideAccelMAP(jsonArray):

    mx = list()
    my = list()
    px = list()
    py = list()
    plotMAP(jsonArray)
    for r in jsonArray:
        if float(r[ORG["ay"]]) < -0.1:
            mx.append(float(r[ORG["point"]["x"]]))
            my.append(float(r[ORG["point"]["y"]]))
        else:
            px.append(float(r[ORG["point"]["x"]]))
            py.append(float(r[ORG["point"]["y"]]))
    plt.scatter(px, py, c= "red",alpha = 0.1)
    plt.scatter(mx, my, c= "blue",alpha = 0.1)

    plt.show()
def accelPlot(jsonArray):
    x = y = list()
    for i in jsonArray:
        x.append(i[ORG["ay"]])
        y.append(i[ORG["ax"]])
    plotScatter(x,y)
def plotScatter(x,y):
    plt.scatter(x, y,alpha = 0.3)

def parse(name,data):
    result = []
    for d in data:
        result.append(d[name])
    return result

def timePlot(x,y):
    pylab.ion()
    axis = pylab.gca()
    for i in range(100):
        pylab.plot(x[i],y[i])
        pylab.pause(0.0000000001)
        axis.clear()

def csv2jsonArray(name):
    result = []
    with open(name) as f:
        for line in csv.DictReader(f):
            line_json = json.dumps(line)
            line_json = json.loads(line_json)
            result.append(line_json)
    return result

def parse_and_float(name,data):
    d = parse(name,data)
    fd = [float(i) for i in d]
    return fd

def extracted_time(begin_utime,finish_utime,jsonArray,time_name = ORG["utime"]):
    result = []
    for i in jsonArray:
        time = float(t[time_name])
        if begin_utime < time and time < finish_utime:
            result.append(i)
    return result

if __name__ == '__main__':
    request_O_CAR()
    #plot(result)
    #sideAccelPlot(result)
    result = csv2jsonArray("some.csv")
    x = parse_and_float(ORG["ay"],result)
    y = parse_and_float(ORG["ax"],result)

    plotScatter(x,y)
    bu = 1445902542940
    fu = 1445902642942
    #extracted_time(bu,fu,result)
    #timePlot(fx,fy)
