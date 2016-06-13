import requests
import pprint
import json


class MapquestGeocoder():

    def __init__(self, members, data_store):
        """
        @param members - Queue - queue of members that need to have their locations found
        @param data_store - Queue - queue to push
        """
        self.members = members
        self.data_store = data_store

    def get_member_location(self, addresses):
        """
        Makes a request to map quests geolocate api
        :param address: List of strings. Strings containing addresses
        :return: Dictionary of latitude and longitude values
        """
        geolocateURL = "http://www.mapquestapi.com/geocoding/v1/batch"

        location = [address for address in addresses]

        param_dic = {
            "key": "Hd2ApA1S2mqJF2IU5nsOJhvjJv9x1ZqD",
            "outFormat": "json",
            "thumbMaps": False,
            "json": json.dumps({"locations": location})
        }

        return requests.get(geolocateURL, params=param_dic)


def filter_address_string(address):
    """
    @param address: string containing address which will be split up into consitituent parts
    @return Dictionary: Dictionary to be passed onto mapquest locations array
    """
    pass

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=2)
    # g = MapquestGeocoder(None, None)
    # l = g.get_member_location([
    #     {"address": "27 Mountbel Road, Stanmore, UK"},
    #     {"address": "22 Market Rd, London N7 9GT, UK"}
    # ])
    l = geolocate([
        {"postalCode": "ha7 2ag", "country": "United Kingdom"},
        {"postalCode": "LE11 3DU", "country": "United Kingdom"}
    ])
    print(l.url)
    pp.pprint(l.json())
    print(l.url)
    for address in l.json()["results"]:
        print(address["providedLocation"])
        print(address["locations"][0]['latLng'])
