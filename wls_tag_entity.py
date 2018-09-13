from bs4 import BeautifulSoup
import requests
import re
import json

def write_json_to_disk(filename, json_data):
	"""
	When called, write the json_data to a json file.
	"""
	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile)

def scrape_wls_tag():
	"""
	A function to scrape wls_tag.
	Outputs to JSON.
	"""
	scraped_page = requests.get("https://whaleshares.io/tags")
	if scraped_page.status_code == 200:
		soup = BeautifulSoup(scraped_page.text, 'html.parser')
		target_script_tag = str(soup.find('script', attrs={'type': 'application/json'}))
		target_script_tag = target_script_tag.replace('<script data-iso-key="_0" type="application/json">', "")
		target_script_tag = target_script_tag.replace('</script>', "")
		target_script_tag_json = json.loads(target_script_tag)

		tags_json_contents = target_script_tag_json["global"]["tags"] # Many tags!

		accepted_tags = []
		for k,v in tags_json_contents.items():
			if k == "": # We don't want this
				continue

			if (v["top_posts"] < 3): # We need at least 3 posts to show the user
				continue

			synonym_list = []
			synonym_list.append(k)

			if "-" in k:
				k_space = k.replace("-", " ")
				k_dot = k.replace("-", ".")
				k_underscore = k.replace("-", "_")
				synonym_list.append(k_space)
				synonym_list.append(k_dot)
				synonym_list.append(k_underscore)

			accepted_tags.append({"value": k, "synonyms": synonym_list})

		print(accepted_tags)
		write_json_to_disk('wls_tags.json', accepted_tags) # Storing to disk
	else:
		print("FAILURE!")

scrape_wls_tag()
