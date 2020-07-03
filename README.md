# AffinityPropagation
# Language: Python
# Input: CSV (network)
# Output: prefix (cluster and centroids files)
# Tested with: PluMA 1.0, Python 3.6
# Dependency: sklearn==0.21.0

PluMA plugin that runs the Affinity Propagation (AP) clustering algorithm (Frey and Dueck, 2007).
AP is particularly useful when finding clusters in a signed and weighted network, and you do not
know the number of clusters in advance.  AP operates by finding exemplar nodes that represent
each cluster and uses message passing to determine these exemplars.

Expected input is a CSV file representing the network, where rows and columns both represent
nodes and entry (i, j) is the weight of the edge from node i to node j.

The output CSV file of clusters will be in the following format:


"","x"
"1","Family.Lachnospiraceae.0001"
"2","Family.Ruminococcaceae.0003"
"3","Family.Lachnospiraceae.0029"
"4","Family.Lachnospiraceae.0043"
"5","Family.Ruminococcaceae.0019"
"6","Family.Lachnospiraceae.0095"
"","x"
"1","Family.Porphyromonadaceae.0005"
"2","Family.Porphyromonadaceae.0006"
"3","Family.Lachnospiraceae.0045"
"4","Order.Clostridiales.0007"
"","x"
"1","Kingdom.Bacteria.0001"
"2","Family.Porphyromonadaceae.0013"
"3","Phylum.Firmicutes.0004"
.....


Each "","x" marks the start of a new cluster.  Note PluMA also has a ClusterCSV2NOA plugin
that can convert a file like this to a NOde Attribute (NOA) file for Cytoscape.  Nodes
can then be visualized using their cluster identifier as an attribute.

The output file of centroids will be similar to the above, with one for each cluster and its corresponding centroid.

Output files will be (prefix).AP.csv and (prefix).centroids.csv
