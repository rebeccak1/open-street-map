
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
direction_re = re.compile(r'\w*(North|South|East|West|Northeast|Northwest|Southeast|Southwest|S|NE|W|N|E|SE|N.)$')

direction_mapping = {"N":"North",
                    "S":"South",
                    "NE":"Northeast",
                    "W":"West",
                    "E":"East",
                    "SE": "Southeast"}

expected = ["Passage","Cutoff","Bridge","Crossing","Lane","Way","Run","Loop","Plaza","Causeway","Terrace","Highway","Bayway","Circle","Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

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

def audit_state(state_name):
    if state_name != 'FL':
        state_name = 'FL'

def audit_street_type(street_types, street_name):
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
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_city(invalid_cities, city_name):
    if city_name not in cities:
        if city_name in city_mapping:
            city_name = city_mapping[city_name]
        else:
            invalid_cities[city_name] += 1       

def audit_zipcode(invalid_zipcodes, zipcode):
    if not re.match(r'^\d{5}$', zipcode):
        invalid_zipcodes[zipcode] += 1
             
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_state(elem):
    return (elem.attrib['k'] == "addr:state")
    
def is_city(elem):
    return (elem.attrib['k'] == "addr:city")

def is_zipcode(elem):
    return 'zip' in elem.attrib['k']

def audit(osmfile):
    osm_file = open(osmfile, "r")
    
    street_types = defaultdict(set)
    city_types = defaultdict(int)
    zipcode_types = defaultdict(int)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_zipcode(tag):
                    audit_zipcode(zipcode_types, tag.attrib['v'])
                elif is_state(tag):
                    audit_state(tag.attrib['v'])
                elif is_city(tag):
                    audit_city(city_types, tag.attrib['v'])

    return street_types, zipcode_types


def update_name(name, mapping):
    name_array = name.split(' ')
    last = name_array[-1]
    name_array[-1] = mapping[last]
    joined = ' '.join(name_array)
    return joined

def update_direction(name, mapping):
    name_array = name.split(' ')
    first = name_array[0]
    name_array[0] = mapping[first]
    return ' '.join(name_array)

def remove(name,index):
    subname = name[:index]
    return subname