"""Submit new API definition to SwaggerHub.
   Reads key from SWAGGERHUB_KEY environment variable."""

import os
import requests
import sys

SWAGGER_FILE = {  # "-prod" suffix will be added for PROD environment, e.g. "swagger-prod.yaml"
        '1': 'swagger.yaml',
        '2': 'swagger2.yaml'
    }
SWAGGERHUB_API = dict(
        DEV ='https://api.swaggerhub.com/apis/dbgservice/cPME-dev',
        SIMU='https://api.swaggerhub.com/apis/dbgservice/cPME-sandbox',
        PROD='https://api.swaggerhub.com/apis/dbgservice/cPME'
    )

if len(sys.argv) < 3:
    print("Usage: %s <version> <environment> [environment2] [environment3] ..." % sys.argv[0])
    exit(2)

if sys.argv[1] not in SWAGGER_FILE:
    print("Versions: %s\n" % list(SWAGGER_FILE.keys()))
    exit(2)

if any([a not in SWAGGERHUB_API for a in sys.argv[2:]]):
    print("Environments: %s\n" % list(SWAGGERHUB_API.keys()))
    exit(2)

if 'SWAGGERHUB_KEY' not in os.environ:
    print("Error: SWAGGERHUB_KEY environment variable not found")
    exit(2)
SWAGGERHUB_KEY = os.environ['SWAGGERHUB_KEY']

for env in sys.argv[2:]:
    filename = SWAGGER_FILE[sys.argv[1]]
    if 'PROD' in env:
        filename = filename.replace('.yaml', '-prod.yaml')
    print("posting %s to %s" % (filename, env))
    with open(filename, 'r') as infile:
        swagger = infile.read()
        if env not in SWAGGERHUB_API:
            print("Error: %s is not a valid environment" % env)
            continue
        api = SWAGGERHUB_API[env]
        rsp = requests.post(api,
                            data=swagger,
                            headers={'Content-Type': 'application/yaml', 'Authorization': SWAGGERHUB_KEY}
                           )
        if rsp.status_code == 200:
            print("POST %s OK" % (api))
        elif rsp.status_code == 201:
            print("POST %s CREATED NEW VERSION" % (api))
        else:
            print("POST %s ERROR %d: %s\nbody: %s" % (api, rsp.status_code, rsp.text, swagger[0:400]))

