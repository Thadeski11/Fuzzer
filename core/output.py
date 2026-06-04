import json
import xml.etree.ElementTree as ET
import csv

class Output():
	def __init__(self, results, file):
		self.results = results
		self.output_file = file
	

	def text_file(self):
		with open(self.output_file, "w") as o:
			if len(self.results) > 0 and "body" in self.results[0]:
				for lines in self.results:
					o.write(f"{lines['url']:<100} {lines['status_code']:>10} {lines['length']:>10} {lines['body']:>20}\n")	
			else:
				for lines in self.results:
					o.write(f"{lines['url']:<100} {lines['status_code']:>10} {lines['length']:>10}\n")

	def json_file(self):
		with open(self.output_file, "w") as o:
			o.write(json.dumps(self.results, indent=4))


	def xml_file(self):
		root = ET.Element("results")

		for item in self.results:
			result = ET.SubElement(root, "result")
			for key, value in item.items():
				element = ET.SubElement(result, key)
				element.text = str(value)

		tree = ET.ElementTree(root)
		tree.write(self.output_file, encoding="UTF-8", xml_declaration=True)


	def csv_file(self):
		if not self.results:
			return
			
		with open(self.output_file, "w") as o:
			writer = csv.DictWriter(o, fieldnames=self.results[0].keys())
			writer.writeheader()
			writer.writerows(self.results)
