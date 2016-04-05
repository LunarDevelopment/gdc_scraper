from gdc_request import gdc_request
from scraper import gather_information, multiple_regs
from pymongo import MongoClient
import re
import csv
import sys

FIELDNAMES = [
	'Qualifications', 
	'address', 
	'Registration Number',
	'First Registered on' , 
	'Status',
	'Registrant Type', 
	'Current period of Registration from',
	'firstname',
	'surname',
	"Specialty",
]

N_ROWS = 24225

def main():
	col = MongoClient()["tubules"]["members"]

	with open("22nd feb.csv", "r") as in_file:
		data = csv.reader(in_file)

		for index, row in enumerate(data):
			print("{}/{}".format(index, N_ROWS))
			scraped_data = gather_information(row)
			if scraped_data["success"]:
				r = col.insert_one(scraped_data["data"])
				print(r.inserted_id)

			elif scraped_data["error_code"] == 1:
				print(scraped_data["message"])
				print(scraped_data["data"])
				in_db = [reg["Registration Number"] for reg in col.find({"Registration Number": {"$in": scraped_data["data"]}}, {"Registration Number": 1})]
				print(in_db)
				if len(in_db) < len(scraped_data["data"]):
					responses = multiple_regs([regs for regs in scraped_data["data"] if regs not in in_db])
					try:
						r = col.insert_many([response["data"] for response in responses if response["success"]])
						print(r.inserted_ids)
					except Exception as e:
						print(e.args)
				else:
					print("None saved to Database")
			else:
				print(scraped_data["message"])		
					






if __name__ == '__main__':
	if len(sys.argv) < 2:
		main()
		
