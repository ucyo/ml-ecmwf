#!/usr/bin/env python
# coding: utf-8

from datarequests.era5 import ERA5PressureLevelsRequest
from datarequests.defaults import year, month


variables = [
    "geopotential",
    "specific_humidity",
    "temperature",
    "u_component_of_wind",
    "v_component_of_wind",
]


for v in variables:
    for y in ["1979"]:
        for m in month():        
            req = ERA5PressureLevelsRequest(
                variable=[v],
                year=[y],
                month=[m]
            )
            req.send_request(f"/abcde/{y}/{m}/ERA5.pl.{v}.nc")
