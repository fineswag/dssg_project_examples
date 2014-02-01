####
# Removes duplicate entries (GCs with two entries) in the merged spreadsheet containing multiple counselors
# Sam Finegold
# July, 2013
####

import csv

fieldnames = ['area', 'degree', 'languages','lat','lng','areas_of_practice','name', 'occupation', 'company', 'address', 'address_2','city', 'state', 'zip', 'phone', 'fax', 'email', 'website', 'description', 'flag']

##################### Flag Duplicates ##################
# Flags rows with the same names and thereby marks rows for duplication
def flag_duplicates(myjson):

    # Flag the file, marking all entries with the same name with the same flags.        
    flag_counter = 0
    
    counter = 0
    myjson[0]['flag'] = flag_counter

    # If the name in the previous row is the same as the name in the current, do not increment counter     
    for i in range(1,len(myjson)):    
        if myjson[i]['name'] == myjson[i-1]['name'] and myjson[i]['city'] == myjson[i-1]['city']:
            myjson[i]['flag'] = flag_counter
        else:  
            flag_counter = flag_counter + 1
            myjson[i]['flag'] = flag_counter
    
    return(myjson)

###################### Prepped File #####################
# Writes to a new file entries with full information. File contains no duplicates.
def gen_nondup(myjson):

    # Write to file nonduplicate entries     
    with(open('gc_all_no_duplicates.txt','w')) as f:
        
        f_dict = csv.DictWriter(f, fieldnames = fieldnames, delimiter = '\t')
        gen_dict = {'languages': [],'lat': '','lng': '','areas_of_practice': [],'name': '', 'occupation': '', 'company':[], 'address': [],'city': '', 'state': '', 'zip': '', 'phone': [], 'fax': [], 'email': [], 'website': [], 'description': [], 'flag': '', 'degree':[], 'area':[]}
        
        # Clean values to avoid entering duplicate values (ex: two of the same email, where one differs by a space)
        for row in myjson:
            for key, value in row.iteritems():  
                try: value = value.strip()
                except AttributeError: pass # handles type 'int'

        f_dict.writeheader()           
         
        # Go through rows and if previous flag matches current flag and the information is different, add information to current.  
        # If different flag, write the finished person's entry to file and move to next person
        for row in range(1,len(myjson)):
        
            # handle duplicate
            if myjson[row]['flag'] == myjson[row-1]['flag']:
                
                gen_dict['name'] = myjson[row]['name']
                gen_dict['lat'] = myjson[row]['lat']
                gen_dict['lng'] = myjson[row]['lng']
                gen_dict['city'] = myjson[row]['city']
                gen_dict['zip'] = myjson[row]['zip']
                gen_dict['state'] = myjson[row]['state']
                gen_dict['address'] = myjson[row]['address']
                gen_dict['occupation'] = myjson[row]['occupation']

                if myjson[row]['phone'] not in gen_dict['phone'] and myjson[row]['phone'] != '':
                    gen_dict['phone'].append(myjson[row]['phone'])
                if myjson[row]['email'] not in gen_dict['email'] and myjson[row]['email'] != '' or [] or None or '[]':
                    gen_dict['email'].append(myjson[row]['email'])
                # print 'dup email: ', gen_dict['email']
                if myjson[row]['website'] not in gen_dict['website'] and myjson[row]['website'] != '':
                    gen_dict['website'].append(myjson[row]['website'])
                if myjson[row]['description'] not in gen_dict['description'] and myjson[row]['description'] != '':
                    gen_dict['description'].append(myjson[row]['description'])            
                if myjson[row]['languages'] not in gen_dict['languages'] and myjson[row]['languages'] != '':
                    gen_dict['languages'].append(myjson[row]['languages'])
                if myjson[row]['fax'] not in gen_dict['fax'] and myjson[row]['fax'] != '':
                    gen_dict['fax'].append(myjson[row]['fax'])
                if myjson[row]['areas_of_practice'] not in gen_dict['areas_of_practice'] and myjson[row]['areas_of_practice'] != '':
                    gen_dict['areas_of_practice'].append(myjson[row]['areas_of_practice'])
                if myjson[row]['company'] not in gen_dict['company'] and myjson[row]['company'] != '':
                    gen_dict['company'].append(myjson[row]['company'])
                try: 
                    if myjson[row]['area'][0] not in gen_dict['area'] and myjson[row]['area'][0] != '':
                        gen_dict['area'].append(myjson[row]['area'])
                except (IndexError, KeyError): pass
                try:
                    if myjson[row]['degree'][0] not in gen_dict['degree'] and myjson[row]['degree'][0] != '':
                        gen_dict['degree'].append(myjson[row]['degree'][0])
                except (IndexError, KeyError): pass 
            
            # handle nonduplicate
            else:   
                
                # write to file
                f_dict.writerow(gen_dict)
                
                # reinitialize gen_dict for next entry
                gen_dict = {'languages': [],'lat': '','lng': '','areas_of_practice': [],'name': '', 'occupation': '', 'company':[], 'address': [],'city': '', 'state': '', 'zip': '', 'phone': [], 'fax': [], 'email': [], 'website': [], 'description': [], 'flag': '', 'degree':[], 'area':[]}

                # write the first entry for the next person
                gen_dict['name'] = myjson[row]['name']
                gen_dict['lat'] = myjson[row]['lat']
                gen_dict['lng'] = myjson[row]['lng']
                gen_dict['city'] = myjson[row]['city']
                gen_dict['zip'] = myjson[row]['zip']
                gen_dict['state'] = myjson[row]['state']
                gen_dict['occupation'] = myjson[row]['occupation']

                if myjson[row]['phone'] == '': gen_dict['phone'] = ['']
                else: gen_dict['phone'].append(myjson[row]['phone'])
                if myjson[row]['email'] == '': pass
                else: gen_dict['email'].append(myjson[row]['email'])
#                 print 'email: ', gen_dict['email']                
                if myjson[row]['website'] == '': gen_dict['website'] = []
                else: gen_dict['website'].append(myjson[row]['website'])
                if myjson[row]['address_2'] == '': pass
                else: gen_dict['address'].append(myjson[row]['address_2'])
                if myjson[row]['languages'] == '' or myjson[row]['languages'] == 'english': pass
                else: gen_dict['languages'].append(myjson[row]['languages'])
                if myjson[row]['areas_of_practice'] == '': pass
                else: gen_dict['areas_of_practice'].append(myjson[row]['areas_of_practice'])
                if myjson[row]['company'] == '': pass
                else: gen_dict['company'].append(myjson[row]['company'])
                if myjson[row]['fax'] == '': pass
                else: gen_dict['fax'].append(myjson[row]['fax'])
                if myjson[row]['description'] == '': pass
                else: gen_dict['description'].append(myjson[row]['description'])
#                 print myjson[row].keys()
#                 try: gen_dict['degree'].append(myjson[row]['degree'])
#                 except IndexError: pass
#                 try: gen_dict['area'].append(myjson[row]['area'][0])            
#                 except IndexError: pass
    
    print 'done'
with(open('gc_all.txt', 'rU')) as f:
    f_d = csv.DictReader(f,delimiter='\t')
    f_l = []
    for row in f_d:
        f_l.append(row)

flag_duplicates(f_l)

gen_nondup(f_l)