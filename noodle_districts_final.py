####
# Gets US school district information from Wikipedia
# Sam Finegold
# sjfinegold@gmail.com
# August 16, 2013
#
# Note: no info for Hawaii available. 
#
####

import re
import csv
from bs4 import BeautifulSoup
import requests
from lxml import etree

# creates set of cities from set of districts' cities
with(open('cities.txt','rU')) as f:
    cities = {row.strip() for row in f}

# master list of dictionaries containing district information
dist_dicts = []

"""
Generate a list of wiki pages for lists of districts by state. 

Ended up not using this. Instead, I just wrote out the urls. Greater automatization can be achieved by 
iterating through this list. As the code currently stands, state_district_urls is not necessary.
"""

districts_site = 'http://en.wikipedia.org/wiki/Lists_of_school_districts_in_the_United_States'
district_soup = BeautifulSoup(requests.get(districts_site).text)
state_district_urls = []
lis = district_soup.find_all('li')
for li in lis: 
    try: state_district_urls.append(li.a['href'])
    except TypeError: pass
state_district_urls = state_district_urls[6:63]
for ind, url in enumerate(state_district_urls): state_district_urls[ind] = 'http://en.wikipedia.org'+url

"""
Used for diagnostics later...ignore for now
"""

with(open('district_counts_2.txt','rU')) as f:
    state_dist_count = {}
    for row in f:
        state_dist_count[row.split(' ')[0].strip()] = float(row.split(' ')[1].strip())

# # Return a dictionary mapping state abbreviation to the total number of districts in the state
# with(open('district_counts.txt','rU')) as f:
#     sts_abrev = []
#     counts = []
#     for row in f:
#         if re.search("[A-Z]{2}",row) is not None: sts_abrev.append(re.findall("[A-Z]{2}",row)[0])
#         if re.search('[0-9]+',row) is not None: counts.append(float(re.findall('[0-9]+',row)[0]))
# state_dist_count = dict(zip(sts_abrev, counts))

"""
Function get_state_district_urls 
Note: not used for all states due to differences in the html of the states' pages.

INPUT: URL that links to a wikipedia page that contains a list of states' districts' urls

Arguments: 1. List that will hold valid district wikipedia pages' urls. 
2. URL that links to a wikipedia page that contains a list of states' districts' urls
3. Limit on the number of UL tags the function searches through for the url. I looked up the number of UL elements using
the xpath of a district page link in last section of a list of districts (ex: school under the 'Z' section). 
4. State acronym paired to url and separated by ',,,'. This acronym is split from the URL later and is added 
as another key,value pair to the district dictionary at the end.

OUTPUT: a list of the valid district wikipedia pages' urls 
"""

district_urls = []
def get_state_district_urls(state_list,url,ul_limit, state_acronym):
    uls = BeautifulSoup(requests.get(url).text).find_all('ul',limit = ul_limit)
    for ul in uls:
        for li in ul:
            try: 
                if li.a.get('title') is not None:
                    if re.search('does not exist',li.a.get('title')) is None:
                        state_list.append('http://en.wikipedia.org'+li.a['href'] + ',,, ' + state_acronym)
            except AttributeError: pass
    return state_list


"""
And here we go...
The code goes state by state, calling the 'get_state_district_urls' function when convenient to get the 
urls to districts' wikipedia pages.

At times, you'll notice a little extra work to get urls from the list of district pages that are not accessible
on the actual district pages.  In other words, there are urls that link directly to district pages that 
can be obtained only from the list of districts, not from the individual district pages because some of these
individual pages contain NOTHING!
"""

# Alabama
AL = []
response = requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Alabama').text
parser = etree.HTMLParser()
tree = etree.fromstring(response, parser)
for row in tree.xpath('//*[@id="mw-content-text"]/table[1]/tr'):
    links = row.xpath('./td[1]/a')
    if links:
        link = links[0]
        if re.search('exist', link.attrib.get('title')) is None:
            AL.append('http://en.wikipedia.org' + link.attrib.get('href') + ',,, AL')
state_dist_count['AL'] = len(AL)/state_dist_count['AL']

