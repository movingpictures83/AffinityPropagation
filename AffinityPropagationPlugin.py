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
            #print "Removing edge ", bac1, " to ", bac2
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
      ap = AffinityPropagation(preference=0,affinity='precomputed')
      self.removeSingletonsAndPureVillains()
      print len(self.ADJ)
      af = ap.fit(self.ADJ)
      self.cluster_centers_indices = af.cluster_centers_indices_
      self.labels = af.labels_
      self.n_clusters_ = len(self.cluster_centers_indices)
      #print cluster_centers_indices
      #print labels 

      #print dir(af)
      #print af.affinity_matrix_
      
      #s = numpy.zeros([self.n, self.n])
      #self.a = numpy.zeros([self.n, self.n])
      #self.r = numpy.zeros([self.n, self.n])

      # Initialize s(i, k), k != i
      # And all a(i, k) = 0
      #simsum = 0
      #numedges = 0.0
      #for i in range(self.n):
      #   for k in range(self.n):
      #      if (i != k):
      #         s[i][k] = abs(self.ADJ[i][k])
               #simsum += self.ADJ[i][k]
               #numedges += 1
      #      self.a[i][k] = 0

      # Initialize s(k, k)
      # Should it be zero?  Not sure.
      #for k in range(self.n):
      #   s[k][k] = 0#simsum / numedges

      #maxdiff = 1
      #while (maxdiff > eps):
         # Set r(i, k)
      #   maxdiff = eps
      #   for i in range(self.n):
      #      for k in range(self.n):
      #         maximum = -1
      #         for kprime in range(self.n):
      #            if (kprime != k):
      #               tmp = self.a[i][kprime] + s[i][kprime]
      #               if (tmp > maximum):
      #                  maximum = tmp
      #         old = self.r[i][k]
      #         self.r[i][k] = s[i][k] - maximum
      #         diff = abs(self.r[i][k] - old)
      #         if diff > maxdiff:
      #            maxdiff = diff

         # Set a(i, k)
      #   for i in range(self.n):
      #      for k in range(self.n):
      #         sum = 0
      #         for iprime in range(self.n):
      #            if (iprime != i and iprime != k):
      #               sum += max(0, self.r[iprime][k])
      #         old = self.a[i][k]
      #         self.a[i][k] = min(0, self.r[k][k] + sum)
      #         diff = abs(self.a[i][k] - old)
      #         if diff > maxdiff:
      #            maxdiff = diff

         # Set a(k, k)
      #   for k in range(self.n):
      #      sum = 0
      #      for iprime in range(self.n):
      #         if (iprime != k):
      #               sum += max(0, self.r[iprime][k])
      #      old = self.a[k][k]
      #      self.a[k][k] = sum
      #      diff = abs(self.a[k][k] - old)
      #      if diff > maxdiff:
      #         maxdiff = diff

         # Output (for now)
         #for k in range(self.n):
         #   print self.bacteria[k], self.a[k][k]

      #   for i in range(self.n):
      #      for k in range(i+1, self.n):
      #         print "Rik: ", self.r[i][k], " Rki: ", self.r[k][i], " Aik: ", self.a[i][k], " Aki: ", self.a[k][i]

      #   print "MAXDIFF: ", maxdiff
      #   raw_input()

   def output(self, filename):
      #print('Estimated number of clusters: %d' % self.n_clusters_)
      filestuff = open(filename, 'w')

      #print "Cluster Centers and Sizes: "
      cluster = 0
      for index in self.cluster_centers_indices:
         filestuff.write("\"\",\"x\"\n")
         
         #print "****************************************" 
         #print self.bacteria[index], ":"
         count = 0
         innercount = 1
         for label in self.labels:
            if (label == cluster):
               filestuff.write("\""+str(innercount)+"\","+self.bacteria[count].strip()+"\n")
               innercount += 1
            count += 1
         #if (count > 1):
         #print "****************************************" 
         cluster += 1
 
      return




