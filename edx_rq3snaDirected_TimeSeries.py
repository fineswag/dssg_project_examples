###########################
# Directed CSV Builder
# Jennifer De Boer (modified by Sam Finegold)
# RAPID Team
###########################

#!/usr/bin/python
# This first set of commands imports the necessary libraries for the commands that will be
# used to parse the files input from the database of discussion forum posts.

import sys
import json
import glob
import types
import collections
import re
import pprint
import datetime
from random import choice
import csv
import pprint
import StringIO
import csv
from itertools import combinations
from collections import defaultdict
from collections import Counter

# edx_ds (below) is a library developed by Daniel Seaton. The only function in the library required for this
# project is the one that creates a multi-dimensional dictionary, which is created below.

# import edx_ds 
	
# Builds multidimensional dictionary
def multi_dimensions(n, type):
  # """ Creates an n-dimension dictionary where the n-th dimension is of type 'type' 
  if n<=1:
    return type()
  return defaultdict(lambda:multi_dimensions(n-1, type))
  
#### Creating GEXF file for Social Network Analysis of 6.002x discussion forum #### 

# This first command builds off of Daniel's code to create a multi-dimensional dictionary
# format for nodes and their attributes.  The list of edges is a simple list, and the list of
# nodes is multi-dimensional so it can also store start and end times. More columns will be
# needed as more attribute data is stored.

nodelist = multi_dimensions(2,dict)
edgelist = multi_dimensions(2,dict)

csv.field_size_limit(1600000)

# We need to first open the csv file and then create an object through which we can iterate to 
# extract information from it.

f = open('/Users/samuelfinegold/Documents/harvard/edXresearch/snaCreationFiles/time_series/time_series.csv','rU')
reader = csv.DictReader(f, delimiter=',')

# Initialize a variable at one that will allow the edges to be organized by thread
thread_id_recorder = 1
	
for line in reader:
	person = line['author_id']
	# generate node list
	if person not in nodelist:
		nodelist[person]['start'] = line['time']
		nodelist[person]['end'] = line['time']
	else:
		if line[person]['start'] > line['time']:
			line[person]['start'] = line['time']
		if line[person]['end'] < line['time']:
			line[person]['end'] = line['time']
	
	# generate edge list
	type = line['types']
	if type == "Question":
		print "Question"
		source = line[author_id]
	else: 
		edgelist.append(source + line['author_id'] + line['time'])
		
	
	line['thread_id']
	if line['type'] == 'Question':
		print "T"
	else: 
		print "F"		

for line in reader:
	
		


# Here, we start a loop that will go through each row of the csv file and extract the 
# ids of the posters in the file as well as the date of the first and most recent threads
# in which they appear. Each poster is added to the node list and their start/end dates
# are changed as we go through every thread in the discussion forum. If you are using a 
# table which does not have dates, simply add an empty column with header dates. This will
# attach null cells to the row. 

# for line in reader:
# 	# Need to change so that using each author_id
#     posters = line['posters']
#     peeps = posters.split(" ")  
#     	         		
#     for person in peeps:
#         if person not in nodelist:
#             nodelist[person]["start"] = line['dates']
#             nodelist[person]["end"] = line['dates']
#         else:
#             if nodelist[person]["start"]>line['dates']:
#                 nodelist[person]["start"]=line['dates']
#             if nodelist[person]["end"]<line['dates']:
#                 nodelist[person]["end"]=line['dates']


# Right now, the only attributes associated with each node are its start and end date. As 
# our graph gets more sophisticated, we would add columns here that could contain 
# information such as whether or not students got a certificate, their country, etc.
# This would involve adding a second-level characteristic to the 2-level dictionary above
# and therefore adding a column to the csv file that we print out in the section that 
# follows.

hlist = ['start', 'end'] 

def csvwriter_twodim_dict(output_file,dim_one,header,input_dict):
    #Copy header, then add dim_one as a column
    tmpheader = []
    tmpheader = list(header)
    tmpheader.insert(0,dim_one) 
    
    #Open file handle
    file = open(output_file,'wb')

    writer = csv.DictWriter(file,fieldnames=tmpheader,restval=999,extrasaction='ignore')
    writer.writeheader()
    for key in sorted(input_dict.iterkeys()):
        #Coercing dimensions into one for csv writer
        tmpdict={}
        tmpdict = dict(input_dict[key])
        tmpdict[dim_one] = key
        writer.writerow(tmpdict)
	
    file.close()
    return None

# It is helpful to use this as a concrete example to understand how csvwriter_twodim_dict() works
csvwriter_twodim_dict('people_real.csv','person',hlist,nodelist)

# Right now, the connections between each set of two people are just captured in this list.
# Eventually, though, we would want to transition this simple list to a 2-level dictionary
# as well, wherein each edge has attributes.  In particular, we are interested in the
# "direction" of the edge (FROM source TO target).  This can be represented in a list, too,
# by making sure that the source and target are in the correct order. This would involve
# changing the code for creating the edgelist, though. Another possible approach is to 
# create this 2-level dictionary, which would allow for additional attributes, such as
# date/time, to be added to that particular edge.

#with open("/Users/jenniferdeboer1/Desktop/connections.csv", "w") as the_file:
with open("/Users/samuelfinegold/documents/harvard/edxresearch/snacreationfiles/connections_real.csv", "w") as the_file:
    csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
    writer = csv.writer(the_file, dialect="custom")
    for tup in edgelist:
        writer.writerow(tup)      

the_file.close()        
f.close()	
print "done!! yayy!!" 