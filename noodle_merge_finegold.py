################################################################
# Merges data from NBCC, IECA, and NACAC sources into flat JSON
# Samuel Finegold
# sjfinegold@gmail.com
# July 2013
################################################################

from string import punctuation, whitespace
import csv
import pdb
from nameparser import HumanName

########### store data form each of the spreadsheets in arrays containing entries ###########

# aicep
with(open('/Users/samuelfinegold/Documents/noodle/gc/aicep/aicep_cleaned.txt', 'rU')) as aicep:
    aicep_d = csv.DictReader(aicep, delimiter = '\t')
    aicep_l = []
    for row in aicep_d:
        name = HumanName(row['name'])
        row['name'] = name.title + ' ' + name.first + ' ' + name.middle + ' ' + name.last + ' ' + name.suffix       
        row['phone'] = row['phone'].translate(None, whitespace + punctuation)
        if type(row['email']) == list:
            row['email'] = row['email'][0] 
            print 'hi'
        elif row['email'] == []: 
            row['email'] = None
            print 'hi'      
        aicep_l.append(row)

# nbcc
with(open('/Users/samuelfinegold/Documents/noodle/gc/nbcc/nbcc_output.txt', 'rU')) as nbcc:
    nbcc_d = csv.DictReader(nbcc, delimiter = '\t')
    nbcc_l = []
    for row in nbcc_d:
        name = HumanName(row['name'])
        row['name'] = name.title + ' ' + name.first + ' ' + name.middle + ' ' + name.last + ' ' + name.suffix       
        row['name'] = row['name'].encode('utf-8') # Not sure what required this...
        row['phone'] = row['phone'].translate(None, whitespace + punctuation)
        nbcc_l.append(row)
     
# ieca
with(open('/Users/samuelfinegold/Documents/noodle/gc/ieca/ieca_no_duplicates.txt', 'rU')) as ieca:
    ieca_d = csv.DictReader(ieca, delimiter = '\t')
    ieca_l = []
    for row in ieca_d:
        name = HumanName(row['name'])
        row['name'] = name.title + ' ' + name.first + ' ' + name.middle + ' ' + name.last + ' ' + name.suffix        
        row['name'] = row['name'].encode('utf-8')
        row['phone'] = row['phone'].translate(None, whitespace + punctuation) 
        if type(row['email']) == list:
            row['email'] = row['email'][0] 
            print 'hi'
        elif row['email'] == []: 
            row['email'] = None
            print 'hi'  
        ieca_l.append(row)        
#          
# nacac
with(open('/Users/samuelfinegold/Documents/noodle/gc/nacac/nacac_scrape_output_cleaned.txt', 'rU')) as nacac:
    nacac_d = csv.DictReader(nacac, delimiter = '\t')
    nacac_l = []
    for row in nacac_d:
        name = HumanName(row['name'])
        row['name'] = name.title + ' ' + name.first + ' ' + name.middle + ' ' + name.last + ' ' + name.suffix
        row['name'] = row['name'].encode('utf-8')
        row['phone'] = row['phone'].translate(None, whitespace + punctuation)     
        if type(row['email']) == list:
            row['email'] = row['email'][0] 
            print 'hi'
        elif row['email'] == []: 
            row['email'] = None
            print 'hi'  
        nacac_l.append(row)  

fieldnames = ['area','degree','languages','lat','lng','areas_of_practice','name', 'occupation', 'company', 'address', 'address_2','city', 'state', 'zip', 'phone', 'fax', 'email', 'website', 'description', 'flag']

# compile master spreadsheet
with(open('gc_all.txt','w')) as gc_all:
    gc_all_d = csv.DictWriter(gc_all,  fieldnames = fieldnames, extrasaction='ignore', delimiter = '\t') 
    gc_all_d.writeheader()
    for row in aicep_l:
        gc_all_d.writerow(row)
    for row in ieca_l:
        gc_all_d.writerow(row)              
    for row in nacac_l:
        gc_all_d.writerow(row)
    for row in nbcc_l:
         gc_all_d.writerow(row)

with(open('gc_all.txt','rU')) as gc_all:
    gc_all_d = csv.DictReader(gc_all,  delimiter = '\t') 
    gc_l = []
    for row in gc_all_d:
        gc_l.append(row)
    for row in gc_l:
        print row['email']
