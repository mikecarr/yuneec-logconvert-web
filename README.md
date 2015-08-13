# Yuneec FlightLog to GPX Converter Webapp

Python Flask Web Application used to convert Yuneec Flightlogs into GPX format which can then be used in various visualization sites

***Disclaimer***: *I have very little experience with Python, I thought I would use this to gain more knowledge and experience*


## Setup

### Python PIP
```
$ pip install requirements.txt
$ python index.py
```

Open browser to http://localhost:5000

### Virtualenv
It creates an environment that has its own installation directories, that doesn’t share libraries with other virtualenv environments (and optionally doesn’t access the globally installed libraries either).

https://virtualenv.pypa.io/en/latest/

## Doarama

### Activity Type
```
  {
    "id": 30,
    "name": "Fly - UAV / Drone"
  }
```

## Debugging
drop a gpx file here http://nationalmap.gov.au/

## Visualization Sites
* http://www.doarama.com/
* http://www.gpsvisualizer.com/
* http://maplorer.com/view_gpx.html
* http://veloroutes.org/upload/ (slow)

## References
* https://developers.google.com/kml/articles/csvtokml
* http://www.doarama.com/api/0.2/docs
* http://www.rigacci.org/wiki/doku.php/tecnica/gps_cartografia_gis/gpx
* https://github.com/AaronColby/doarama_api_php_lib/blob/master/generic_doarama_lib.php
* http://flask.readthedocs.org/en/0.2/patterns/sqlite3/
