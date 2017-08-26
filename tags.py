
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        key = element.get("k")
        #print key
        if problemchars.search(key):
            keys['problemchars'] += 1
            #print '--> problemchars'
        elif lower_colon.search(key):
            keys['lower_colon'] += 1
            #print '--> lower_colon'
        elif lower.search(key):
            keys['lower'] += 1
            #print '--> lower'
        else:
            keys['other'] += 1
            #print '--> other'
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys