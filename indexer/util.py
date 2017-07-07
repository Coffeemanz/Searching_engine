import requests
from bs4 import BeautifulSoup
import re


def download_page_by_url(url):
	headers = {'User-Agent': 'SearchingEngine bot version 0.1'}
	r = requests.get(url, headers = headers)
	if r.status_code != 200:
		raise Exception("TOO FAST!!!!!")
	return r.text

#rename
def get_text_from_html(html):
	#re.sub('[,]', '', html)
	#return re.sub('<[^<]+?>', ' ', html)
	soup = BeautifulSoup(html,"html.parser")

	# kill all script and style elements
	for script in soup(["script", "style"]):
		script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text