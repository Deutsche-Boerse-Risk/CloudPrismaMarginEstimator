"""Submit new API definition to SwaggerHub.
   Reads key from SWAGGERHUB_KEY environment variable."""

import os
import requests
import sys

SWAGGER_FILE = 'swagger.yaml'
SWAGGERHUB_API = dict(
    DEV ='https://api.swaggerhub.com/apis/dbgservice/cPME-dev',
    SIMU='https://api.swaggerhub.com/apis/dbgservice/cPME-sandbox',
    PROD='https://api.swaggerhub.com/apis/dbgservice/cPME'
)

if len(sys.argv) < 2:
    print("Error: environment expected as command line argument, one or more of %s" % SWAGGERHUB_API.keys())
    exit(2)

if 'SWAGGERHUB_KEY' not in os.environ:
    print("Error: SWAGGERHUB_KEY environment variable not found")
    exit(2)
SWAGGERHUB_KEY = os.environ['SWAGGERHUB_KEY']

with open(SWAGGER_FILE, 'r') as infile:
    swagger = infile.read()
    for env in sys.argv[1:]:
        if env not in SWAGGERHUB_API:
            print("Error: %s is not a valid environment" % env)
            continue
        api = SWAGGERHUB_API[env]
        rsp = requests.post(api,
                            data=swagger,
                            headers={'Content-Type': 'application/yaml', 'Authorization': SWAGGERHUB_KEY}
                           )
        if rsp.status_code != 200:
            print("POST %s ERROR %d: %s\nbody: %s" % (api, rsp.status_code, rsp.text, swagger[0:400]))
        else:
            print("POST %s OK %d" % (api, rsp.status_code))
