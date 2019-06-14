import json
import requests
import constants
import todoist

class apiCalls:

    def __init__(self):
        self.request =  "Hello RWorld"

    def basicAPICall(self):
        return "hello world"

    # Returns json script of weather api
    # Default is the location of the device
    # Backup is New York (City - I think??)
    def weatherAPICall(self, city="New+York"):
        apiKey = constants.OPEN_WEATHER_APIKEY

        location = self.ipGEOLocationAPICall()

        if location is not None:
            url = "https://api.openweathermap.org/data/2.5/forecast?lat="+str(location[0])+"&lon="+str(location[1]) + \
                  "&appid="+apiKey
        else:
            url = "https://api.openweathermap.org/data/2.5/forecast?q="+city+",us&appid="+apiKey

        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            # Need to figure out what is the relavent information in the body of the call
            # Depends on kivy app setup
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    # Returns array of latitude and longitude of calling device
    def ipGEOLocationAPICall(self):
        apiKey = constants.IP_DATA_LOC_APIKEY
        url = "https://api.ipdata.co?api-key=" + apiKey

        response = requests.get(url)
        if response.status_code == 200:
            json_response = json.loads(response.content.decode('utf-8'))
            location = [round(json_response.get('latitude')), round(json_response.get('longitude'))]
            print(location)
            return location
        else:
            return None

    # Returns array of quote and author
    def quoteAPICall(self):
        url = 'https://quotes.rest/qod'

        response = requests.get(url)
        if response.status_code == 200:
            json_response = json.loads(response.content.decode('utf-8'))
            return [json_response.get("contents").get("quotes")[0].get("quote"),
                    json_response.get("contents").get("quotes")[0].get("author")]
        else:
            return None

    # Returns array of active Todoist tasks
    def todoistAPICall(self):
        apiKey = constants.TODOIST_APIKEY
        url = "https://beta.todoist.com/API/v8/tasks"

        response = requests.get(url,
                                headers={
                                    "Authorization": "Bearer %s" % apiKey
                                })

        if response.status_code== 200:
            return response.json()
        else:
            return None

