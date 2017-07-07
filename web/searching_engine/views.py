from django.shortcuts import render
from django.http import HttpResponse 
from django.template.loader import get_template
from django.template import Context
import sys
import multiprocessing as mp
sys.path.insert(0, '/home/sergey/lab3/indexer')
import indexer
import crawler
from urlparse import urlparse
from searching_engine.models import *

# Create your views here.
def home(request):
	query = request.POST.get('query')
	return render(request, 'home.html', {'name': query})


def req(request):
	try:
		word = indexer.Find_word(request.POST['query'])
		print word
	except:
		word = ["Results not found"]
		return render(request, 'results.html', {'name': word})

	a = []
	for d in word:
		for item in d:
			a.append(item)
	b = []
	for i in range(0,len(a),2):
		b.append(a[i])
	
	return render(request, 'results.html', {'name': b})


def indexURL(request):
	urls = []
	site = request.POST.get('query')	

	if str(site).find(' ') != -1:		
		urls.extend(str(site).split(" "))
	else: urls.append(site)
	      
	file_links = request.FILES.get('file_links')
	if file_links:
		for url in file_links:					
			urls.append(url.strip())			
		

	for url in urls:
		if len(str(url)) < 5: continue			
		str_url = str(url)
		if str_url.find('http') != 0:
			url = "http://" + str(url)
		print url					
		crawler.Crawl(url)
		print "started indexing"

		workers = []
		for i in range(4):
			worker = mp.Process(target = indexer.indexing())
			workers.append(worker)
			worker.start()

		
		for i in range(4):
			workers[i].join(None)

		indexer.indexing()
	

	return render(request, 'indexURL.html')

def knownURL(request):
	ids = []
	docs = Pages.objects.all()
	for doc in docs:
		ids.append(int(doc.id))

	if not request.method == "POST" or request.POST.get('id') == '':
		return render(request, 'knownURL.html', {'docs':docs})  

	if int(request.POST.get('id')) in ids:
		id_ = request.POST.get('id')
        Pages.objects.get(id=id_).delete()
        docs = Pages.objects.all()

	return render(request, 'knownURL.html', {"docs": docs})


def indexWords(request):
	ids = []
	pags = Indexes.objects.all()
	for index in pags:
		ids.append(int(index.id))

	if not request.method == "POST" or request.POST.get('id') == '':
		return render(request, 'indexWords.html', {'pags':pags[:300]})  

	if int(request.POST.get('id')) in ids:
		id_ = request.POST.get('id')
        Indexes.objects.get(id=id_).delete()
        pags = Indexes.objects.all()



	pags = Indexes.objects.all()
	return render(request, 'indexWords.html', {"pags": pags[:300]})