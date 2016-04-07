from googlemaps import Client
from googlemaps.exceptions import Timeout
from pymongo import MongoClient
import pprint
from time import sleep

APIKEY = "AIzaSyDDj7EvYk-arWEqLFuMZeWcQ7cw6MaPhms"
pp = pprint.PrettyPrinter(indent=4)

gmaps = Client(key=APIKEY)
col = MongoClient()["tubules"]["members"]

# Find all members who don't have location points in already
for member in col.find({"location": {"$exists": False}})[1:]:
    print(member)
    geocode_result = gmaps.geocode(member["address"])
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