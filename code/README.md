# Code
Auto-download ERA5 data from Copernicus Climate Data Store.

# Setup

1. Copy and update env files
```bash
cp ./env/cdsapirc.env.example ./env/.cdsapirc.env
cp ./env/rq.env.example ./env/.rq.env
```

2. Update `API_KEY`, `UID` and `VERIFY` from https://cds.climate.copernicus.eu/user


# Example

```python
from datarequests.era5 import ERA5PressureLevelsRequest

# Request parameters
req = ERA5PressureLevelsRequest(
    variable=['temperature'],
    year = [1987],
    month = [1],
    day = [17],
    time = ['09:00'],
    pressure_level=[800]
)

# Send download request to workers
req.send_request("new_file.nc")
```

# Docker

Scale individual workers
```
docker-compose up -d --build --scale worker=3
```