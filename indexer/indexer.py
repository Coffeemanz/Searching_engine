# -*- coding: utf-8 -*-
from util import *
import argparse
from base64 import b16encode, b16decode
import os
import json
import operator
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.insert(0, '/home/sergey/lab3/web')
from searching_engine.models import *



def add_document(url, parsed_text):
	for word in parsed_text:		
		if word == '':continue
		if word.find(' ') != -1:continue
		if len(word) < 2: continue

		if ord(word[0]) < 33: continue		
		d = Indexes(word = word, url = url)
		print word
		d.save()

def indexing():		
	for i in Pages.objects.values_list('url', 'parsed_text', 'is_indexed', 'id'):
		if i[2] == False:
			text = i[1].replace('.', '').replace(',', '').replace('"', '').replace("'", ''). \
	                            replace(':', '').replace('!', '').replace('?', '').lower()			
			add_document(i[0], text.split(" "))
			Pages.objects.get(id=i[3]).delete()
			page = Pages(id = i[3], url = i[0], parsed_text = i[1], is_indexed = True)
			page.save()
		else: continue	


def Find_word(word):
	l =  Indexes.objects.filter(word=word).values_list('url')	
	d = {}
	for i in l: 
		if i not in d:
			d[i[0]] = 1 
		else: d[i] += 1			
	return sorted(d.items(), key=operator.itemgetter(1), reverse=True)


if __name__ == "__main__":
	Find_word("при")	