from unittest import TestCase
from mapquest import MapquestGeocoder, test_filter_address
from pprint import pprint


class test_mapquest(TestCase):

    def coordinate_checker(self, mapQuestResponse, expectedResponse):
        """
        Helper function for checking coordinates a and b are roughly similar
        (Only required similarity is to 3 decimal place)
        """
        print(mapQuestResponse.json())
        for index, address in enumerate(mapQuestResponse.json()["results"]):
            print("checking address: {}".format(address["providedLocation"]))
            mapQuest = address["locations"][0]['latLng']
            expected = expectedResponse[index]
            self.assertAlmostEqual(mapQuest["lat"], expected["lat"], 3)
            self.assertAlmostEqual(mapQuest["lng"], expected["lng"], 3)

    def test_mapquest_get_member_location(self):
        # Given
        g = MapquestGeocoder(None, None)
        correctAddresses = [
            {'lng': -0.3232248, 'lat': 51.60104279999999},
            {"lat": 52.7706876, "lng": -1.2089334}
        ]

        # When
        l = g.get_member_location([
            {"postalCode": "ha7 2ag", "country": "United Kingdom"},
            {"postalCode": "LE11 3DU", "country": "United Kingdom"}
        ])

        # Then
        self.coordinate_checker(l, correctAddresses)

    def test_mapquest_get_member_location_without_address(self):
        # Given
        g = MapquestGeocoder(None, None)

        # When
        l = g.get_member_location([{"noAddress": "address"}])

        # Then
        self.assertFalse(l)

    # def test_mapquest_get_member_location_unclear_address(self):
    #     # TODO decide on specs for this?
    #     g = mapquest(None, None)

    #     l = g.get_member_location([{"address": "Somewhere In scotland"}])
    #     print(l.body)
    #     assert(False)

    # def test_mapquest_get_member_location_isle_of_man(self):
    #     # Given
    #     g = MapquestGeocoder(None, None)
    #     addresses = [
    #         {"street": "27 Mountbel Road, ha7 2ag"},
    #         {"street": "47 Derby Square, Douglas, Isle of Man, IM1 3LP", "country": "Isle of Man"},
    #         {"street": "26 Grawen Street, Porth, Rhondda Cynon Taff, CF39 0BU", "country:": "United Kingdom"}
    #     ]

    #     correctGeoCoordinate = [
    #         # mountbel
    #         {'lng': -0.3232248, 'lat': 51.60104279999999},
    #         # isle of man
    #         {"lat": 54.1562134, "lng": -4.4822503},
    #         # Whales
    #         {"lat": 51.61578, "lng": -3.415012}
    #     ]

    #     # When
    #     l = g.get_member_location([{"street": "47 Derby Square, Douglas, Isle of Man, IM1 3LP, Isle of Man"}])

    #     # Then
    #     self.coordinate_checker(l, correctGeoCoordinate)

    # def test_mapquest_get_member_location_whales_town(self):
    #     # Given
    #     g = MapquestGeocoder(None, None)
    #     correctAddress = [{"lat": 51.61578, "lng": -3.415012}]

    #     # When
    #     l = g.get_member_location([{"street": "26 Grawen Street, Porth, Rhondda Cynon Taff, CF39 0BU, United Kingdom"}])

    #     # Then
    #     self.coordinate_checker(l, correctAddress)

class test_filter_address(TestCase):

    def test_should_find_post_code(self):
        # Given
        address = "Granby House Dental Practice, 25 Granby Street, Loughborough, Leicestershire, LE11 3DU, United Kingdom"
        expected_format = {
            "postalCode": "LE11 3DU",
            "country": "United Kingdom"
        }
        
        # When
        
        # Then



class test_intergration_tests(TestCase):

    def setupClass():
        # Create mock mongo db to hold members
        pass

    def get_locations():
        pass