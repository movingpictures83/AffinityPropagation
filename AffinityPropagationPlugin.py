import sys
import math
#import numpy
from CSV2GML.CSV2GMLPlugin import *
#random_state = None
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

def unquote(s):
   return s[1:len(s)-1]


class AffinityPropagationPlugin(CSV2GMLPlugin):
   #def input(self, filename):
      # Will produce self.bacteria, self.n and self.ADJ
      #CSV2GMLPlugin.input(self,filename)

   def removeSingletonsAndPureVillains(self):
      n = len(self.ADJ)
      singletons = []
      self.singletonbac = []

      for i in range(n):
         count = 0
         for j in range(n):
            if (i != j and self.ADJ[i][j] > 0):
               count += 1
         if (count == 0):
            singletons.append(i)
            self.singletonbac.append(self.bacteria[i])

      newADJ = []
      for i in range(n):
         if not i in singletons:
            newrow = []
            for j in range(n):
               if not j in singletons:
                  newrow.append(self.ADJ[i][j])
            newADJ.append(newrow)
      self.ADJ = newADJ

      for bac in self.singletonbac:
         self.bacteria.remove(bac)


   def run(self):
      CSV2GMLPlugin.run(self)
      #print("INDEX:"),
      #print(self.bacteria.index('\"Streptosporangiales\"'))
      eps = 1e-8
      ap = AffinityPropagation(preference=0,damping=0.5,affinity='precomputed',convergence_iter=200)
      self.removeSingletonsAndPureVillains()
      #print("INDEX:"),
      #print(self.bacteria.index('\"Streptosporangiales\"'))
      #print("EDGES:")
      #i = self.bacteria.index('\"Streptosporangiales\"')
      #for j in range(len(self.ADJ[i])):
      #      if (i != j and self.ADJ[i][j] != 0):
      #         print(self.bacteria[j])
      af = ap.fit(self.ADJ)
      self.cluster_centers_indices = af.cluster_centers_indices_
      self.labels = af.labels_
      self.n_clusters_ = len(self.cluster_centers_indices)
      #print(self.labels)
      #print(self.labels[i])
      # Mark singletons, will remove when printing
      cluster = 0
      for i in range(0, len(self.cluster_centers_indices)):
         cluster_size = 0
         for label in self.labels:
            if (label == cluster):
               cluster_size += 1
         #print("CLUSTER SIZE: "+str(cluster_size))
         if (cluster_size <= 1):
            self.cluster_centers_indices[i] = -1 # Mark
         cluster += 1

   def output(self, filename):
      filestuff = open(filename+".AP.csv", 'w')
      centroidfile = open(filename+".centroids.noa", 'w')
      #centroidfile.write("\"\",\"x\"\n")
      centroidfile.write("Name\tCentroid\n")
      cluster = 0
      printedcluster = 1
      for index in self.cluster_centers_indices:
       if (index != -1):
         filestuff.write("\"\",\"x\"\n")
         #centroidfile.write("\""+str(printedcluster)+"\","+self.bacteria[index].strip()+"\n")   
         centroidfile.write(unquote(self.bacteria[index].strip())+"\t"+unquote(self.bacteria[index].strip())+" (C)\n")   
         count = 0
         innercount = 1
         for label in self.labels:
            if (label == cluster):
               filestuff.write("\""+str(innercount)+"\","+self.bacteria[count].strip()+"\n")
               innercount += 1
            count += 1
         printedcluster += 1
       cluster += 1
 
      for index in range(len(self.bacteria)):
          if (index not in self.cluster_centers_indices):
              centroidfile.write(unquote(self.bacteria[index].strip())+"\t"+unquote(self.bacteria[index].strip())+"\n")
      for bac in self.singletonbac:
          centroidfile.write(unquote(bac.strip())+"\t"+unquote(bac.strip())+"\n")
      return




