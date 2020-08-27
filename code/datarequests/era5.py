from dataclasses import dataclass, field
from . import variables
from . import defaults
from . import tasks
import hashlib
import json
from rq import Queue, exceptions
from rq.job import Job
from redis import Redis

REDIS_CONNECTION = Redis(host="redis")
QUE = Queue(
    connection=REDIS_CONNECTION,
    default_timeout="1h",
)


@dataclass
class _ECMWF:
    """Base class for an ERA5 data request.

    The base case handles common parameters of each request.
    These parameters are:

    - Variable                          (mandatory)
    - Latitude/Longitude boundaries     (optional; N [-90;90] and E [-180;180])
    - Year                              (optional; [1979;2020])
    - Month                             (optional; [1;12])
    - Time                              (optional; [00:00, 01:00, ..., 23:00])
    """

    variable: list
    lat_boundary: tuple = None  # (90,-90)
    lon_boundary: tuple = None  # (-180,180)

    year: list = field(default_factory=defaults.year)
    month: list = field(default_factory=defaults.month)
    time: list = field(default_factory=defaults.time)

    def __post_init__(self):
        self.format = "netcdf"
        self.product_type = "reanalysis"
        self._check_area()
        self.month = self._check_range(self.month, 1, 13, "month", "{:02}")
        self.year = self._check_range(self.year, 1979, 2021, "year", "{:04}")
        self.time = self._check_membership(self.time, defaults.time(), "time")

    def _check_area(self):
        self.area = [90, -180, -90, 180]
        if self.lat_boundary is not None and len(self.lat_boundary) == 2:
            self.area[0] = max(self.lat_boundary)
            self.area[2] = min(self.lat_boundary)
            self.lat_boundary = None
        if self.lon_boundary is not None and len(self.lon_boundary) == 2:
            self.area[3] = max(self.lon_boundary)
            self.area[1] = min(self.lon_boundary)
            self.lon_boundary = None

    @staticmethod
    def _check_membership(candidates, allowed_list, name):
        allowed = set(allowed_list)
        if not allowed.issuperset(candidates):
            result = allowed.intersection(candidates)
            if not result:
                raise KeyError(f"None of the {name} are allowed")
            print(f"Not all {name} allowed.")
            print(f"Changed {name} list to: {result}")
            return list(result)
        return list(candidates)

    @staticmethod
    def _check_range(candidates, minimum, maximum, name, formatting):
        msg = f"{name} are wrong: {candidates}"
        assert all([int(x) >= minimum and int(x) < maximum for x in candidates]), msg
        return [formatting.format(int(x)) for x in candidates]

    @property
    def _request(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def request():
        raise NotImplementedError("Not implemented for base class")

    def send_request(self, output):
        req = self.request(output)
        if self.job_status in ("finished", "failed", "queued"):
            print(self.job_status)
            return self.job_status
        job = QUE.enqueue(
            tasks.get_data,
            result_ttl=31536000,  # 1 year
            failure_ttl=31536000,  # 1 year
            job_id=self.job_id,
            description=output,
            kwargs={"request": req},
        )
        print(job.get_status())
        return job

    @property
    def job_status(self):
        try:
            j = Job.fetch(self.job_id, connection=REDIS_CONNECTION)
        except exceptions.NoSuchJobError as e:
            return None  # Apparently job is not in queue, hence no status
        else:
            return j.get_status()

    @property
    def job_id(self):
        return hashlib.md5(
            json.dumps(self._request, sort_keys=True).encode("utf-8")
        ).hexdigest()


@dataclass
class ERA5PressureLevelsRequest(_ECMWF):
    """Request hourly ERA5 data on pressure levels.

    Request for ERA5 data on pressure level. This class extends the base
    class with following parameters (for details [0]):

    - Variable   (mandatory; restricted possible values (for details [1]))
    - Day        (optional; [1;31])

    [0] https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview
    [1] [variables.py](./variables.py)
    """

    day: list = field(default_factory=defaults.day)
    pressure_level: list = field(default_factory=defaults.pl)

    def __post_init__(self):
        super(ERA5PressureLevelsRequest, self).__post_init__()
        self._check_pl()
        self.day = self._check_range(self.day, 1, 32, "day", "{:02}")
        self.variable = self._check_membership(
            self.variable, variables.PRESSURE_LEVELS, "variables"
        )

    def _check_pl(self):
        allowed = set(defaults.pl())
        if not allowed.issuperset([str(x) for x in self.pressure_level]):
            result = allowed.intersection(self.pressure_level)
            if not result:
                raise KeyError("None of the pressure levels are allowed")
            self.pressure_level = list(result)
            print("Not all pressure levels allowed.")
            print(f"Changed variables list to: {self.pressure_level}")
        self.pressure_level = [str(x) for x in self.pressure_level]

    @property
    def name(self):
        return "reanalysis-era5-pressure-levels"

    def request(self, filepath):
        return dict(name=self.name, request=self._request, target=filepath)


@dataclass
class ERA5SingleLevelsRequest(_ECMWF):
    """Request hourly ERA5 data on single levels.

    Request for ERA5 data on pressure level. This class extends the base
    class with following parameters (for details [0]):

    - Variable   (mandatory; restricted possible values (for details [1]))
    - Day        (optional; [1;31])

    [0] https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview
    [1] [variables.py](./variables.py)
    """

    day: list = field(default_factory=defaults.day)

    def __post_init__(self):
        super(ERA5SingleLevelsRequest, self).__post_init__()
        self.day = self._check_range(self.day, 1, 32, "day", "{:02}")
        self.variable = self._check_membership(
            self.variable, variables.SINGLE_LEVELS, "variables"
        )

    @property
    def name(self):
        return "reanalysis-era5-single-levels"

    def request(self, filepath):
        return dict(name=self.name, **self._request, target=filepath)
