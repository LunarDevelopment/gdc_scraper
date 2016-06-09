from unittest import TestCase
from gmaps_geolocate import GmapsGeocoder


# class test_GmapsGeocoder(TestCase):

# 	def setUpClass():
# 		self.g = GmapsGeocoder(None, None)

def test_GmapsGeocder_get_member_location():
	g = GmapsGeocoder(None, None)

	l = g.get_member_location("27 Mountbel Road, ha7 2ag")
	print(l)
	assertNotEquals(len(l), 0)