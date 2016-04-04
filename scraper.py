from bs4 import BeautifulSoup
from gdc_request import gdc_request
import re



DEBUG = False

def response(success, message=None, data=None, error_code=None):
	return {
		"success": success,
		"message": message,
		"data": data,
		"error_code": error_code
	}

def gather_information(row):
	"""
	Retrevies information from GDC database about individual.
	Returns dictionary.
	"""
	first_name, last_name = row[0].strip(), row[1].strip()

	if first_name == "":
		return response(False, "First name non existant")

	if first_name == last_name:	
		if DEBUG:
			print("firstname and last name the same for: {}".format(first_name))

		names = first_name.split(" ")
		if len(names) > 2:
			first_name, last_name = names[0], names[1]
		else:
			return response(False, "Firstnames and Lastnames are the same, but no space exists!")

	# Remove all the Dr.
	first_name = re.sub(r"dr\.", "", first_name, flags=re.IGNORECASE).strip()

	r = gdc_request(first_name, last_name)

	if r is not None:
		# names = {"firstname": first_name, "surname": last_name}
		return extract(r.text)

	return response(False, "Was not able to get Data from Websites")
			

def extract(html):
	"""
	Returns dict
	html = html file
	"""
	data = {}
	soup = BeautifulSoup(html, 'html.parser')

	if soup.find(class_="noresultfound") is not None:
		return response(False, "No Result Found")

	if soup.find("span", class_="ShowHide") is not None:
		return response(False, message="Multiple responses found", data=get_multiple_pages(soup))

	address = soup.find(id="td_address")
	if address is not None:
		data["address"] = clean_address(address)
	else:
		return response(False, "No address Found")

	# data.update(get_names(str(soup)))
	data.update(get_names(str(soup)))

	if DEBUG:
		print(data)

	data.update(extract_table(soup.find("table", id="tblSearchDetail")))
	
	return response(True, data=data)

def get_names(soup):
	names = re.search(r'class="searchDetailFirstName">(?P<firstname>[\w, \s]*)<.*"searchDetailSurnameName">(?P<surname>[\w, \s]*)<', soup).groupdict()
	if DEBUG:
		print("names = {}".format(names))
		
	return names

def extract_table(table):
	# print(table)
	data = {}
	for r in table.find_all(class_="searchDetailRow"):
			c = r.find_all("td")
			if len(c) > 1:
				data[c[0].text.strip()[:-1]] = c[1].text.strip().split("\n")[0].split(u"\xa0\xa0\xa0")[0]

	return data

def clean_address(address):
	no_spaces_list = []

	for row in address.text.strip().split("\n"):
		if not row.isspace():
			no_spaces_list.append(row.strip())
	if DEBUG:
		print(no_spaces_list)

	return str.join(", ", no_spaces_list)


def get_multiple_pages(soup):
	"""
	Returns list of tupules, with GDC number and link to their page.
	"""
	members = []
	regnumber_regex = re.compile(r"RegNumber=(\d*)&")
	rows = soup.find_all("tr", class_="searchTableRow")
	for r in rows:
		members.append({
			"link": r.a["href"],
			"reg": regnumber_regex.search(str(r)).group(1)
		})
	return members


if __name__ == "__main__":
	DEBUG = False

	def print_output(f_name):
		with open(f_name) as doc:
			print()
			print("Working on file: {}".format(f_name))
			print(extract(doc))
			print()

	print_output("output.html")
	print_output("none_found.html")
	print_output("multiple_found.html")
	print_output("Dhru.html")


	# print("working on method: get_multiple_pages")
	# with open("multiple_found.html") as file:
	# 	soup = BeautifulSoup(file, "html.parser")
	# 	print(get_multiple_pages(soup))

