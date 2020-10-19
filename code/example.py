#!/usr/bin/env python
# coding: utf-8

from datarequests.era5 import ERA5PressureLevelsRequest
from datarequests.defaults import year, month

for v in ["temperature"]:
    for y in ["1979"]:
        for m in month():        
            req = ERA5PressureLevelsRequest(
                variable=[v],
                year=[y],
                month=[m]
            )
            req.send_request(f"/abcde/{y}/{m}/ERA5.pl.{v}.nc")
