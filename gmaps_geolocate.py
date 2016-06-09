from googlemaps import Client
from googlemaps.exceptions import Timeout
from pymongo import MongoClient
import pprint
from time import sleep

APIKEY = "AIzaSyDDj7EvYk-arWEqLFuMZeWcQ7cw6MaPhms"


class GmapsGeocoder():

    def __init__(self, members, data_store, gmaps=Client(key=APIKEY)):
        """
        @param members - Queue - queue of members that need to have their locations found
        @param gmaps - GoogleMaps Client - Gmaps client for making address requests.
        @param data_store - Queue - queue to push 
        """
        self.gmaps =  gmaps
        self.members = members

    def get_member_location(self, member):
        geocode_result = self.gmaps.geocode(member["address"])
        #check if we have a result?
        if len(geocode_result) > 0:
            return geocode_result[0]["geometry"]["location"]
        else:
            return False

    def get_member_locations():
        # while queue is not empty
        while not self.queue.empty():
            member = self.queue.get()
            geoPoint = self.get_member_location(member)

            if geoPoint:
                self.data_store.push(geoPoint[0]["geometry"]["location"])






pp = pprint.PrettyPrinter(indent=4)

col = MongoClient()["tubules"]["members"]

# Find all members who don't have location points in already
for member in col.find({"location": {"$exists": False}})[1:]:
    print(member)
    geocode_result = self.gmaps.geocode(member["address"])
    if len(geocode_result) > 0:
        try:
            pp.pprint(geocode_result[0]["geometry"]["location"])
            update_result = col.update(
                {"address": member["address"]},
                {"$set": {"location": geocode_result[0]["geometry"]["location"]}}
            )
            print(update_result)
        except KeyError as e:
            with open("error_maps/KeyErrorException", "w") as file:
                file.write("{}\n\n{}".format(member, str(e.args)))
        except Timeout as e:
            print(e)
            time = 2 * (60 * 60)  # 2 hours
            print("Sleeping {} seconds".format(time))
            update_diff = 10 * 60  # 2 Minutes
            while time > 0:
                sleep(update_diff)
                time -= update_diff
    else:
        print("FUCKED Up")
        with open("error_maps/{}".format(str(member["_id"])), "w") as file:
            file.write(str(member))