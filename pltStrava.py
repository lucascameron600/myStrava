#from FileParser import lat,lon,ele,hrs,time
import numpy as np
import matplotlib.pyplot as plt
from Workout import Workout
from Person import Person
from matplotlib.backends.backend_pdf import PdfPages
from Plt import genPlot

Lucas = Person("Luke", 25, 72, 215, 76)
fakewrkout = 'Afternoon_Run.gpx'
Workout1 = Workout(fakewrkout, Lucas)
Plotter = genPlot(Workout1)
Plotter.genAll()
min_hr = np.min(Workout1.hrs)
max_hr = np.max(Workout1.hrs)
hr_range = max_hr - min_hr




print(Workout1.getHrZones())


fig, axes = plt.subplots(1,2, figsize=(12,5))

Plotter.genAll(axes[0])
Plotter.genAll(axes[])
plt.tight_layout()
plt.show()
cals = Workout1.calories_burned()
bounds = Workout1.calcHrConf()
for time in Workout1.distancelist
print("MIN HR")
print(min_hr)
print("MAX HR")
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
print(dist)
print(f'Total Duration in Mins {Workout1.getDuration()}')
print(f"{Lucas.name} burned {cals:.2f} calories.")
print(f'Bounds are {bounds}')
print(f'Total percent in each zone {round(Workout1.getZonePercents())}')
print(f'Total Distance Traveled = {Workout1.getDistanceTraveled()}')
print(f'Average pace is {Workout1.getAvgPace()} min per mile')

if Workout1 > Workout2:
    print('You spent more time in zone two in Workout1 signaling greater recovery capacity.')
else:
    print('You spent more time in zone two in Workout2')
