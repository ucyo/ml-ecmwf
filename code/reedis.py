#!/usr/bin/env python
# coding: utf-8

import xarray as xr
from datarequests.era5 import ERA5PressureLevelsRequest
from datarequests.tasks import get_data

req = ERA5PressureLevelsRequest(
    variable=['temperature'],
    year = [1986],
    month = [1],
    day = [17],
    time = ['11:00'],
    pressure_level=[1000]
)
req = req.request("redis.nc")

from rq import Queue
from redis import Redis

# Tell RQ what Redis connection to use
redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)  # no args implies the default queue

job = q.enqueue(get_data, 
          ttl=30,
          kwargs={
              "request":req,
          })


print(job.result)

