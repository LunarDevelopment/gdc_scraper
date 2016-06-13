from googlemaps import Client
from googlemaps.exceptions import Timeout
import pprint
from time import sleep
from pymongo import UpdateOne

APIKEY = "AIzaSyDDj7EvYk-arWEqLFuMZeWcQ7cw6MaPhms"


class GmapsGeocoder():

    def __init__(self, members, data_store, gmaps=Client(key=APIKEY)):
        """
        @param members - Queue - queue of members that need to have their locations found
        @param gmaps - GoogleMaps Client - Gmaps client for making address requests.
        @param data_store - Queue - queue to push
        """
        self.gmaps = gmaps
        self.members = members
        self.data_store = data_store

    def get_member_location(self, member):
        address = member.get("address", False)
        print("address: {}".format(address))
        if not address:
            return False

        geocode_result = self.gmaps.geocode(address)
        # check if we have a result?
        if len(geocode_result) > 0:
            return geocode_result[0]["geometry"]["location"]
        else:
            print(geocode_result)
            print("Not enough results found")
            return False

    def get_member_locations(self):
        # while queue is not empty
        while not self.members.empty():
            member = self.members.get()
            geoPoint = self.get_member_location(member)
            print("geoPoint = {}".format(geoPoint))
            if geoPoint:
                self.data_store.append(
                    UpdateOne(
                        {"_id": member["_id"]},
                        {"$set": {"location": geoPoint}},
                        upsert=True
                    )
                )

            self.members.task_done()


if __name__ == "__main__":
    from pymongo import MongoClient
    from threading import Thread
    from queue import Queue

    c = MongoClient()["tubules"]["members"]
    no_location_members = c.find({"location": {"$exists": False}})

    # client = Client(key=APIKEY)
    members = Queue()
    data_store = []

    g = GmapsGeocoder(members, data_store)
    threads = [Thread(target=g.get_member_locations) for i in range(10)]

    for i in no_location_members:
        members.put(i)

    for t in threads:
        t.start()
    try:
        members.join()
    except Exception:
        print("In exception")
    finally:
        c.bulk_write(data_store)








# pp = pprint.PrettyPrinter(indent=4)

# col = MongoClient()["tubules"]["members"]

# # Find all members who don't have location points in already
# for member in col.find({"location": {"$exists": False}})[1:]:
#     print(member)
#     geocode_result = self.gmaps.geocode(member["address"])
#     if len(geocode_result) > 0:
#         try:
#             pp.pprint(geocode_result[0]["geometry"]["location"])
#             update_result = col.update(
#                 {"address": member["address"]},
#                 {"$set": {"location": geocode_result[0]["geometry"]["location"]}}
#             )
#             print(update_result)
#         except KeyError as e:
#             with open("error_maps/KeyErrorException", "w") as file:
#                 file.write("{}\n\n{}".format(member, str(e.args)))
#         except Timeout as e:
#             print(e)
#             time = 2 * (60 * 60)  # 2 hours
#             print("Sleeping {} seconds".format(time))
#             update_diff = 10 * 60  # 2 Minutes
#             while time > 0:
#                 sleep(update_diff)
#                 time -= update_diff
#     else:
#         print("FUCKED Up")
#         with open("error_maps/{}".format(str(member["_id"])), "w") as file:
#             file.write(str(member))