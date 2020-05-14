import sys
import math
#import numpy
from CSV2GML.CSV2GMLPlugin import *

from sklearn.cluster import AffinityPropagation
#from sklearn import metrics
#from sklearn.datasets.samples_generator import make_blobs

def readClusterFile(myfile):
   clusters = []
   filestuff = open(myfile, 'r')
   for line in filestuff:
      vals = line.split(',')
      if (vals[0] == "\"\""):
          clusters.append([])
      else:
          clusters[len(clusters)-1].append(vals[1][1:len(vals[1])-3].strip())
   return clusters

def inSameCluster(bac1, bac2, clusters):
   if (bac1[0] == '\"'):
      bac1 = bac1[1:len(bac1)-1]
      bac2 = bac2[1:len(bac2)-1]
   for i in range(len(clusters)):
      if (clusters[i].count(bac1) > 0):
         if (clusters[i].count(bac2) > 0):
            return True
         else:
            return False



class AffinityPropagationPlugin(CSV2GMLPlugin):
   #def input(self, filename):
      # Will produce self.bacteria, self.n and self.ADJ
      #CSV2GMLPlugin.input(self,filename)

   def removeSingletonsAndPureVillains(self):
      n = len(self.ADJ)
      singletons = []
      singletonbac = []

      for i in range(n):
         count = 0
         for j in range(n):
            if (self.ADJ[i][j] > 0):
               count += 1
         if (count == 0):
            singletons.append(i)
            singletonbac.append(self.bacteria[i])

      newADJ = []
      for i in range(n):
         if not i in singletons:
            newrow = []
            for j in range(n):
               if not j in singletons:
                  newrow.append(self.ADJ[i][j])
            newADJ.append(newrow)
      self.ADJ = newADJ

      for bac in singletonbac:
         self.bacteria.remove(bac)


   def run(self):
      CSV2GMLPlugin.run(self)
      eps = 1e-8
      ap = AffinityPropagation(preference=0,affinity='precomputed',convergence_iter=200)
      self.removeSingletonsAndPureVillains()
      af = ap.fit(self.ADJ)
      self.cluster_centers_indices = af.cluster_centers_indices_
      self.labels = af.labels_
      self.n_clusters_ = len(self.cluster_centers_indices)
      

   def output(self, filename):
      filestuff = open(filename+".AP.csv", 'w')
      centroidfile = open(filename+".centroids.csv", 'w')
      centroidfile.write("\"\",\"x\"\n")
      cluster = 0
      for index in self.cluster_centers_indices:
         filestuff.write("\"\",\"x\"\n")
         centroidfile.write("\""+str(cluster)+"\","+self.bacteria[index].strip()+"\n")   
         count = 0
         innercount = 1
         for label in self.labels:
            if (label == cluster):
               filestuff.write("\""+str(innercount)+"\","+self.bacteria[count].strip()+"\n")
               innercount += 1
            count += 1
         cluster += 1
 
      return




