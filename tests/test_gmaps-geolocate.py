from unittest import TestCase
# from unittest import Mock
from gmaps_geolocate import GmapsGeocoder
from mongomock import Mock
from queue import Queue


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

        l = g.get_member_location(
            {"address": "27 Mountbel Road, stanmore, UK"})
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
        l = g.get_member_location(
            {"address": "47 Derby Square, Douglas, Isle of Man, IM1 3LP, Isle of Man"})
        print("l = {}".format(l))
        self.assertEqual(l, correctAddress)

    def test_GmapsGeocoder_get_member_location_whales_town(self):
        g = GmapsGeocoder(None, None)
        correctAddress = {"lat": 51.61578, "lng": -3.415012}
        l = g.get_member_location(
            {"address": "26 Grawen Street, Porth, Rhondda Cynon Taff, CF39 0BU, United Kingdom"})
        print("l = {}".format(l))
        self.coordinate_checker(l, correctAddress)

    # def test_GmapsGeocoder_should_not_push_when_no_data_passed_false(self):
    #     q = Queue()
    #     rq = Queue()
    #     q.push({"test": "value"})
    #     g = GmapsGeocoder(q, rq, None)
    #     g.get_member_location = Mock(return_value=False)

    def test_GmapsGecoder_intergration_test(self):
        member_list = [
            {"Qualifications": "Qual- BSc Honours in Dental Technology Cardiff 2014", "Registrant Type": "Dental Care Professional", "Registration Number": 252911, "Status": "Registered",
                "address": "14 Royal Parade Mews, Cheltenham, Gloucestershire, GL50 1SZ, United Kingdom", "firstname": "Sameera ", "location": {"lat": 51.8963537, "lng": -2.0822569}, "surname": "Patel", "tubuleMember": True},
            {"Qualifications": "Dip Orth Therapy RCPS Eng 2010", "Registrant Type": "Dental Care Professional", "Registration Number": 110107, "Status": "Registered",
                "address": "Lakeside Specialist Orthodontics Practice, 38 Salisbury Ave, Wirral, Merseyside, CH48 0QP, United Kingdom", "firstname": "Lucy ", "location": {"lat": 53.37120849999999, "lng": -3.1873406}, "surname": "Evans", "tubuleMember": True},
            {"Qualifications": "Diploma in Dental Nursing Level 3 QCF City & Guilds 2015", "Registrant Type": "Dental Care Professional", "Registration Number": 259592, "Status": "Registered",
                "address": "31 Lingen Close, Shrewsbury, Shropshire, SY1 2UN, United Kingdom", "firstname": "Lucy Annabelle", "location": {"lat": 52.7204636, "lng": -2.738369}, "surname": "Evans", "tubuleMember": True},
            {"Qualifications": "BDS Sheff 2009", "Registrant Type": "Dentist", "Registration Number": 177819, "Status": "Registered",
                "address": "Hockley Dental Surgery, 2 Woodlands Parade, Main Road, Hockley, Essex, SS5 4QU, UNITED KINGDOM", "firstname": "Teki ", "location": {"lat": 51.6011237, "lng": 0.6535264}, "surname": "Sowdani", "tubuleMember": True},
            {"Qualifications": "NVQ L3 Oral Health Care:Dental Nursing& Indp Asses City & Guilds 2008", "Registrant Type": "Dental Care Professional", "Registration Number": 160793, "Status": "Registered",
                "address": "195 Thunder Lane, NORWICH, Norfolk, NR7 0JF, United Kingdom", "firstname": "Gemma Claire", "location": {"lat": 52.63631609999999, "lng": 1.3430194}, "surname": "Spencer", "tubuleMember": True},
            {"Qualifications": "NVQ L3 Oral Health Care:Dental Nursing& Indp Asses City & Guilds 2007", "Registrant Type": "Dental Care Professional", "Registration Number": 141437, "Status": "Registered",
                "address": "8 Sandstone Road, Milnrow, Rochdale, Greater Manchester, OL16 3UH, United Kingdom", "firstname": "Gemma Wendy", "location": {"lat": 53.614079, "lng": -2.1128219}, "surname": "Spencer", "tubuleMember": True},
            {"Qualifications": "BDS Ncle 1995", "Registrant Type": "Dentist", "Registration Number": 70566, "Status": "Registered", "address": "Dental Surgery, 78 Kenton Lane, Newcastle upon Tyne, Tyne and Wear, NE3 4LE, United Kingdom",
                "firstname": "Annabelle Jane", "location": {"lat": 55.00312109999999, "lng": -1.63958}, "surname": "Ford", "tubuleMember": True},
            {"Qualifications": "Qual- National Certificate NEBDN 2010", "Registrant Type": "Dental Care Professional", "Registration Number": 213984, "Status": "Registered",
                "address": "Glendale Manor, Collaroy Road, Cold Ash, Thatcham, Berkshire, RG18 9PB, UNITED KINGDOM", "firstname": "Rebecca Claire", "location": {"lat": 51.4214753, "lng": -1.2631128}, "surname": "Holmes", "tubuleMember": True},
            {"Qualifications": "Diploma in Dental Nursing Level 3 QCF City & Guilds 2015", "Registrant Type": "Dental Care Professional", "Registration Number": 255870, "Status": "Registered",
                "address": "Dental Surgery, 30 Highgate Lane, Lepton, Huddersfield, West Yorkshire, HD8 0HB, United Kingdom", "firstname": "Rebecca Louise", "location": {"lat": 53.6333496, "lng": -1.7121814}, "surname": "Holmes", "tubuleMember": True}
        ]
        data_store = []
        members = Queue()
        g = GmapsGeocoder(members, data_store)

if __name__ == "__main__":
    unittest.main()
