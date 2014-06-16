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

####first pass: resolve pronouns
# f = open("/home/feste/CoCoLab/why?/src/bots/js/whybot.results")
# w = open("/home/feste/CoCoLab/why?/src/bots/js/whybot-with-pron-res.results", "w")
# f = open("whybot.results")
# w = open("whybot-pron-res-june16.results", "w")
f = open(readfile)
w = open(writefile, "w")
line_num = 0
previous_answer = ""
for line in f:
	print line_num
	elems = line[:-1].split("\t")
	if line_num == 0:
		w.write(line[:-1] + "\tsent_with_corefs\n")
	#elif line_num > 92:
	else:
		answer = elems[1]
		answer = re.sub("\.", "", answer)
		seed = elems[2]
		level = elems[3]
		if level == "0":
			discourse = seed
			question = seed
		else:
			question = previous_answer
			discourse = discourse + ". " + previous_answer
		result = nlp.parse(discourse + " because " + answer)
		#print discourse + " because " + answer
		if "coref" in result.keys():
			corefs = result["coref"]
			print corefs
			num_pos = 0
			#print "num_pos = 0"
			for coref_set in corefs:
				for coref in coref_set:
					possible_pronoun_coref = coref[0]
					possible_pronoun = possible_pronoun_coref[0]
					antecedent_coref = coref[1]
					antecedent = antecedent_coref[0]
					if antecedent != possible_pronoun and is_pronoun(possible_pronoun) and (not is_pronoun(antecedent)):
						num_for_question = sent_length(question) + 1
						antecedent_index = antecedent_coref[3]
						antecedent_sentence = antecedent_coref[1]
						if antecedent_sentence < int(level) or num_for_question > antecedent_index:
							#question ends after antecedent index
							#(or antecedent is from an earlier sentence)
							pronoun_index_in_full_sentence = possible_pronoun_coref[3]
							if num_for_question <= pronoun_index_in_full_sentence and possible_pronoun_coref[1] == int(level):
								#only replace stuff in answer
								if antecedent_sentence < int(level) or antecedent_index < pronoun_index_in_full_sentence:
									#and only if antecedent is actually before
									pronoun_index_in_answer = pronoun_index_in_full_sentence - num_for_question + num_pos
									# print question + " because " + answer
									# print antecedent
									#print coref
									# print possible_pronoun
									#print pronoun_index_in_full_sentence
									# print pronoun_index_in_answer
									#print antecedent_index
									if is_possessive(possible_pronoun, possible_pronoun_coref, result["sentences"]):
										answer = sent_replace(answer, pronoun_index_in_answer, clean(antecedent) + "'s")
										num_pos += (sent_length(clean(antecedent)) + 1) - sent_length(possible_pronoun)
									else:
										answer = sent_replace(answer, pronoun_index_in_answer, clean(antecedent))
										num_pos += sent_length(clean(antecedent)) - sent_length(possible_pronoun)
									#print answer
		print answer
		w.write(re.sub(" s ", "'s ", re.sub("sn t", "sn't", re.sub("dn t", "dn't", line[:-1] + "\t" + answer + "\n"))))
		#print answer
		previous_answer = answer
	# else:
	# 	w.write(line)
	line_num += 1
w.close()
f.close()