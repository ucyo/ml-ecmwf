#!/usr/bin/env python
# coding: utf-8

from datarequests.era5 import ERA5PressureLevelsRequest

req = ERA5PressureLevelsRequest(
    variable=["temperature"],
    year=[1986],
    month=[1],
    day=[17],
    time=["11:00"],
    pressure_level=[800],
)

req.send_request("/downloads/redic.nc")
