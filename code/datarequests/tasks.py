import cdsapi

c = cdsapi.Client()


def get_data(request):
    c.retrieve(**request)
