import time
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv, json
import math
import pylab
import glob
ORG = {
    'utime' : 'measurement_ms',
    'point' : {'x' :'longitude','y' : 'latitude'},
    'ay' : 'accel_y_longitudinal',
    'ax' : 'accel_x_transverse'
}
requestLoad = [
    {"car_name":"patrol01",'measurement_data_id' : "20151030_162045", 'limit': 10000 },
    {"car_name":"patrol01",'measurement_data_id' : "20151110_091224", 'limit': 10000 },
    {"car_name":"patrol01",'measurement_data_id' : "20151112_124852", 'limit': 10000 },
    {"car_name":"patrol01",'measurement_data_id' : "20151113_105429", 'limit': 10000 },
    {"car_name":"patrol02",'measurement_data_id' : "20151027_083459", 'limit': 10000 },
    {"car_name":"patrol02",'measurement_data_id' : "20151217_130656", 'limit': 10000 },
    {"car_name":"patrol02",'measurement_data_id' : "20151218_083934", 'limit': 10000 }]

def request_O_CAR(car_id = 0):

    url = "http://www.data4citizen.jp/app/users/openDataOutput/json/get/O_CAR_TRAFFIC_DATA"
    #parameter = {'measurement_hour': 10, 'patrol_car_name': '237', 'limit': 100, 'measurement_date': '2014/02/28',"gps_error_meter" : 2}
    parameter = requestLoad[car_id]
    print parameter
    r = requests.post(url,parameter).json()
    if str(r["result"]) == u"fail":
        return
    jsonData = r["data"]
    csvData = json2csv(jsonData)
    f = open("data/"+requestLoad[car_id]["car_name"]+"_"+requestLoad[car_id]["measurement_data_id"]+".csv","w")
    f.write(csvData)
    len(csvData)
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
def plotMAP(jsonArray,axis):
    x = list()
    y = list()
    for r in jsonArray:
        x.append(float(r[ORG["point"]["x"]]))
        y.append(float(r[ORG["point"]["y"]]))
    axis.plot(x, y,alpha = 0.3)

def AccelMAP(jsonArray):
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
def timeAccelPlot(jsonArray):
    x = list()
    y = list()
    for i in jsonArray:
        x.append(float(i[ORG["utime"]]))
        y.append(float(i[ORG["ay"]]))
    plotScatter(x,y)

def accelPlot(jsonArray):
    x = list()
    y = list()
    for i in jsonArray:
        x.append(float(i[ORG["ay"]]))
        y.append(float(i[ORG["ax"]]))
    plotScatter(x,y)

def accelPlot(jsonArray,axis):
    x = list()
    y = list()
    for i in jsonArray:
        if 0.2 < math.fabs(float(i[ORG["ax"]])):
            x.append(float(i[ORG["ay"]]))
            y.append(float(i[ORG["ax"]]))
    axis.plot(x, y,alpha = 0.3)

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
        time = float(i[time_name])
        if begin_utime < time and time < finish_utime:
            result.append(i)
    return result
def getfiles():
    files = glob.glob("*.csv")
    fig,axis = plt.subplots(len(files),sharex = True,sharey=True)
    for i in range(len(files)):
        data = csv2jsonArray(files[i])
        print(len(data))
        accelPlot(data,axis[i])
        #plotMAP(data,axis[i])
    fig.show()
if __name__ == '__main__':
    #request_O_CAR()
    #plot(result)
    #sideAccelPlot(result)

    result = csv2jsonArray("patrol02_20151218_083934.csv")
    timeAccelPlot(result)
    plt.show()

    resultw = csv2jsonArray("patrol01_20151030_162045.csv")
    AccelPlot(resultw)
    plt.show()
    bu = 1445902542940
    fu = 1446189836007
    #extracted_time(bu,fu,result)
    #timePlot(fx,fy)
