import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv, json
def request_O_CAR():
    url = "http://www.data4citizen.jp/app/users/openDataOutput/json/get/O_CAR_TRAFFIC_DATA"
    #parameter = {'measurement_hour': 10, 'patrol_car_name': '237', 'limit': 100, 'measurement_date': '2014/02/28',"gps_error_meter" : 2}
    parameter = {'car_name': "patrol01", 'measurement_data_id': '20151030_162045', 'limit': 10000 }

    r = requests.post(url,parameter).json()
    if str(r["result"]) == u"fail":
        print("failed")
        return
    jsonData = r["data"]
    csvData = json2csv(jsonData)
    f = open("some.csv","w")
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

def plotMAP(result):
    x = list()
    y = list()
    px = list()
    py = list()
    mx = list()
    my = list()

    for r in result:
        r = json.loads(r)
        x.append(float(r["longitude"]))
        y.append(float(r["latitude"]))
        if float(r["accel_y_longitudinal"])<0 and float(r["accel_x_transverse"]) < 0:
            mx.append(float(r["longitude"]))
            my.append(float(r["latitude"]))
        else:
            px.append(float(r["longitude"]))
            py.append(float(r["latitude"]))
    plt.plot(x, y,alpha = 0.3)

    plt.scatter(px, py, c= "red",alpha = 0.1)
    plt.scatter(mx, my, c= "blue",alpha = 0.1)

    plt.show()
#request()



if __name__ == '__main__':
    request_O_CAR
    result = []
    with open('some.csv') as f:
        for line in csv.DictReader(f):
            line_json = json.dumps(line)
            result.append(line_json)
    plotMAP(result)
