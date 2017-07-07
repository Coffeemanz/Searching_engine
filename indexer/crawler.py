import requests
from bs4 import BeautifulSoup
import os
import time
from base64 import b16encode
import argparse
from util import *
import Queue
import threading
import robotparser
from urlparse import urlparse
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.insert(0, '/home/sergey/lab3/web')
from searching_engine.models import *
import reppy
from reppy.cache import RobotsCache



class Crawler(object):
	def __init__(self, start_url):
		self.start_url = start_url			
		self.sites_num = 0

	def download_pages_in_queue(self, queue):		
		current_page_url = queue.get()
		
		robot = RobotsCache()
		if (robot.allowed(current_page_url, "*")):

			print current_page_url
			if len(current_page_url) < 10: return	
			current_page_html = download_page_by_url(current_page_url)			
			bs = BeautifulSoup(current_page_html, "html.parser")

			links = bs.find_all('a', href=True)
			post_links = [link['href'] for link in links]
			
			for post_link in post_links:
				if len(post_link) < 10: continue
				if str(post_link).find('http') != 0:
					post_link = str(self.start_url) + str(post_link)
				queue.put(post_link)
			self.sites_num = self.sites_num + 1		

			page = Pages(url = current_page_url, parsed_text = get_text_from_html(current_page_html), is_indexed = False)
			page.save()
		else:
			print "Page can't be indexed because of the rules in ROBOTS.TXT"	

	def crawl(self):		
		current_page_url = self.start_url
		queue = Queue.Queue()
		queue.put(current_page_url)
		#threads = []
		while queue:
			if self.sites_num < 8:	            
				self.download_pages_in_queue(queue)
			else: return
		

def Crawl(url):
	if url == None: return 
	start_url = url	
	crawler = Crawler(start_url)	
	crawler.crawl()
	

if __name__ == "__main__":
	Crawl("http://4pda.ru")