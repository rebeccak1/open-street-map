
#!/usr/bin/env python
import xml.etree.cElementTree as ET
from collections import defaultdict
import re


"""
Your task in this exercise has two steps:
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
direction_re = re.compile(r'\w*(North|South|East|West|Northeast|Northwest|Southeast|Southwest|S|NE|W|N|E|SE|N.)$')

#the mapping from abbreviated direction names to full direction names
direction_mapping = {"N":"North",
                    "S":"South",
                    "NE":"Northeast",
                    "W":"West",
                    "E":"East",
                    "SE": "Southeast"}

#the expected street types in the data set
expected = ["Passage","Cutoff","Bridge","Crossing","Lane","Way","Run","Loop","Plaza","Causeway","Terrace","Highway","Bayway","Circle","Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

#the mapping from problem cities encountered to their corrected values
city_mapping = {'St. Petersburg, FL':'St. Petersburg',
                'St Petersburg ': 'St. Petersburg',
                'St Pete Beach': 'St. Pete Beach',
                'SPRING HILL': 'Spring Hill',
                'sarasota': 'Sarasota',
                'St Petersburg': 'St. Petersburg',
                'lutz': 'Lutz',
                'spring hill': 'Spring Hill',
                'Zephyhills': 'Zephyrhills',
                'port richey': 'Port Richey',
                'Miakka': 'Old Myakka',
                'Saint Petersburg': 'St. Petersburg',
                'Seminole ': 'Seminole',
                'Land O Lakes': "Land O' Lakes",
                'Tampa ': 'Tampa',
                'St Petersbug': 'St. Petersburg',
                'hudson': 'Hudson',
                'Land O Lakes, FL': "Land O' Lakes",
                'Clearwarer Beach': 'Clearwater Beach',
                'Palm Harbor, Fl.': 'Palm Harbor',
                'tampa': 'Tampa'}

#the expected cities in the data set
cities = ['Indian Shores',"Land O' Lakes", 'Pinellas Park',
          'Largo', 'Trinity', 'St. Petersburg', 'Bay Pines',
          'Treasure Island', 'Indian Rocks Beach', 'Apollo Beach',
          'Palm Harbor', 'Temple Terrace','Tampa', 'St. Pete Beach',
          'Lakeland', 'Old Myakka', 'Plant City','Dunedin', 'South Highpoint', 
          'Madeira Beach', 'Gulfport', 'Lakewood Ranch', 'Longboat Key', 'Brandon',
          'Clearwater Beach', 'Verna', 'Seminole', 'Dade City', 'Feather Sound', 'Redington Shores',
          'Gandy', 'South Pasadena', 'Cortez Village', 'Safety Harbor', 'San Antonio',
          'Anna Maria', 'Bradenton Beach', 'Palm Harbor',
          'Wesley Chapel', 'Tarpon Springs', 'New Port Richey',
          'St. Petersburg', 'Port Richey', 'Clearwater', 'Pasadena', 'Redington Beach',
          'Holiday', 'Sarasota', 'Lutz', 'Wimauma', 'Parrish', 'Zephyrhills', 'Shady Hills',
          'Thonotosassa', 'Belleair', 'Belleair Beach', 'Ellenton', 'Ruskin', 'Oldsmar',
          'Valrico', 'Kenneth City', 'Hudson', 'Riverview',
          'Bradenton', 'Odessa', 'Gibsonton', 'Lithia',
          'Palmetto', 'Pass-a-Grille Beach', 'Spring Hill',
          'Holmes Beach', 'Dover', 'Seffner', 'Sun City Center', 'Saint Leo']

#the mapping from abbreviated street types to the full, corrected type
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Dr": "Drive",
            "Av": "Avenue",
            "AVE": "Avenue",
            "Blvd": "Boulevard",
            "Cir": "Circle",
            "Hwy": "Highway",
            "Blvd.": "Boulevard",
            "Pkwy": "Parkway",
            "dr": "Drive",
            "Dr.": "Drive",
            "Ave.": "Avenue",
            "Pl": "Place",
            "Cswy": "Causeway",
            "Plz": "Plaza",
            "Ct": "Court",
            "Pky": "Parkway",
            "Ln": "Lane",
            "st": "Street",
            "road": "Road",
            "drive": "Drive",
            "lane": "Lane"
            }
'''
Correct the state name to 'FL'.
'''
def clean_state(state_name):
    if state_name != 'FL':
        state_name = 'FL'
    return state_name

'''
Audit states that are not 'FL', and add to dictionary.
'''
def audit_state(state_types, state_name):
    if state_name != 'FL':
        state_types[state_name] += 1

'''
Audit streets and add ones that do not end in a value 
found in the expected list to a dictionary.
'''
def audit_street_type(street_types, street_name):
    street_name = clean_street(street_name)
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    return street_name

'''
Audit cities and add ones that are not in the expected list of
cities or are not found in the ldictionary city_mapping, which maps
known incorrect cities to correct ones, to a dictionary.
'''
def audit_city(invalid_cities, city_name):
    if city_name not in cities and city_name not in city_mapping:
        invalid_cities[city_name] += 1   

        
'''
Correct incorrect city names with the city_mapping dictionary.
'''        
def clean_city(city_name):
    if city_name not in cities and city_name in city_mapping:
        city_name = city_mapping[city_name]
    return city_name

'''
Audit zipcodes and add ones that are not of length 5 digits to
a dictionary.
'''
def audit_zipcode(invalid_zipcodes, zipcode):
    if not re.match(r'^\d{5}$', zipcode):
        invalid_zipcodes[zipcode] += 1
    return zipcode

'''
Tests whether an element is a street.
'''
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

'''
Tests whether an element is a state.
'''
def is_state(elem):
    return (elem.attrib['k'] == "addr:state")

'''
Tests whether an element is a city.
'''
def is_city(elem):
    return (elem.attrib['k'] == "addr:city")

'''
Tests whether an element is a zipcode.
'''
def is_zipcode(elem):
    return 'zip' in elem.attrib['k']

def audit(osmfile):
    osm_file = open(osmfile, "r")
    
    street_types = defaultdict(set)
    city_types = defaultdict(int)
    zipcode_types = defaultdict(int)
    state_types = defaultdict(int)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_zipcode(tag):
                    audit_zipcode(zipcode_types, tag.attrib['v'])
                elif is_city(tag):
                    audit_city(city_types, tag.attrib['v'])
                elif is_state(tag):
                    audit_state(state_types, tag.attrib['v'])

    return street_types, zipcode_types, city_types, state_types


'''
Clean a street name by removing everything after a comma,
# sign, the word 'Suite', changing abbreviated directions to full
directions, moving directions from the end of the street to the 
beginning, and finally fixing incorrect street types with the
'mapping' dictionary.
'''
def clean_street(street_name):
    try:
        comma_index = street_name.index(',')
        street_name = remove(street_name,comma_index)
    except:
        pass
        #print street_name
    try:
        pound_index = street_name.index('#')
        street_name = remove(street_name, pound_index)
    except:
        pass
    
    try:
        suite_index = street_name.index('Suite')
        street_name = remove(street_name, suite_index)
    except:
        pass

    end_direction = direction_re.search(street_name)
    if end_direction:
        street_name = street_name[:-len(end_direction.group(0))]
        street_name = end_direction.group(0) + " " + street_name
        try:
            street_name = update_direction(street_name,direction_mapping)
        except:
            pass
    
    try:
        name_array = street_name.split(' ')
        last = name_array[-1]
        name_array[-1] = mapping[last]
        joined = ' '.join(name_array)
        return joined
    except:
        return street_name

'''
Update a direction in a street name by using the provided dictionary.
The direction must already be at the beginning of the street.
'''
def update_direction(name, mapping):
    name_array = name.split(' ')
    first = name_array[0]
    name_array[0] = mapping[first]
    return ' '.join(name_array)

'''
Used by clean_street() to remove everything after commas, #s,
and 'Suite' by finding the index of these.
'''
def remove(name,index):
    subname = name[:index]
    return subname