# Alaska
AK = []
soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Alaska').text)
lis = soup.find_all('li')
for li in lis:
    try:
        if re.search('District',li.a.get('title')) is not None:
            if re.search('not exist',li.a.get('title')) is None:
                AK.append('http://en.wikipedia.org'+li.a['href'] + ',,, AK')
    except (AttributeError, TypeError): pass
state_dist_count['AK'] = len(AK)/state_dist_count['AK']

# Arizona     
AZ = []   
response = requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Arizona').text
parser = etree.HTMLParser()
tree = etree.fromstring(response, parser)
for row in tree.xpath('//*[@id="mw-content-text"]/ul/li/a'):
    AZ.append('http://en.wikipedia.org'+ row.get('href')+ ',,, AZ')
state_dist_count['AZ'] = len(AZ)/state_dist_count['AZ']
    
# Arkansas
AR = []
soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Arkansas').text) 
lis = soup.find('tr', valign = 'top').find_all('li')
for li in lis:
    try:
        if re.search('not exist',li.a.get('title')) is None:
            if re.search('District',li.a.get('title')) is not None or re.search('school',li.a.get('title')) is not None or re.search('department',li.a.get('title')) is not None: # check syntax
                AR.append('http://en.wikipedia.org'+li.a['href']+ ',,, AR')
    except (AttributeError, TypeError): pass
state_dist_count['AR'] = len(AR)/state_dist_count['AR']

# California
CA = []
get_state_district_urls(CA,'http://en.wikipedia.org/wiki/List_of_school_districts_in_California',23, 'CA')
state_dist_count['CA'] = len(CA)/state_dist_count['CA']

# Colorado
CO = []
CO_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Colorado').text)
CO_table = CO_soup.find('table')
CO_rows = CO_table.find_all('tr')
for row in CO_rows:
    if row.a is not None:
        if re.search('does not exist',row.a.get('title')) is None:
            CO.append('http://en.wikipedia.org'+row.a['href']+ ',,, CO')
# CO_urls = CO_table.find_all('a')
# for url in CO_urls:
#     try: 
#         if url.get('title') is not None:
#             if re.search('does not exist',url.get('title')) is None:
#                 CO.append('http://en.wikipedia.org'+url['href']+ ',,, CO')
#     except AttributeError: pass
state_dist_count['CO'] = len(CO)/state_dist_count['CO']

