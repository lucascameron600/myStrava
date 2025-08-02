#from FileParser import lat,lon,ele,hrs,time
import numpy as np
import matplotlib.pyplot as plt
from Workout import Workout
from Person import Person
from matplotlib.backends.backend_pdf import PdfPages


class genPlot:
        
    
    def __init__(self, workout):
        self.workout = workout
        
    #def loopData(self, folderofworkouts):
        
    def genAll(self, ax):
        #generates a histogram showing how much time was spent in each heart rate zone
        #formatting stuff
        histEdges = self.workout.getHrZones()
        zones = self.workout.getHrZones()
        zoneLabels = [
            f'Z1 {zones[0]:.1f}-{zones[1]:.1f}',
            f'Z2 {zones[1]:.1f}-{zones[2]:.1f}',
            f'Z3 {zones[2]:.1f}-{zones[3]:.1f}',
            f'Z4 {zones[3]:.1f}-{zones[4]:.1f}',
            f'Z5 {zones[4]:.1f}-{zones[5]:.1f}'
            ]
            
        binCenters = [(histEdges[i] + histEdges[i+1]) / 2 for i in range(len(histEdges)-1)]
        ax.set_xticks(binCenters)  
        ax.set_xticklabels(zoneLabels, rotation =30)
        
        ax.hist(self.workout.hrs, bins=histEdges, color='red', edgecolor='black')
        
        ax.axvline(self.workout.getAvgHr(), color='black', linestyle='--', label=f'Mean: {self.workout.getAvgHr():.1f} bpm')
        ax.set_xlabel('Heart Rate (bpm)')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Heart Rate Distribution for {self.workout.workoutname}')
        ax.grid(True)
        

        
        
    def genPacePlot(self, ax):
        #generates a dot plot connected showing pace over duration of workout
        
        self.workout.time = self.workout.time * 60
        
        #turn time into fractional hours
        dist = np.array(self.workout.dist)
        time = np.array(self.workout.time[:len(dist)])
        
        #only plot every ten seconds so that its not so many points
        time = time[::10]
        dist = dist[::10]
        
        #get the difference between each index
        deltaTime = np.diff(time)
        deltaDist = np.diff(dist)
        
        #random numpy stuff
        N = np.arange(len(time) +1)
        N = N[:-2]
        
        #divide time by distance
        paceMin = np.divide(deltaTime, deltaDist, out=np.zeros_like(deltaDist))
        
        #filter anything over two std away from mean this is to filter out stopped time but it
        #should be done way better
        #paceStd = np.std(paceMin)
        #paceMean = np.mean(paceMin)
        #paceMask = np.abs(paceMin - paceMean) <= .2 * paceStd 

        lower = np.percentile(paceMin, 5)
        upper = np.percentile(paceMin, 95)
        paceMask = (paceMin >= lower) & (paceMin <= upper)

        filteredPaceMin = paceMin[paceMask]
        filteredN = N[paceMask]
        
        ax.plot(filteredN, filteredPaceMin, marker='.', color='blue')
        ax.set_xticks([0, (np.size(N)-1)*.25, (np.size(N)-1)*.5, (np.size(N)-1)/2, (np.size(N)-1)*.75, np.size(N)-1])
        ax.axhline(self.workout.getAvgPace(), color='black', linestyle='--', label=f'Mean: {self.workout.getAvgPace():.1f} Min/Mile')   
        ax.set_xticklabels([f'0',f'{round((self.workout.getDistanceTraveled())*.25,2)}',f'{round((self.workout.getDistanceTraveled())*.5,2)}',f'{round((self.workout.getDistanceTraveled())/2,2)}',f'{round((self.workout.getDistanceTraveled())*.75,2)}',f'{round(self.workout.getDistanceTraveled(),2)}'])
        
        ax.set_xlabel("Distance (miles)")
        ax.set_ylabel("Pace (min/mile)")
        ax.set_title(f"Pace Over Distance for {self.workout.workoutname}")
        ax.grid(True)


    #def gen3DPlot(self, ax):