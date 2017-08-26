# OpenStreetMap Data Case Study

### Map Area
Tampa, FL, United States

- https://mapzen.com/data/metro-extracts/metro/tampa_florida/

## Problems Encountered in the Map
# City name inconsistencies
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
  - `Tampa  -> Tampa`
  - `Seminole  -> Seminole`
# State inconsistencies
The majority of the data have `FL` as the state in `addr:state`. Otherwise, 
the state is listed as:
  - `Florida`: 24
  - `GA`: 3
  - `Fl`: 3
  - `fl`: 16
  - `florida`: 1
  - `f`: 1
  - `FLq`: 1