# Connecticut
CT = []
get_state_district_urls(CT,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Connecticut',20, 'CT')

# Connecticut schools with links
CT_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Connecticut').text)
links = CT_soup.find_all('li')
for link in links:
    if len(link.find_all('a')) > 1: 
        dist_dicts.append({'name': link.find_all('a')[0].text, 'url': link.find_all('a')[1]['href'], 'location': '', 'dist_id': '', 'state': 'CT'})
state_dist_count['CT'] = len(CT)/state_dist_count['CT']

# Delaware
DE = []
DE_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Delaware').text)
uls = DE_soup.find_all('ul',limit=6)
for ul in uls:
    for li in ul:
        try: 
            if li.a.get('title') is not None:
                if re.search('does not exist',li.a.get('title')) is None:
                    DE.append('http://en.wikipedia.org'+li.a['href']+ ',,, DE')
        except AttributeError: pass

# Delaware schools with links
DE_links = DE_soup.find_all('li')
for link in DE_links:
    if len(link.find_all('a')) > 1: 
        dist_dicts.append({'name': link.find_all('a')[0].text, 'url': link.find_all('a')[1]['href'], 'location': '', 'dist_id': '', 'state':'DE'})
state_dist_count['DE'] = len(DE)/state_dist_count['DE']

# DC?

# Florida
FL = []
get_state_district_urls(FL,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Florida',21, 'FL')
state_dist_count['FL'] = len(FL)/state_dist_count['FL']

# Georgia
GA = []
GA_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Georgia').text)
table = GA_soup.find('table')
rows = table.find_all('tr')
for row in rows:
    try: 
        GA.append('http://en.wikipedia.org'+row.contents[1].a['href']+ ',,, GA')
        dist_dicts.append({'name': row.contents[1].a.get('title'), 'url': row.contents[3].a['href'], 'location': '', 'dist_id':''})
    except TypeError: pass
state_dist_count['GA'] = len(GA)/state_dist_count['GA']

# Hawaii sucks...doesn't have a wiki list of district pages

# Idaho
ID = []
get_state_district_urls(ID,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Idaho',8, 'ID')
state_dist_count['ID'] = len(ID)/state_dist_count['ID']

# Illinois
IL = []
get_state_district_urls(IL,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Illinois',102, 'IL')
state_dist_count['IL'] = len(IL)/state_dist_count['IL']

# Indiana
IN = []
get_state_district_urls(IN,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Indiana',23, 'IN')
state_dist_count['IN'] = len(IN)/state_dist_count['IN']

# Iowa
IA = []
get_state_district_urls(IA,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Iowa',99, 'IA')
state_dist_count['IA'] = len(IA)/state_dist_count['IA']

# Kansas
KS = []
get_state_district_urls(KS,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Kansas',12,'KS')
state_dist_count['KS'] = len(KS)/state_dist_count['KS']

# Kentucky
KY = []
get_state_district_urls(KY,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Kentucky',21,'KY')
state_dist_count['KY'] = len(KY)/state_dist_count['KY']

# Louisiana
LA = []
get_state_district_urls(LA,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Louisiana',21,'LA')
state_dist_count['LA'] = len(LA)/state_dist_count['LA']

# Maine
ME = []
get_state_district_urls(ME,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Maine',11,'ME')
state_dist_count['ME'] = len(ME)/state_dist_count['ME']

# Maryland
MD = []
get_state_district_urls(MD,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Maryland',1,'MD')
state_dist_count['MD'] = len(MD)/state_dist_count['MD']

MA = []
get_state_district_urls(MA,'http://en.wikipedia.org/wiki/List_of_school_districts_in_Massachusetts',39,'MA')
state_dist_count['MA'] = len(MA)/state_dist_count['MA']

MI = []
# public schools in MI
get_state_district_urls(MI, 'http://en.wikipedia.org/wiki/List_of_local_education_agency_districts_in_Michigan',15,'MI')
# 'intermediate' schools (whatever that means) in MI added to the MI list
MI_soup_2 = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_intermediate_school_districts_in_Michigan').text)
table = MI_soup_2.find('table')
rows = table.find_all('tr')
for row in rows:
    for col in row:
        try: 
            if re.search('not exist',col.a.get('title')) is None:
                MI.append('http://en.wikipedia.org'+col.a['href']+',,, MI')
        except (AttributeError,TypeError): pass

# intermediate more detailed added to master list of dictionaries 
for row in rows:
    tds = row.find_all('td')
    try: 
        dist_dicts.append({'name': tds[0].a.text, 'dist_id':tds[1].text, 'county':tds[2].text, 'url':tds[3].a['href'], 'state':'MI'})
    except (IndexError,AttributeError): pass
state_dist_count['MI'] = len(MI)/state_dist_count['MI']

MN = []
get_state_district_urls(MN, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Minnesota', 12,'MN')
state_dist_count['MN'] = len(MN)/state_dist_count['MN']

MS = []
get_state_district_urls(MS, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Mississippi', 26,'MS')
state_dist_count['MS'] = len(MS)/state_dist_count['MS']

MO = []
get_state_district_urls(MO, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Missouri', 23,'MO')
MO_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_Connecticut').text)
links = MO_soup.find_all('li')
for link in links:
    if len(link.find_all('a')) > 1: 
        dist_dicts.append({'name': link.find_all('a')[0].text, 'url': link.find_all('a')[1]['href'], 'location': '', 'dist_id': '','state':'MO'})
state_dist_count['MO'] = len(MO)/state_dist_count['MO']

MT = []
get_state_district_urls(MT, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Montana', 23,'MT')
state_dist_count['MT'] = len(MT)/state_dist_count['MT']

NV = []
get_state_district_urls(NV, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Nevada', 10,'NV')
state_dist_count['NV'] = len(NV)/state_dist_count['NV']

NH = []
NH_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_New_Hampshire').text)
NH_table = NH_soup.find('table')
NH_rws = NH_table.find_all('tr')
for row in NH_rws:
    try:
        if row.contents[3].a is not None:
            if re.search('not exist', row.contents[3].a.get('title')) is None:
                print 'title: ',row.contents[3].a.get('title')
                NH.append('http://en.wikipedia.org' + row.contents[3].a['href']+',,,NH')
                print 'valid url'
        else: pass
    except (IndexError, AttributeError): pass
print NH
# NH_urls = NH_table.find_all('a')
# for url in NH_urls:
#     try: 
#         if url.get('title') is not None:
#             if re.search('does not exist',url.get('title')) is None:
#                 NH.append('http://en.wikipedia.org'+url['href']+',,,NH')
#     except AttributeError: pass
state_dist_count['NH'] = len(NH)/state_dist_count['NH']

NJ = []
get_state_district_urls(NJ, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_New_Jersey', 21,'NJ')
state_dist_count['NJ'] = len(NJ)/state_dist_count['NJ']

NM = []
get_state_district_urls(NM, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_New_Mexico', 10,'NM')
state_dist_count['NM'] = len(NM)/state_dist_count['NM']

NY = []
get_state_district_urls(NY, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_New_York', 23,'NY')

NY_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_New_York').text)
lis = NY_soup.find_all('li')
for li in lis: 
    if len(li)>1:
        try:
            try: value = li.contents[0].get('href')
            except KeyError: value = ''
            dist_dicts.append({'name': li.contents[2].text, 'url': value,'location':'','dist_id':'','state':'NY'})
        except (AttributeError,IndexError): pass
state_dist_count['NY'] = len(NY)/state_dist_count['NY']

OH = []
get_state_district_urls(OH, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Ohio', None,'OH')
state_dist_count['OH'] = len(OH)/state_dist_count['OH']

NC = []
get_state_district_urls(NC, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Ohio', 23,'NC')
state_dist_count['NC'] = len(NC)/state_dist_count['NC']

ND = []
get_state_district_urls(ND, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_North_Carolina', 23,'ND')
state_dist_count['ND'] = len(ND)/state_dist_count['ND']

NE = []
get_state_district_urls(NE, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Nebraska', 94,'NE')
state_dist_count['NE'] = len(NE)/state_dist_count['NE']

OK = []
get_state_district_urls(OK, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Oklahoma', 23,'OK')
state_dist_count['OK'] = len(OK)/state_dist_count['OK']

OR = []
get_state_district_urls(OR, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Oregon', 24,'OR')
state_dist_count['OR'] = len(OR)/state_dist_count['OR']

PA = []
get_state_district_urls(PA, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Pennsylvania', 24, 'PA')
state_dist_count['PA'] = len(PA)/state_dist_count['PA']

RI = []
get_state_district_urls(RI, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Rhode_Island', 19, 'RI')
state_dist_count['RI'] = len(RI)/state_dist_count['RI']

SC = []
get_state_district_urls(SC, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_South_Carolina', 20, 'SC')
state_dist_count['SC'] = len(SC)/state_dist_count['SC']

SD = []
get_state_district_urls(SD, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_South_Dakota', 20, 'SD')
state_dist_count['SD'] = len(SD)/state_dist_count['SD']

TN = []
get_state_district_urls(TN, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Tennessee', 21, 'TN')
state_dist_count['TN'] = len(TN)/state_dist_count['TN']

TX = []
get_state_district_urls(TX, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Texas', 27, 'TX')
state_dist_count['TX'] = len(TX)/state_dist_count['TX']

UT = []
get_state_district_urls(UT, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Utah', 19, 'UT')
UT_soup = BeautifulSoup(requests.get('http://en.wikipedia.org/wiki/List_of_school_districts_in_New_York').text)
lis = UT_soup.find_all('li')
for li in lis: 
    if len(li)>1:
        try:
            try: value = li.contents[0].get('href')
            except KeyError: value = ''
            dist_dicts.append({'name': li.contents[2].text, 'url': value, 'location':'', 'dist_id':'', 'state': 'UT'})
        except (AttributeError,IndexError): pass
state_dist_count['UT'] = len(UT)/state_dist_count['UT']

VA = []
get_state_district_urls(VA, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Virginia', 7, 'VA')
state_dist_count['VA'] = len(VA)/state_dist_count['VA']

VT = []
get_state_district_urls(VT, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Virginia', 8, 'VT')
state_dist_count['VT'] = len(VT)/state_dist_count['VT']

WA = []
get_state_district_urls(WA, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Washington', 12, 'WA')
state_dist_count['WA'] = len(WA)/state_dist_count['WA']

WI = []
get_state_district_urls(WI, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Washington', 11, 'WI')
state_dist_count['WI'] = len(WI)/state_dist_count['WI']


WV = []
get_state_district_urls(WV, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_West_Virginia', 11, 'WV')
state_dist_count['WV'] = len(WV)/state_dist_count['WV']

WY = []
get_state_district_urls(WY, 'http://en.wikipedia.org/wiki/List_of_school_districts_in_Wyoming', 6, 'WY')
state_dist_count['WY'] = len(WY)/state_dist_count['WY']

state_district_lists = AL + AK + AR + AZ + CA + CO + CT + DE + FL + GA + ID + IL + IN + IA + KS + KY + LA + ME + MD + MA + MI + MN + MS + MO + MT + NE + NV + NH + NJ + NM + NY + NC + ND + OK + OH + OR + PA + RI + SC + SD + TN + TX + UT + WI + WA + WV + VA + WY

"""
Diagnostics
"""

# Return a dictionary mapping the state abbreviation to the fraction of districts covered by this script
for key,value in state_dist_count.iteritems(): print key, ': ', value

"""
Get district info
"""

tbl_ctr = 0
ttl_ctr = 0

def get_district_info(url):

    dist_d = {'name':'','url':'','state':'','dist_id':''}
    try:
        soup = BeautifulSoup(requests.get(url.split(',,,')[0].strip()).text)
        try: dist_d['state'] = url.split(',,,')[1].strip()
        except IndexError: dist_d['state'] = ''

        # get school name
        dist_d['name'] = soup.find('h1', 'firstHeading').get_text()

        # get school location and url
        if soup.find("table", class_ = "infobox") is not None:

            global tbl_ctr
            tbl_ctr += 1
    
            table = soup.find('table', class_ = 'infobox')
    
            for row in table.find_all('tr'):
                try: 
                    if 'NCES' in row.th.text: dist_d['dist_id'] = row.td.a.text
                except AttributeError: pass
        
            table_contents = soup.find('table','infobox').text
            for city in cities:
                if re.search(city, table_contents) is not None:
                    dist_d['location'] = city
                else: pass

            table = soup.find('table','infobox')
            try: dist_d['url'] = table.find('th', text = 'Website').parent.find('td').a['href']
            except (AttributeError, TypeError):
                try: dist_d['url'] = table.find('th', text = 'Website').parent.find('td').text
                except AttributeError: pass
    
        elif soup.find_all('a','external text') is not None: 
            for link in soup.find_all('a','external text'):
                if re.search('tools.wmflabs.org', link['href']) is None and re.search('en.wikipedia.org', link['href']) is None: 
                    dist_d['url'] = link['href']
                    break

        elif soup.find('a','external free') is not None:
            for link in soup.find_all('a','external text'):
                if re.search('tools.wmflabs.org', link['href']) is None and re.search('en.wikipedia.org', link['href']) is None: 
                    dist_d['url'] = link['href']
                    break

    except (AttributeError, requests.packages.urllib3.exceptions.LocationParseError): pass

    return dist_d

counter = 0
for url in state_district_lists[3200:]: 
    if counter%75==0: 
        print(get_district_info(url))
    dist_dicts.append(get_district_info(url))
    ttl_ctr += 1
    
    counter += 1

counter = 0
for ind,value in enumerate(dist_dicts): 
    if ind%50==0: print ind, value
    counter += 1

"""

Writing to a spreadsheet

When I left off, I was having issues with unicode errors.  Below was my feeble patch attempt to remedy this, 
but I think fixing it will require actually going into the values and making sure that they're
encoded using unicode.

"""
with(open('districts_info.txt','w')) as f:
    f_d = csv.DictWriter(f,fieldnames = dist_dicts[0].keys(),extrasaction = 'ignore',delimiter = '\t')
    for row in dist_dicts: 
        try: f_d.writerow(row)
        except UnicodeError: row.encode('utf-8')

"""
Writing to JSON
"""
# ...........
