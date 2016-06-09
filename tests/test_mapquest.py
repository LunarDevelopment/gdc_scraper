from unittest import TestCase
from mapquest import geolocate


class test_mapquest(TestCase):
    def mapquest_should_be_able_to_get_more_than_one_address_coordinates(self):
        # Given
        addresses = ["27 Mountbel Road, Stanmore, UK", "22 Market Rd, London N7 9GT, UK"]
        expectedCoords = {}

        # When
        r = geolocate(addresses)

        # Then
        print(r)
        # Two address coordinates should be returned
        assert(False)
        self.assertEqual(len(r), 2)
