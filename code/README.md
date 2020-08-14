# Code
Auto-download ERA5 data from Copernicus Climate Data Store.

# Setup

1. Copy cdsapi env example file as env file 
```bash
cp ./env/cdsapirc.env.example ./env/cdsapirc.env
```

2. Update `API_KEY`, `UID` and `VERIFY` from https://cds.climate.copernicus.eu/user

# Example dowload request

```python
import cdsapi
from datarequests.era5 import ERA5PressureLevelsRequest

# Generate CDS request client
c = cdsapi.Client()

# Generate request
rq = ERA5PressureLevelsRequest(
    variable=['temperature'],
    year = [1986],
    month = [1],
    day = [17],
)

# Define download location
output = './example.nc'

# Send request
c.retrieve(**rq.request(output))
```