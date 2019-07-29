from django.shortcuts import render
from . import utils
import json

def graph(request):
	# data = json.load(open("/Users/Xing/Documents/vpo/viz/data/graph_data.json", 'r'))

	graph_data = json.load(open("/Users/Xing/Documents/vpo/viz/data/graph_data_euclidean.txt", 'r'))

	texts_data = json.load(open("/Users/Xing/Documents/vpo/viz/data/texts_data.txt", 'r'))

	filter_texts_data = []

	for line in texts_data:

		if len(line) == 0: continue

		no_tag = True

		for each in line:

			if each['tag'] != 'O':

				no_tag = False

		if no_tag == False:

			filter_texts_data.append(line) 

	context = {"graph_data": json.dumps(graph_data), "texts_data": json.dumps(filter_texts_data)}

	return render(request, "viz/graph.html", context)

def text(request):
	return render(request, "viz/text.html")
