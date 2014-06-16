import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
from pprint import pprint
import re
import sys

readfile = sys.argv[1]
writefile = sys.argv[2]

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()

def is_pronoun(possible_pronoun):
	return possible_pronoun in ["he", "him", "his",
	                            "she", "her", "hers",
	                            "it", "its",
		                        "they", "them", "their", "theirs",
		                        "we", "us", "our"
		                        ]

def is_possessive(pronoun, pronoun_coref, sentences):
	sentence_index = pronoun_coref[1]
	word_index = pronoun_coref[3]
	sentence = sentences[sentence_index]
	#print sentence
	words = sentence["words"]
	#print words
	word = words[word_index]
	#print word
	pos = word[1]["PartOfSpeech"]
	#print pos
	if pronoun == "her":
		#print words
		#print pronoun_index
		#print words[pronoun_index]
		#print words[pronoun_index][1]
		#print words[pronoun_index][1]["PartOfSpeech"]
		#return pos == "PRP$"
		return False
	else:
		return pronoun in ["his", "hers", "its", "their", "theirs", "our"]

def sent_length(sentence):
	no_quote_sentence = re.sub("'", " '", sentence)
	return len(no_quote_sentence.split(" "))

def sent_replace(sentence, index, replacement):
	no_quote_sentence = re.sub("'", " ", sentence)
	new_sentence = no_quote_sentence.split(" ")
	new_sentence[index] = replacement
	return " ".join(new_sentence)

def clean(word):
	w = re.sub(" 's$", "", word)
	w = re.sub("'s$", "", w)
	return w

def lemmatize(element, words):
	for word in words:
		if word[0] == element:
			return word[1]["Lemma"]
	print "error 7"

####second pass: dependency parse / lemmatization / simplification
## keep subject, negation, predicate, object (if no object, use pobj)
## next try looking for xcomp and getting subj, pred, obj
# f = open(sys.argv[1])
# w = open(sys.argv[2], "w")
f = open(readfile)
w = open(writefile, "w")
# f = open("whybot-with-pron-res-take6.results");
# w = open("whybot-cavemanese-june16.results", "w");
#f = open("/home/feste/CoCoLab/why?/src/bots/js/whybot-with-pron-res-take6.results")
#w = open("/home/feste/CoCoLab/why?/src/bots/js/whybot-cavemanese.results", "w")
line_num = 0
previous_answer = ""
for line in f:
	if len(line) > 1:
		#print line_num
		elems = line[:-1].split("\t")
		if line_num == 0:
			w.write(line[:-1] + "\tbaby_cavemanese\tcavemanese\tS\tN\tP\tO\tS'\tN'\tP'\tO'\ttense\n") #8 elements
		#elif line_num == 68:
		else:
			print elems
			explanation = elems[8]
			#print explanation
			result = nlp.parse(explanation)
			sentence = result["sentences"][0]
			dependencies = sentence["dependencies"]
			words = sentence["words"]
			tense = "future"
			p_raw = ""
			p_prime_raw = ""
			s = ""
			n = ""
			p = ""
			o = ""
			s_prime = ""
			n_prime = ""
			p_prime = ""
			o_prime = ""
			baby_cavemanese = ""
			cavemanese = ""
			has_passive_agent = False
			for dependency in dependencies:
				if dependency[0] == "root":
					p_raw = dependency[2]
					p = lemmatize(p_raw, words)
			for dependency in dependencies:
				if dependency[0][:5] == "nsubj" and dependency[1] == p_raw and (not dependency[0] == "nsubjpass"):
					s = lemmatize(dependency[2], words)
				if (dependency[0] == "dobj" or dependency[0][:4] == "prep") and dependency[1] == p_raw:
					o = lemmatize(dependency[2], words)
				if dependency[0] == "xcomp" and dependency[1] == p_raw:
					p_prime_raw = dependency[2]
					p_prime = lemmatize(p_prime_raw, words)
				if dependency[0] == "neg" and dependency[1] == p_raw:
					n = "not"
			for dependency in dependencies:
				if dependency[0] == "agent" and dependency[1] == p_raw:
					has_passive_agent = True
					s = lemmatize(dependency[2], words)
			for dependency in dependencies:
				if dependency[0] == "nsubjpass" and dependency[1] == p_raw:
					if has_passive_agent:
						o = lemmatize(dependency[2], words)
					else:
						s = lemmatize(dependency[2], words)
						p = p_raw
			if p_prime != "":
				for dependency in dependencies:
					if dependency[0][:5] == "nsubj" and dependency[1] == p_prime_raw:
						s_prime = lemmatize(dependency[2], words)
					if (dependency[0] == "dobj" or dependency[0][:4] == "prep") and dependency[1] == p_prime_raw:
						o_prime = lemmatize(dependency[2], words)
					if dependency[0] == "neg" and dependency[1] == p_prime_raw:
						n_prime = "not"
			baby_cavemanese = " ".join([x for x in [s, n, p] if x != ""])
			cavemanese = " ".join([x for x in [s, n, p, s_prime, n_prime, p_prime, o_prime, o] if x != ""])
			print cavemanese
			for word in words:
				lemma = word[1]["Lemma"]
				pos = word[1]["PartOfSpeech"]
				if lemma != "want" and lemma != "need" and lemma != "require" and lemma != "try":
					if pos == "VBD" or pos == "VBN":
						tense = "past"
					elif (pos == "VBZ" or pos == "VBP") and tense == "future":
						tense = "present"
			if re.match(".* (have|has|had) to .*", explanation):
				tense = "future"
			w.write(line[:-1] + "\t" + "\t".join([baby_cavemanese, cavemanese, s, n, p, o, s_prime, n_prime, p_prime, o_prime, tense]) + "\n")
		line_num += 1
w.close()
f.close()

# result = nlp.parse("government is controlled by business")
# pprint(result["sentences"][0]["dependencies"])