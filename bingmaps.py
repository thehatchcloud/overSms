import requests
import json

class Map(object):

    def __init__(self, bing_maps_key):
        self.bing_maps_url = 'http://dev.virtualearth.net/REST/V1/Routes/Driving'
        self.bing_maps_key = bing_maps_key
        self.distance_unit = 'mi'
    

    def get_directions(self, dir_request):

        if 'from:' in dir_request and 'to:' in dir_request:
            dir_request = dir_request.replace('from: ', 'from:').replace('to: ', 'to:')
            to_location = dir_request.find('to:')
            wp0 = dir_request[5:to_location-1]
            wp1 = dir_request[to_location+3:]

            querystring = {
                'wp.0': f'{wp0}',
                'wp.1': f'{wp1}',
                'du': self.distance_unit,
                'key': self.bing_maps_key
            }

            #print(querystring)

            response = requests.request("GET", self.bing_maps_url, params=querystring)
            text = response.text
            obj = json.loads(text)
            #pprint(obj)

            directions = obj['resourceSets'][0]['resources'][0]
            routeLegs = directions['routeLegs']
            totalDistance = round(directions['travelDistance'], 2)
            totalDuration = directions['travelDuration']
            if totalDuration < 3600:
                totalDuration = round(totalDuration/60, 2)
                durationUnit = 'minutes'
            else:
                totalDuration = round((totalDuration/60)/60, 2)
                durationUnit = 'hours'
            itineraryItems = routeLegs[0]['itineraryItems']

            sms_directions = ''

            for item in itineraryItems:
                travelDistance = round(item['travelDistance'], 2)
                if item['instruction']['maneuverType'] == 'DepartStart':
                    sms_directions += (f"\u25CF Heading {item['compassDirection']},"
                         f" {item['instruction']['text']} - {travelDistance} mi.\n")
                else:
                    sms_directions += f"\u25CF {item['instruction']['text']} - {travelDistance} mi.\n"
            
            sms_directions += f'\n\u25FC Total distance: {totalDistance} mi\n'
            sms_directions += f'\u25FC Total duration: {totalDuration} {durationUnit}'

            return sms_directions

