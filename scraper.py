from bs4 import BeautifulSoup
from gdc_request import gdc_request
import re
import os



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

	if first_name == "" and last_name == "":
		return response(False, "First name non existant")

	if first_name == last_name:	
		print("firstname and last name the same for: {}".format(first_name))

		names = first_name.split(" ")
		if len(names) > 1:
			first_name, last_name = names[0], names[1]
		else:
			first_name, last_name = names[0], ""
			print("Set first name: {} and last name: {}".format(first_name, last_name))

	# Remove all the Dr. (just in case)
	first_name = re.sub(r"dr\.", "", first_name, flags=re.IGNORECASE).strip()

	r = gdc_request(first_name, last_name)

	if r is not None:
		# names = {"firstname": first_name, "surname": last_name}
		try:
			return extract(r.text)
		except AttributeError:
			print("ATTRIBUTE ERROR! with names {} {}".format(row[0], row[1]))
			with open("error_html/names_{}_{}".format(row[0], row[1]), "w") as file:
				file.write(r.text)

	return response(False, "Was not able to get Data from Websites")


def multiple_regs(reg_array):
	"""
	Goes through reg_array and makes multiple requests from reg_array
	returns array of extracted information
	"""
	return_array = []
	for reg in reg_array:
		r = gdc_request(reg=reg)
		if r is not None:
			try:
				return_array.append(extract(r.text))
			except AttributeError:
				print("ATTRIBUTE ERROR! with registration {}".format(reg))
				with open("error_html/reg_{}".format(reg), "w") as file:
					file.write(r.text)


	return return_array

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
		return response(False, message="Multiple responses found", data=get_multiple_pages(soup), error_code=1)

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

def get_names(soup_text):
	names = re.search(r'class="searchDetailFirstName">(?P<firstname>[\w,\s,\-,\',\(,\),\.]*)<.*"searchDetailSurnameName">(?P<surname>[\w, \s,\-,\',\(,\),\.]*)<', soup_text).groupdict()
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
	return [i for i in re.findall(r">(\d{2,})<", str(soup))]
	
	# return [v for v in re.findall(r">(\d*)</td>", soup.text)]




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
	print_output("multiple_found_problem.html")

	for file in os.listdir("error_html"):
		print_output("error_html/{}".format(file))
	# print("working on method: get_multiple_pages")
	# with open("multiple_found.html") as file:
	# 	soup = BeautifulSoup(file, "html.parser")
	# 	print(get_multiple_pages(soup))

