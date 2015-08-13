import requests, json

debug = False

doarama_api_url = "https://www.doarama.com/api/0.2/"
doarama_params = {'api-name': 'yuneec-logconvert-web', 'Accept': 'application/JSON'}

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client

http_client.HTTPConnection.debuglevel = 1

def display_debug(r):
    print r.url
    print r.headers
    print r.text
    print r

def post_file(user_id, payload):
    print("\n\n*********Upload GPX Data *********")
    files = {'gps_track': payload}
    r = requests.post(doarama_api_url+"activity", headers=doarama_params, files=files)
    if(debug):
        display_debug(r)

    json_response = json.loads(r.text)
    post_id =  json_response['id']

    return post_id

def set_activity_info(activity_type_id, post_id):
    print("\n\n*********Set Activity Info *********")
    payload = { 'activityTypeId' : activity_type_id}
    r = requests.post(doarama_api_url+'activity/' + str(post_id), headers=doarama_params, json=payload)
    if(debug):
        display_debug(r)

def create_visualisation(post_id):
    print("\n\n*********Create Visualisation *********")
    payload = { 'activityIds' : [post_id]}
    r = requests.post(doarama_api_url+"visualisation", headers=doarama_params, json=payload)
    if(debug):
        display_debug(r)
    json_response = json.loads(r.text)
    key_id =  json_response['key']
    return key_id

def main():

    #  Query Activity Types
    # print("\n\n*********Query Activity Types *********")
    # r = requests.get(doarama_api_url+"activityType", headers=doarama_params)
    # if(debug):
    #     display_debug(r)
    # print("Doarama Activity Types: {}".format(r.text))

    flightlog_data = open('flightlog.gpx', 'rb')
    user_id = str(1234)
    doarama_params.update({'user-id': user_id})

    post_id = post_file(user_id, flightlog_data)
    print("Activity Id: " + str(post_id))

    set_activity_info(30,post_id)

    key_id = create_visualisation(post_id)
    print 'keyid: ' + key_id

if __name__ == "__main__":
    print 'Starting'
    main()

