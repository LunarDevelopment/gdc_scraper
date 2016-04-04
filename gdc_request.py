import requests


def gdc_request(f_name=None, s_name=None, reg=None):
	pay_load = {
		"RegNumber": reg,
		"Surname": s_name,
		"Forenames": f_name,
		"isSoundexFN": 0,
		"isSoundexSN": 0,
		"Town": "",
		"Postcode": "",
		"isDentist": 0,
		"isDCP": 0,
		"isTemporaryRegistrantDentist": 0,
		"isVisitingDCP": 0,
		"isVisitingDentist": 0,
		"isSpecialist": 0,
		"Speciality": "",
		"DCPTitle": "",
		"IER": 0,
		"isAllRegisters": 1
	}
	return requests.get("http://www.gdc-uk.org/Pages/GDCSearchResults.aspx", params=pay_load)




if __name__ == '__main__':
	response = gdc_request("Amy", "Gwynne")
	print(response.url)
	with open("correct.html", 'w') as f:
			f.write(response.text)

	response = gdc_request("test", "test")
	with open("none_found.html", 'w') as f:
			f.write(response.text)

	response = gdc_request("Dhru", "Shah")
	with open("multiple_found.html", 'w') as f:
			f.write(response.text)