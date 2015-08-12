import requests

doarama_api_url = "https://www.doarama.com/api/0.2"
doarama_params = {'api-name': 'API-NAME', 'api-key': 'API_KEY', 'Accept': 'application/JSON'}
# doarama_params = {'Accept': 'application/JSON'}


def main():
    #  Query Activity Types
    r = requests.get(doarama_api_url+"/activityType", headers=doarama_params)
    print("Doarama Activity Types: {}".format(r.text))

    user_id = str(1234)

    doarama_params.update({'user-id': user_id})
    files = {'gps_track': open('flightlog.gpx', 'rb')}
    r = requests.post(doarama_api_url+"/activity", headers=doarama_params, files=files)

    print("Doarama Activity Upload: {}".format(r.text))



if __name__ == "__main__":
    print 'before main'
    main()
    print 'after main'
