import requests
import json
import numpy as np
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
TOKEN_URL = 'https://consent.swisscom.com/o/oauth2/token'
client_id = 'vjM3xDUK2Con9zy4D8d8SqZjS3jYEQ28'
client_secret = 'rsConE5RAlKqD6QB'
# See https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow.
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
# Fetch an access token.
oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret)
print(oauth.access_token)

'''
Function to get the tiles for given municipality
'''
def get_tiles (municipality):
    # Use the access token to query an endpoint.
    resp = oauth.get(
        'https://api.swisscom.com/layer/heatmaps/demo/grids/municipalities/' + municipality,
        headers={'scs-version': '2'})
    #print(resp.json())
    res_json = resp.json()
    val = next(iter(res_json.values()))
    result = [sub['tileId']for sub in val]
    return result
#run the function for each municipality
lausanne_tiles = get_tiles('5586')
zurich_tiles = get_tiles('261')
geneva_tiles = get_tiles('6621')

# split the tile ids into 100 
lausanneTilesSplit = [lausanne_tiles[i:i + 100] for i in range(0, len(lausanne_tiles), 100) ]
zurichTilesSplit = [zurich_tiles[i:i + 100] for i in range(0, len(zurich_tiles), 100) ]
genevaTilesSplit = [geneva_tiles[i:i + 100] for i in range(0, len(geneva_tiles), 100) ]

# date and hour data
dates = ['2019-03-25', '2019-03-26', '2019-03-27', '2019-03-28', '2019-03-29', '2019-03-30','2019-03-31', 
         '2020-03-23', '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29']
hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', 
         '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00',
         '22:00', '23:00', '24:00']

'''
Function to get the daily data for density and demographics
'''
def getDaily (info, tiles):
    TOKEN_URL = 'https://consent.swisscom.com/o/oauth2/token'
    client_id = 'vjM3xDUK2Con9zy4D8d8SqZjS3jYEQ28'
    client_secret = 'rsConE5RAlKqD6QB'
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret)
    for date in dates:
        for tile in tiles:
            print('https://api.swisscom.com/layer/heatmaps/demo/heatmaps/dwell-' 
                  + info + '/daily/' + date +'?tiles='
                + str(','.join(str(i) for i in tile)))
            resp = oauth.get(
                'https://api.swicsscom.com/layer/heatmaps/demo/heatmaps/dwell-demographics/daily/' + date +'?tiles='
                + str(','.join(str(i) for i in tile)), headers={'scs-version': '2'})
    result = resp.json()
    return result
   
'''
Function to get the hourly data for density and demographics
'''
def getHourly (info, tiles):
    TOKEN_URL = 'https://consent.swisscom.com/o/oauth2/token'
    client_id = 'vjM3xDUK2Con9zy4D8d8SqZjS3jYEQ28'
    client_secret = 'rsConE5RAlKqD6QB'
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret)
    for date in dates:
        for hour in hours:
            for tile in tiles:
                resp = oauth.get(
                    'https://api.swicsscom.com/layer/heatmaps/demo/heatmaps/dwell-' + info +'/daily/' +  date + 'T' + hour + '?tiles=' + str(','.join(str(i) for i in tile)), 
                    headers={'scs-version': '2'})
    result = resp.json()
    return result
    
# run the function for density and demographics
lausanneDensityDaily = getDaily('density', lausanneTilesSplit)
zurichDensityDaily = getDaily('density', zurichTilesSplit)
genevaDensityDaily = getDaily('density', genevaTilesSplit)

lausanneDemographicDaily = getDaily('demographics', lausanneTilesSplit)
zurichDemographicDaily = getDaily('demographics', zurichTilesSplit)
genevaDemographicDaily = getDaily('demographics', genevaTilesSplit)

lausanneDensityHourly = getHourly('density', lausanneTilesSplit)
zurichDensityHourly = getHourly('density', zurichTilesSplit)
genevaDensityHourly = getHourly('density', genevaTilesSplit)

lausanneDemographicHourly = getHourly('demographics', lausanneTilesSplit)
zurichDemographicHourly = getHourly('demographics', zurichTilesSplit)
genevaDemographicHourly = getHourly('demographics', genevaTilesSplit)
