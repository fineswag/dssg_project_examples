####
# Consolidates and formats BLS O*NET Data into JSON
# Sam Finegold
# sjfinegold@gmail.com
# August 11, 2013
####

# NOTE: set to run through full list, which will take a while to write to JSON. To test if it works, run on a sample of d_l

import csv
from collections import OrderedDict
import json
from pprint import pprint
import json

# Supposed to help with organization of files. Basically just creates a list of files, but actually easy to open them 
# by directly referencing their names rather than positions in a list. 
file_list = []

# Get list of files
with(open('db_files.txt','rU')) as f:
    for row in f:
        file_list.append(str(row.strip()))
        
"""
DONE 0 :  Abilities.txt
DONE 5 :  Skills.txt
DONE, 8 :  Green Occupations.txt
DONE 10 :  Green Task Statements.txt CHANGED NAME TO 'Green Task'
DONE 11 :  Task Ratings.txt
DONE 12 :  Interests.txt
DONE 14 :  Job Zone Reference.txt
DONE 15 :  Work Activities.txt
DONE 16 :  Job Zones.txt
DONE 18 :  Knowledge.txt
DONE 19 :  Work Context.txt
DONE 21 :  Work Styles.txt
MASTER FILE 22 :  Occupation Data.txt

2 :  Content Model Reference.txt    PAIR WITH ABILITIES
3 :  Scales Reference.txt   NOT SURE WHERE TO PUT
4 :  Education, Training, and Experience Categories.txt     NOT SURE WHERE TO PUT
6 :  Education, Training, and Experience.txt
9 :  Task Categories.txt
11 :  Task Ratings.txt
13 :  Task Statements.txt
? 20 :  Level Scale Anchors.txt
23 :  Work Values.txt

NA 7 :  Survey Booklet Locations.txt
NA 17 :  Work Context Categories.txt
NA 1 :  Read Me.txt
NA 24 :  Occupation Level Metadata.txt
"""

"""
Create master list named d_l which will eventually be converted to JSON
"""

with(open('Occupation Data.txt','rU')) as f:
    f_d = csv.DictReader(f,delimiter = '\t')
    d_l = []
    for row in f_d:    
        d_l.append(row)

"""
Consolidate Class
This class creates a list of dictionaries from a file, each dictionary representing a row in a file.
This class also has an associated function, merge, that exploits a similar structure in a number of files and
consolidates the list of dictionaries.
"""

class Consolidate(object):
    
    def __init__(self, file):
        self.file = file
                
    def create_master_list(self):
        with(open(self.file,'rU')) as f:
            f_d = csv.DictReader(f, delimiter = '\t')
            m_l = []
            for d in f_d:
                m_l.append(d)
        return m_l
    
    def merge(self, field):
        
        # initialize field to empty dict
        for row in d_l:
            row[field] = {}

        field_dict = {}  
        
        field_list = self.create_master_list()
        
        for index, dict in enumerate(field_list):
            if field_list[index]['O*NET-SOC Code'] == field_list[index-1]['O*NET-SOC Code']:
                if field_list[index]['Element Name'] != field_list[index-1]['Element Name']:
                    field_dict[field_list[index]['Element Name']] = []
                    field_dict[field_list[index]['Element Name']].append({key:value for key,value in dict.iteritems() if key != 'Element Name'})
                else: field_dict[field_list[index]['Element Name']].append({key:value for key,value in dict.iteritems() if key != 'Element Name' or 'O*NET-SOC Code'})   
            else: 
                for row in d_l:
                    if row['O*NET-SOC Code'] == field_list[index-1]['O*NET-SOC Code']:
                        row[field] = field_dict
                field_dict = {}
                field_dict[field_list[index]['Element Name']] = []
                field_dict[field_list[index]['Element Name']].append({key:value for key,value in dict.iteritems() if key != 'Element Name'})       

           
"""
Merge Task Statements and Ratings
"""

# create list of task ratings and list of task statements
task_r = Consolidate('Task Ratings.txt')
task_r_l = task_r.create_master_list()
task_s = Consolidate('Task Statements.txt')
task_s_l = task_s.create_master_list()

# initialize each entry to an empty dictionary
for row in d_l:
    row['task_rating'] = {}

