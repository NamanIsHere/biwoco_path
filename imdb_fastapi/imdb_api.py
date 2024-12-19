"""
Main application file for FastAPI.
This module sets up the FastAPI app and includes movie-related endpoints.
"""

import sys
import json
from fastapi import FastAPI
from imdb_fastapi.routes.route import endPoints

sys.path.append(".")
app = FastAPI()
app.include_router(endPoints, prefix="/api/movies")

@app.get('/')
def root():
    """
    Root endpoint.

    :return: A welcome message indicating that the API is running.
    """
    return{
        'message': 'Fast API is running!',
        'List of regions code use for API':
        """\
AF, AL, AS, AI, AR, AM, AU, AT, BD, BB, BY, BE, BJ, BM,\
BR, KH, CM, CA, CF, CL, CN, CC, CO, CR, HR, CU, CW, CY,\
CZ, DK, DM, DO, EC, EG, GQ, EE, FI, FR, GF, GA, GM, GE,\
DE, GR, GN, GW, HK, HU, IS, IN, ID, IR, IE, IL, IT, JP,\
KZ, KW, LV, LB, LR, LY, LT, LU, MO, MY, MV, MH, MX, ME,\
MM, NP, NL, NZ, NI, NG, NO, PK, PY, PE, PH, PL, PT, PR,\
QA, RO, RU, SA, RS, SG, SK, SI, ZA, KR, ES, LK, SE, CH,\
TW, TH, TR, UA, AE, GB, US, UY, VE, VN
        """
        }
