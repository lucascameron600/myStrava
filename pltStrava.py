#from FileParser import lat,lon,ele,hrs,time
import numpy as np
import matplotlib.pyplot as plt
from Workout import Workout
from Person import Person
from matplotlib.backends.backend_pdf import PdfPages

Lucas = Person("Luke", 25, 72, 215, 76)
fakewrkout = 'Afternoon_Run.gpx'
Workout1 = Workout(fakewrkout, Lucas)

min_hr = np.min(Workout1.hrs)
max_hr = np.max(Workout1.hrs)
hr_range = max_hr - min_hr

print("MIN")
print(min_hr)
print("MAX")
print(max_hr)
print("RANGE")
print(hr_range)
print("STD")
print(np.std(Workout1.hrs))
print("VAR")
print(np.var(Workout1.hrs))
print("AVG HR")
avgHR = np.mean(Workout1.hrs)
print(avgHR)



print(Workout1.getHrZones())

#plt.hist(hrs)
#plot heart rate in histogram and send to pdf
with PdfPages('heart_rate_histogram.pdf') as pdf:

    histEdges = Workout1.getHrZones()
    zoneLabels = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']

    binCenters = [(histEdges[i] + histEdges[i+1]) / 2 for i in range(len(histEdges)-1)]
    plt.xticks(binCenters, zoneLabels)


    plt.hist(Workout1.hrs, bins=histEdges, color='red', edgecolor='black')

    plt.axvline(avgHR, color='black', linestyle='--', label=f'Mean: {avgHR:.1f} bpm')

    plt.xlabel('Heart Rate (bpm)')
    plt.ylabel('Frequency')
    plt.title('Heart Rate Distribution')
    plt.grid(True)
    pdf.savefig()
    plt.close()

cals = Workout1.calories_burned()
bounds = Workout1.calcHrConf()

print(f'Total Duration in Mins {Workout1.getDuration()}')
print(f"{Lucas.name} burned {cals:.2f} calories.")
print(f'Bounds are {bounds}')
print(f'Total percent in each zone {Workout1.getZonePercents()}')
print(f'Total Distance Traveled = {Workout1.getDistanceTraveled()}')
print(f'Average pace is {Workout1.getAvgPace()} min per mile')