# Task info will be added to the d_l as a task_ratings_dictionary
task_r_dict = {} 
for index, dict in enumerate(task_r_l):
    if task_r_l[index]['O*NET-SOC Code'] == task_r_l[index-1]['O*NET-SOC Code']:
        if task_r_l[index]['Task ID'] != task_r_l[index-1]['Task ID']:
            task_r_dict[task_r_l[index]['Task ID']] = []
            task_r_dict[task_r_l[index]['Task ID']].append({key:value for key,value in dict.iteritems() if key != 'Task ID'})
        else: task_r_dict[task_r_l[index]['Task ID']].append({key:value for key,value in dict.iteritems() if key != 'Task ID' or 'O*NET-SOC Code'})   
    else: 
        for row in d_l:
            if row['O*NET-SOC Code'] == task_r_l[index-1]['O*NET-SOC Code']:
                row['task_rating'] = task_r_dict
        task_r_dict = {}
        task_r_dict[task_r_l[index]['Task ID']] = []
        task_r_dict[task_r_l[index]['Task ID']].append({key:value for key,value in dict.iteritems() if key != 'Element Name'})       
        
"""
Work Style
"""
       
# initialize field to empty list
for row in d_l:
    row['work_style'] = []

w_s = Consolidate('Work Styles.txt')
work_style_list = w_s.create_master_list()
 
w_s_compiled = []
for index, dict in enumerate(work_style_list):
    if work_style_list[index]['O*NET-SOC Code'] == work_style_list[index-1]['O*NET-SOC Code']:
        w_s_compiled.append({key:value for key,value in dict.iteritems() if key != 'O*NET-SOC Code'})
    else: 
        dict['work_style'] = w_s_compiled
        w_s_compiled = []

print 'work style'

"""
Green Occupations
"""

# initialize keys to nothing
for row in d_l:
    row['Green Occupational Category'] = ''
    row['Green Task'] = ''
            
with(open(file_list[8])) as f:
    f_d = csv.DictReader(f,delimiter = '\t')
    for row in f_d:
        for r in d_l:
            if row['O*NET-SOC Code'] == r['O*NET-SOC Code']:
                r['Green Occupational Category'] = row['Green Occupational Category']

print 'green occ'

"""
Green Task
"""

with(open(file_list[10])) as f:
    f_d = csv.DictReader(f, delimiter = '\t')
    for row in f_d:
        for r in d_l:
            if row['O*NET-SOC Code'] == r['O*NET-SOC Code']:
                r['Green Task'] = row['Task']
print 'green task'

"""
Job Zone
"""     

a = Consolidate('Job Zones.txt')
job_zones_list = a.create_master_list()

a = Consolidate('Job Zone Reference.txt')
job_zone_ref_list = a.create_master_list()

for job in job_zones_list:
    for ref in job_zone_ref_list:
        if job['Job Zone'] == ref['Job Zone']:
            job[job['O*NET-SOC Code']] = {key:value for key,value in ref.iteritems()}

# add field to master list
for dict in d_l:
    for row in job_zones_list:
        if dict['O*NET-SOC Code'] == row['O*NET-SOC Code']:
            dict['job_zone'] =  row[row['O*NET-SOC Code']]
            
print 'job zone'


"""
Interests 
"""  
   
# initialize field to empty dict
for row in d_l:
    row['interests'] = []
     
interests = Consolidate('Interests.txt')  
interests_list = interests.create_master_list()
       
interests_compiled = []
 
for index, dict in enumerate(interests_list[1:]):
    if interests_list[index]['O*NET-SOC Code'] == interests_list[index-1]['O*NET-SOC Code']:
        interests_compiled.append({key:value for key,value in dict.iteritems() if key != 'O*NET-SOC Code'})
    else: 
        for row in d_l:
            if row['O*NET-SOC Code'] == interests_list[index-1]['O*NET-SOC Code']:
                row['interests'] = interests_compiled
        interests_compiled = []

print 'interests'

"""                
Abilities
"""

abilities = Consolidate("Abilities.txt")
abilities.merge('abilities')

print 'abilities'

"""
Skills
"""
skills = Consolidate("Skills.txt")
skills.merge('skills')

print 'skills'

"""
Work Activities
"""
work_act = Consolidate("Work Activities.txt")
work_act.merge("work_activities")

print 'work activities'

"""
Knowledge
"""
know = Consolidate("Knowledge.txt")
know.merge("knowledge")

print 'knowledge'

"""
Work Context
"""
w_c = Consolidate("Work Context.txt")
w_c.merge("work_context")

print 'work context'

"""
Test
"""

print 'nearly done'

print d_l[0].keys()

with(open('bls.json','w')) as f:
    json.dump(d_l,f,indent = 4)
    