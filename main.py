from gdc_request import gdc_request
from scraper import gather_information
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

	with open("22nd feb.csv", "r") as in_file:
		with open("output.csv", "w") as out_file:
			data = csv.reader(in_file)
			

			writer = csv.DictWriter(out_file, FIELDNAMES)
			writer.writeheader()

			for index, row in enumerate(data):
				print("{}/{}".format(index, N_ROWS))
				scraped_data = gather_information(row)
				if scraped_data["success"]:
					data = scraped_data["data"]
					try:
						writer.writerow(data)
					except ValueError as e:
						wrong_headers = re.findall("'([\w, \s]*)'",e.args[0])
						for header in wrong_headers:
							del data[header]
						writer.writerow(data)
				else:
					print(scraped_data["message"])
					






if __name__ == '__main__':
	if len(sys.argv) < 2:
		main()
	else:
		# with open("output.csv", "w") as out_file:
		# 	writer = csv.DictWriter(out_file, FIELDNAMES)
		r = ["Jamie", "Kerr"]
		values = {"firstname": r[0], "surname": r[1]}
		r = gdc_request(r[0], r[1])
		e = extract(r.text)
		if e is not None:
			try:
				values.update(e["return_dict"])
				print(values)
				writer.writerow(values)
			except ValueError as e:
				print(e.args[0])
				strings = re.findall("'([\w, \s]*)'", e.args[0])
				print(strings)
				for i in strings:
					values.pop(i)
				print(values)

