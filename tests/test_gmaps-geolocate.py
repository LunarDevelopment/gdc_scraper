from unittest import TestCase
# from unittest import Mock
from gmaps_geolocate import GmapsGeocoder


# class test_GmapsGeocoder(TestCase):

#   def setUpClass():
#       self.g = GmapsGeocoder(None, None)

class test_gmaps_geolocate(TestCase):

    def coordinate_checker(self, a, b):
        """
        Helper function for checking coordinates a and b are roughly similar
        (Only required similarity is to 3 decimal place)
        """
        self.assertAlmostEqual(a["lat"], b["lat"], 3)
        self.assertAlmostEqual(a["lng"], b["lng"], 3)

    def test_GmapsGeocoder_get_member_location(self):
        g = GmapsGeocoder(None, None)

        l = g.get_member_location({"address": "27 Mountbel Road, stanmore, UK"})
        print("l = {}".format(l))
        self.assertEqual({'lng': -0.3232248, 'lat': 51.60104279999999}, l)

    def test_GmapsGeocoder_get_member_location_without_address(self):
        g = GmapsGeocoder(None, None)

        l = g.get_member_location({"noAddress": "address"})
        print("l = {}".format(l))
        self.assertFalse(l)

    # def test_GmapsGeocoder_get_member_location_unclear_address(self):
    #     # TODO decide on specs for this?
    #     g = GmapsGeocoder(None, None)

    #     l = g.get_member_location({"address": "Somewhere In scotland"})
    #     print("l = {}".format(l))
    #     assert(False)

    def test_GmapsGeocoder_get_member_location_isle_of_man(self):
        g = GmapsGeocoder(None, None)
        correctAddress = {"lat": 54.1562134, "lng": -4.4822503}
        l = g.get_member_location({"address": "47 Derby Square, Douglas, Isle of Man, IM1 3LP, Isle of Man"})
        print("l = {}".format(l))
        self.assertEqual(l, correctAddress)

    def test_GmapsGeocoder_get_member_location_whales_town(self):
        g = GmapsGeocoder(None, None)
        correctAddress = {"lat": 51.61578, "lng": -3.415012}
        l = g.get_member_location({"address": "26 Grawen Street, Porth, Rhondda Cynon Taff, CF39 0BU, United Kingdom"})
        print("l = {}".format(l))
        self.coordinate_checker(l, correctAddress)


    # def test_GmapsGeocoder_should_not_push_when_no_data_passed_false(self):
    #     q = Queue()
    #     rq = Queue()
    #     q.push({"test": "value"})
    #     g = GmapsGeocoder(q, rq, None)
    #     g.get_member_location = Mock(return_value=False)



if __name__ == "__main__":
    unittest.main()
