from django.shortcuts import render
from . import utils
import json

def graph(request):
	# data = json.load(open("/Users/Xing/Documents/vpo/viz/data/graph_data.json", 'r'))

	data = json.load(open("/Users/Xing/Documents/vpo/viz/data/graph_data_euclidean.txt", 'r'))

	context = {"graph_data": json.dumps(data)}

	return render(request, "viz/graph.html", context)

def text(request):
	return render(request, "viz/text.html")
