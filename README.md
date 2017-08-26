# OpenStreetMap Data Case Study

### Map Area
Tampa, FL, United States

- https://mapzen.com/data/metro-extracts/metro/tampa_florida/

## Data Audit
### Unique Tags
Use `mapparser.py` to find the unique tags: 
- `bounds`: 1
- `member`: 31857
- `nd`: 1957582
- `node`: 1655566
- `osm`: 1
- `relation`: 1252
- `tag`: 1131585
- `way`: 182866
### Patterns in the Tags
- `lower`: 575997
- `lower_colon`: 520908
- `other`: 34675
- `problemchars`: 5
## Problems Encountered in the Map
### City name inconsistencies
Use `audit.py` to clean city names:
- Capitalization:
  - `spring hill -> Spring Hill`
  - `SPRING HILL -> Spring Hill`
  - `port richey -> Port Richey`
  - `lutz -> Lutz`
  - `tampa -> Tampa`
- Spelling
  - `Clearwarer Beach -> Clearwater Beach`
  - `St Petersbug -> St. Petersburg`
  - `Zephyhills -> Zephyrhills`
  - `Miakka -> Old Myakka`
- Punctuation
  - `St. Petersburg, FL -> St. Petersburg`
  - `St Pete Beach -> St. Pete Beach`
  - `Saint Petersburg -> St. Petersburg`
  - `Land O Lakes, FL -> Land O' Lakes`
  - `Land O Lakes -> Land O' Lakes`
  - `Palm Harbor, Fl. -> Palm Harbor`
  - `'Tampa  '-> Tampa`
  - `'Seminole  '-> Seminole`
### State inconsistencies
Use `audit.py` to clean state names:
The majority of the data have `FL` as the state in `addr:state`. Otherwise, 
the state is listed as:
  - `Florida`: 24
  - `GA`: 3
  - `Fl`: 3
  - `fl`: 16
  - `florida`: 1
  - `f`: 1
  - `FLq`: 1
### Zip code inconsistencies
  - There are a few inconsistent zip codes, all of which have a length longer than 5. For example:
    - 33548:33556
    - 34669; 34667; 34667
