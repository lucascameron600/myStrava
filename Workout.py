from Person import Person
from Helpers import pounds_to_kilos
import re
import numpy as np
import scipy.stats as st
from math import radians, cos, sin, asin, sqrt, atan2, degrees

class Workout:


    def __init__ (self, workoutgpx, person, workoutname):

        self.workoutgpx = workoutgpx
        self.workoutname = workoutname
        self.lat, self.lon, self.ele, self.hrs, self.time = self.parseGpx()
        self.person = person
       # self.elevationGain =
        self.avgHeartRate = np.mean(self.hrs)
        self.totalDurationMins = np.size(self.time) / 60
        self.caloriesBurned = self.calories_burned()
        self.dist = np.array([])
        self.getDistanceTraveled()
        
    def __gt__(self, other):
        return (self.getZonePercents()[1] > other.getZonePercents()[1])

        
    def parseGpx(self):
        def extractTime(line):
            hour = float(line[17:19])
            minute = float(line[20:22])
            second = float(line[23:25])
            t = hour + minute/60.0 + second/3600.0
            return t

        def extractLatLon(line):
            row = line.split('"')
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

        lat = []
        lon = []
        ele = []
        hrs = []
        time = []
        filename = self.workoutgpx
        l = getLines(filename)
        fid = open(filename)
        ctr = 0
        dp = 10.0
        p = 0.0
        for line in fid:
            if len(line) > 4:
                line = line.replace(" ","")
                if line[0:6] == "<time>":
                    t = extractTime(line)
                    time.append(t)
                if line[0:9] == "<trkptlat":
                    lt,ln = extractLatLon(line)
                    lat.append(lt)
                    lon.append(ln)
                if line[0:11] == "<gpxtpx:hr>":
                    hr = extractHr(line)
                    hrs.append(hr)
                if line[0:5] == "<ele>":
                    el = extractEle(line)
                    ele.append(el)
            ctr+=1
        print('Percentage Complete = ',100.0)

        time = time[1:]
        lat = np.array(lat)
        lon = np.array(lon)
        ele = np.array(ele)
        hrs = np.array(hrs)
        time = np.array(time)-6

        #elevation in ft
        ele = ele*3.28
        return(lat,lon,ele,hrs,time)


    def getDuration(self):
        return self.totalDurationMins

    def getAvgHr(self):
        return np.sum(self.hrs)/np.size(self.hrs)

    def MET(self):
        MET = .05 * self.getAvgHr() +2
        return MET


    def calories_burned(self):
        weight_kg = pounds_to_kilos(self.person.weight)
        calories = self.MET() * weight_kg * (self.totalDurationMins / 60)
        return calories


    def getHrZones(self):

        ## take the age height and weight and return heart rate zones 1-5 in a range

        MaxHR = 220 - self.person.age
        
        ReserveHR = MaxHR - self.person.RestHR

        calc = ReserveHR + self.person.RestHR

        zone1low = (.50 * ReserveHR) +self.person.RestHR
        zone1high = (.60 * ReserveHR)+ self.person.RestHR

        zone2low = (.60 * ReserveHR) +self.person.RestHR
        zone2high = (.70 * ReserveHR)+ self.person.RestHR

        zone3low = (.70 * ReserveHR) +self.person.RestHR
        zone3high = (.80 * ReserveHR)+ self.person.RestHR

        zone4low = (.80 * ReserveHR) +self.person.RestHR
        zone4high = (.90 * ReserveHR)+ self.person.RestHR

        zone5low = (.90 * ReserveHR) +self.person.RestHR
        zone5high = ( ReserveHR)+ self.person.RestHR


        zone1range= (zone1low,zone1high)
        zone2range= (zone2low,zone2high)
        zone3range= (zone3low,zone3high)
        zone4range= (zone4low,zone4high)
        zone5range= (zone5low,zone5high)
        ##return range return[zone1range,zone2range,zone3range,zone4range,zone5range]
        return zone1low,zone2low,zone3low,zone4low,zone5low,zone5high

    def calcHrConf(self):
       sizeOfHrs = np.size(self.hrs)
       m = np.mean(self.hrs)
       s = np.std(self.hrs)
       t = st.t(sizeOfHrs-1).ppf(.95)
       lb = m - t * s /np.sqrt(sizeOfHrs)
       ub = m + t * s /np.sqrt(sizeOfHrs)

       return((lb,ub))

    def getZonePercents(self):
        zones = self.getHrZones()
        zoneCounts = []
        zoneLabels = {'Z1','Z2','Z3','Z4','Z5'}
        for i in range(5):
            lower = zones[i]
            upper = zones[i+1]
            countThisZone = np.count_nonzero((self.hrs >= lower) & (self.hrs < upper))
            zoneCounts.append(countThisZone)


        total = np.size(self.hrs)
        totalPercents = []
        for count in zoneCounts:
            totalPercents.append((count / total *100))
        return totalPercents

    def getAvgPace(self):
        return self.getDuration()/self.getDistanceTraveled()
    
    
    
#   def getPacePerMile(self):
#       duration = self.getDuration() 
#       distanceTraveled = self.getDistanceTraveled()
#       milePaces = []
#       mileMarkers = []
#       
#       for dis in self.dist
#           

    def getDistanceTraveled(self):
        distance = 0.0
        distancelist = []
        for i in range(1, np.size(self.lat)):
            distance += self.haversine(self.lat[i-1], self.lon[i-1], self.lat[i], self.lon[i])
            distancelist.append(distance)
        self.dist = distancelist
        return distance

    #put this somewhere else bro I dont want this static method lingering in my workout class
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 3956 # Radius of earth in miles
        return c * r


