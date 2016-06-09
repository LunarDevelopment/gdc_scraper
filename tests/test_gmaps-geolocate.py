from unittest import TestCase
# from unittest import Mock
from gmaps_geolocate import GmapsGeocoder
from queue import Queue


# class test_GmapsGeocoder(TestCase):

#   def setUpClass():
#       self.g = GmapsGeocoder(None, None)

class test_gmaps_geolocate(TestCase):

    def test_GmapsGeocoder_get_member_location(self):
        g = GmapsGeocoder(None, None)

        l = g.get_member_location({"address": "27 Mountbel Road, ha7 2ag"})
        print("l = {}".format(l))
        self.assertEqual({'lng': -0.3232248, 'lat': 51.60104279999999}, l)

    def test_GmapsGeocoder_get_member_location(self):
        g = GmapsGeocoder(None, None)

        l = g.get_member_location({"noAddress": "address"})
        print("l = {}".format(l))
        # self.assertEqual({'lng': -0.3232248, 'lat': 51.60104279999999}, l)

    def test_GmapsGeocoder_get_member_location(self):
        g = GmapsGeocoder(None, None)

        l = g.get_member_location({"address": "Somewhere In scotland"})
        print("l = {}".format(l))

    # def test_GmapsGeocoder_should_not_push_when_no_data_passed_false(self):
    #     q = Queue()
    #     rq = Queue()
    #     q.push({"test": "value"})
    #     g = GmapsGeocoder(q, rq, None)
    #     g.get_member_location = Mock(return_value=False)
