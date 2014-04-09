import re
import json

workers = {}
def symb(workerid):
	if workerid in workers:
		return workers[workerid]
	else:
		id_number = str(len(workers))
		workers[workerid] = id_number
		return id_number

def cutquotes(x, i):
	return x[i:-i]
def cutone(x):
	return cutquotes(x, 1)

f = open("whybot-4-1-mturk.results")
line_number = 0
data = [["subject", "explanation", "seed", "level", "grammaticality", "age", "language", "comments"]]

header_labels = []
for line in f:
	elements = line[:-1].split("\t")
	if line_number == 0:
		#get header labels
		header_labels = map(cutone, elements)
	else:
		#get data
		subject_data = {}
		trial_data = {"seeds":[], "explanation":[], "level":[], "grammaticality":[]}
		for i in range(len(elements)):
			element = cutone(elements[i])
			header_label = header_labels[i]
			if header_label == "workerid":
				subject_data["subject"] = symb(element)
			elif header_label[:6] == "Answer":
				shorter_header_label = header_label[7:]
				if shorter_header_label == "dialogues":
					#get trial data
					element = re.sub("\"\"", "\"", element)
					element = json.loads(element)
					for dialogue in element:
						seed = dialogue[0]["text"]
						explanations = dialogue[1:]
						for j in range(len(explanations)):
							explanation = explanations[j]
							level = str(j)
							if "ungrammatical" in explanation.keys():
								if explanation["ungrammatical"]:
									grammaticality = "bad"
								else:
									grammaticality = "good"
							else:
								grammaticality = "unknown"
							trial_data["seeds"].append(seed)
							trial_data["explanation"].append(explanation["text"])
							trial_data["level"].append(level)
							trial_data["grammaticality"].append(grammaticality)
				else:
					if shorter_header_label == "comments":
						element = cutquotes(element, 2)
						element = re.sub("\+", " ", element)
						element = re.sub("\%2C", ",", element)
					elif shorter_header_label in ["age", "language"]:
						element = cutquotes(element, 2)
					subject_data[shorter_header_label] = element
		#subj data has the values: comments, age, language, subject
		#trial data has lists of seeds, explanations, levels, and grammaticalities
		for k in range(len(trial_data["seeds"])):
			seed = trial_data["seeds"][k]
			explanation = trial_data["explanation"][k]
			level = trial_data["level"][k]
			grammaticality = trial_data["grammaticality"][k]
			subject = subject_data["subject"]
			comments = subject_data["comments"]
			age = subject_data["age"]
			language = subject_data["language"]
			data.append([subject, explanation, seed, level, grammaticality, age, language, comments])
	line_number = line_number + 1
w = open("whybot.results", "w")
#w.write(data)
def printyprint(x):
	return "\t".join(x)
w.write("\n".join(map(printyprint, data)))
w.close()