import requests
import pprint

def geolocate(address):
    """
    Makes a request to map quests geolocate api
    :param address: List of strings. Strings containing addresses
    :return: Dictionary of latitude and longitude values
    """
    geolocateURL = "http://www.mapquestapi.com/geocoding/v1/batch"

    params = []
    for location in address:
        params.append(["location", location])

    param_dic = {
        "key": "Hd2ApA1S2mqJF2IU5nsOJhvjJv9x1ZqD",
        "outFormat": "json",
        "thumbMaps": False
    }

    for key, value in param_dic.items():
        params.append([key, value])

    return requests.get(geolocateURL, params=params)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    l = geolocate(["27 Mountbel Road, Stanmore, UK", "22 Market Rd, London N7 9GT, UK"])
    # print(l.url)
    # print(l.text)
    print(l.json())
    for address in l.json()["results"]:
        print(address["providedLocation"]["location"])
        print(address["locations"][0]['latLng'])

