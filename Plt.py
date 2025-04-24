#from FileParser import lat,lon,ele,hrs,time
import numpy as np
import matplotlib.pyplot as plt
from Workout import Workout
from Person import Person
from matplotlib.backends.backend_pdf import PdfPages

class genPlot:

    def __init__(self, workout):
        self.workout = workout

    def genAll(self, ax):

        histEdges = self.workout.getHrZones()
        zoneLabels = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']

        binCenters = [(histEdges[i] + histEdges[i+1]) / 2 for i in range(len(histEdges)-1)]

        ax.set_xticks(binCenters)  
        ax.set_xticklabels(zoneLabels)
        
        ax.hist(self.workout.hrs, bins=histEdges, color='red', edgecolor='black')

        ax.axvline(self.workout.getAvgHr(), color='black', linestyle='--', label=f'Mean: {self.workout.getAvgHr():.1f} bpm')

        ax.set_xlabel('Heart Rate (bpm)')
        ax.set_ylabel('Frequency')
        ax.set_title('Heart Rate Distribution')
        ax.grid(True)
        #pdf.savefig()

    def genPacePlot(self, ax):
        