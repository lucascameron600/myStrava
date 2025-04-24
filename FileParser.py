import numpy as np
import re

##Function to grab HH:MM:SS from <time>
def extractTime(line):
    #print(line)
    hour = float(line[17:19])
    #print('Hour = ',hour)
    minute = float(line[20:22])
    #print('Minute = ',minute)
    second = float(line[23:25])
    #print('Second = ',second)
    t = hour + minute/60.0 + second/3600.0
    return t

def extractLatLon(line):
    #print(line)
    row = line.split('"')
    #print(row)
    lt = float(row[1])
    ln = float(row[3])
    return lt,ln

def extractEle(line):
    el = "".join(c for c in line if not c.isalpha())
    el = el.replace("<>","")
    el = el.replace("</>","")
    el = float(el)
    return el

def extractHr(line):
    match = re.search(r'<gpxtpx:hr>(\d+)</gpxtpx:hr>', line)
    heart_rate = int(match.group(1))
    return heart_rate

def getLines(fullpath):
    length = 0
    file = open(fullpath)
    for line in file:
        length+=1
    file.close()
    print(fullpath,'LINES = ',length)
    return length



#READ IN STRAVA DATA

lat = []
lon = []
ele = []
hrs = []
time = []
filename = 'Afternoon_Run.gpx'
l = getLines(filename)
fid = open(filename)
ctr = 0
dp = 10.0
p = 0.0
for line in fid:
    #Notify user of progress
    if 100*(ctr/l) >= p:
        print('Percentage Complete = ',p)
        p+=dp
    #Make sure the line is over 4 characters
    if len(line) > 4:
        #remove all the spaces
        line = line.replace(" ","")
        #Search for time
        if line[0:6] == "<time>":
            ##Grab just the hour, minute and seconds
            t = extractTime(line)
            time.append(t)
        #Search for lat and lon
        if line[0:9] == "<trkptlat":
            lt,ln = extractLatLon(line)
            lat.append(lt)
            lon.append(ln)
        #Search for Heart Rate
        if line[0:11] == "<gpxtpx:hr>":
            hr = extractHr(line)
            hrs.append(hr)
        #Search for Elevation
        if line[0:5] == "<ele>":
            el = extractEle(line)
            ele.append(el)
    #Break for debugging
    ctr+=1
    #if ctr == 200:
    #    break
print('Percentage Complete = ',100.0)

#Time has an extra timestamp
time = time[1:]
#Convert to numpy arrays
lat = np.array(lat)
lon = np.array(lon)
ele = np.array(ele)
hrs = np.array(hrs)
time = np.array(time)-6
#Convert elevation to feet
ele = ele*3.28

