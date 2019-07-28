# utility functions

# generate data for graph
def gen_graph_data(
	cornell_format_file, 
	embeddings_file,
	word_embeddings_map_file,
	vocab_size, 
	distance_threshod):

	from collections import Counter
	import numpy as np
	import json
	from nltk.stem import PorterStemmer

	cnt = Counter()

	tags = {}

	with open(cornell_format_file, 'r') as f:

		for line in f:

			data = line.strip().split()

			if not data or len(data) == 0:

				continue

			token, tag = data

			if tag != 'O':

				cnt[token] += 1
				tags[token] = tag

	# select most frequent tokens to add to the graph

	top = cnt.most_common(vocab_size)

	top = dict(top)

	# generate links

	mapping = json.load(open(word_embeddings_map_file, 'r'))
	embeddings = np.loadtxt(embeddings_file)

	unknown_embedding = np.mean(embeddings, axis = 0)

	ps = PorterStemmer()

	links = []

	seen = set()

	for token_i in top.keys():

		for token_j in top.keys():

			stem_i = ps.stem(token_i)
			stem_j = ps.stem(token_j)

			# prevent duplicate pairs
			if (stem_i, stem_j) in seen or (stem_j, stem_i) in seen:

				continue

			seen.add((stem_i, stem_j))

			# if same, pass
			if stem_i == stem_j:

				continue

			if stem_i in mapping:
				row = mapping[stem_i]
				embedding1 = embeddings[row]

			else:
				embedding1 = unknown_embedding

			if stem_j in mapping:
				row = mapping[stem_j]
				embedding2 = embeddings[row]

			else:
				embedding2 = unknown_embedding

			
			# normalize embeddings
			embed1_normal = np.linalg.norm(embedding1)
			embed2_normal = np.linalg.norm(embedding2)

			# euclidean distance
			distance = np.linalg.norm(embed1_normal - embed2_normal)
			print(distance)
			if distance > 0 and distance <= distance_threshod:

				links.append({"source": token_i, "target": token_j, "distance": 1 - distance})
			"""

			embed1_normal = np.linalg.norm(embedding1)
			embed2_normal = np.linalg.norm(embedding2)

			distance = embedding1.dot(embedding2)
			distance /= (embed1_normal * embed2_normal)

			print(distance)
			if distance >= distance_threshod and distance < 1:

				links.append({"source": token_i, "target": token_j, "distance": distance})

			"""


	# create node list
	nodes = []
	for token in top.keys():

		node = {"token": token, "frequency": top[token], "tag": tags[token]}

		nodes.append(node)

	return nodes, links

# generate data for texts view
def generate_text_data(cornell_format_file):

	texts = []

	with open(cornell_format_file, 'r') as f:

		text = []

		for line in f:

			data = line.strip().split()

			if not data or len(data) == 0:

				texts.append(list(text))

				text = []

			else:

				token, tag = data

				text.append({"token": token, "tag": tag})

	return texts










