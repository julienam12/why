import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint

class ID_Maker:
	def __init__(self):
		self.n_entity_ids = 0
	def next(self):
		ret_id = self.n_entity_ids
		self.n_entity_ids+=1
		return ret_id

class Predicate:
	def __init__(self):
		self.neg = None
		self.root = None
		self.xcomp = None
		self.subj = None
		self.dobj = None
		self.prep = None
		self.pobj = None
		self.is_pass = False
	#def full_show(self):
	def full_show(self):
		print "Predicate:"
		if self.subj:
			print "  subj:", self.subj
		if self.neg:
			print "  neg:", self.neg
		if self.root:
			print "  root:", self.root
		if self.xcomp:
			print "  xcomp:", self.xcomp
		if self.dobj:
			print "  dobj:", self.dobj
		if self.prep:
			print "  prep:", self.prep
		if self.pobj:
			print "  pobj:", self.pobj
	#def caveman(self):
	def show(self):
		if self.subj:
			print self.subj,
		else:
			print "_",
		if self.neg:
			print self.neg,
		else:
			print "_",
		if self.root:
			print self.root,
		else:
			print "_",
		if self.xcomp:
			print self.xcomp,
		else:
			print "_",
		if self.dobj:
			print self.dobj,
		else:
			print "_",
		if self.prep:
			print self.prep,
		else:
			print "_",
		if self.pobj:
			print self.pobj,
		else:
			print "_",
		print
	# def show(self):
	# 	if self.root:
	# 		root = self.root
	# 	else:
	# 		root = "_"

	# 	if self.subj:
	# 		nsubj = self.subj
	# 	else:
	# 		nsubj = "_"

	# 	if self.dobj:
	# 		dobj = self.dobj
	# 	else:
	# 		dobj = "_"

	# 	if self.neg:
	# 		neg = u"\u00ac"
	# 	else:
	# 		neg = ""

	# 	print neg + root + "(" + nsubj + "," + dobj + ")"
	def pretty(self, words):
		def pretty_word(w):
			for word in words:
				if word.text == w:
					return word.lemma
			return w
		self.root = pretty_word(self.root)
		self.xcomp = pretty_word(self.xcomp)
		self.subj = pretty_word(self.subj)
		self.dobj = pretty_word(self.dobj)
		self.prep = pretty_word(self.prep)
		self.pobj = pretty_word(self.pobj)

def dependencies(words, nlp_dependencies):
	predicate = Predicate()
	#print nlp_dependencies
	for dependency in nlp_dependencies:
		if dependency[0] == "root":
			predicate.root = dependency[2]
	for dependency in nlp_dependencies:
		depType, governor, dep = dependency
		if governor == predicate.root:
			if depType == "nsubj":
				predicate.subj = dep
				#get NP that contains this nsubj?
			elif depType == "dobj":
				predicate.dobj = dep
			elif depType == "prep":
				predicate.prep = dep
			elif depType == "agent":
				predicate.subj = dep
			elif depType[0:4] == "prep":
				predicate.prep = depType[5:]
				predicate.pobj = dep
			elif depType == "xcomp":
				predicate.xcomp = dep
			elif depType == "neg":
				predicate.neg = "not"
			elif depType == "nsubjpass":
				if not predicate.subj:
					predicate.subj = "someone"
				predicate.dobj = dep
				predicate.is_pass = True
		# elif governor == predicate.prep:
		# 	if depType == "pobj":
		# 		predicate.pobj = dep
		elif governor == predicate.xcomp:
			if depType == "dobj":
				predicate.dobj = dep
			elif depType == "prep":
				predicate.prep = dep
			elif depType[0:4] == "prep":
				predicate.prep = depType[5:]
				predicate.pobj = dep
			elif depType == "neg":
				predicate.neg = "not"

	predicate.pretty(words)
	predicate.show()
	#print nlp_dependencies

def get_because_index(words):
	i = 0
	for word in words:
		if word.text == "because":
			return i
		i+=1
	return -1

class Word:
	def __init__(self, nlp_word):
		self.text = nlp_word[0]
		self.id_in_expl = None
		self.id_in_full = None
		self.entity_id = None
		self.lemma = nlp_word[1]["Lemma"]
	def show(self):
		print "Word"
		print "  word: ", self.text
		print "  id_in_expl: ", self.id_in_expl
		print "  id_in_full: ", self.id_in_full
		print "  entity_id: ", self.entity_id
		print "  lemma: ", self.lemma

def get_words(nlp_output):
	words = nlp_output["sentences"][0]["words"]
	return map(lambda x: Word(x), words)

def get_sentences(nlp_output):
	sentences = []
	for sentence in nlp_output["sentences"]:
		words = sentence["words"]
		sentences.append(map(lambda x: Word(x), words))
	return sentences

class Coref:
	def __init__(self, coref):
		# print coref
		self.text = coref[0]
		self.sentence = int(coref[1])
		self.word = int(coref[4])-1
		# print self.sentence
		# print self.word

def process(discourse):
	full = ". ".join(discourse)
	id_maker = ID_Maker()

	full_parse = nlp.parse(full)
	sentences = get_sentences(full_parse)

	if "coref" in full_parse.keys():
		corefs = full_parse["coref"]
		for entity in corefs:
			for reference_pair in entity:
				possible_pronoun_coref, antecedent_coref = reference_pair
				possible_pronoun = Coref(possible_pronoun_coref)
				antecedent = Coref(antecedent_coref)
				possible_pronoun_word = sentences[possible_pronoun.sentence][possible_pronoun.word]
				if possible_pronoun_word.lemma in ["she", "he"] or (possible_pronoun_word.lemma in ["it", 
					"they"] and possible_pronoun.word != 0):
					antecedent_word = sentences[antecedent.sentence][antecedent.word]
					# print antecedent_word.lemma
					# print possible_pronoun_word.lemma
					sentences[possible_pronoun.sentence][possible_pronoun.word].lemma = antecedent_word.lemma
		# 		#print antecedent
		# #replace pronouns in sentences with initial word

	# for sentence in sentences:
	# 	for word in sentence:
	# 		print word.show(),
	# 	print
	for i in range(len(discourse)):
		parse = nlp.parse(discourse[i])
		predicates = dependencies(sentences[i], parse["sentences"][0]["dependencies"])
		#predicates = dependencies(sentences[i], parse["sentences"][0])

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("corn18.stanford.edu", 12345)))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()

f = open("whybot2.csv")
line_num = 0
discourse = []
for line in f:
	if len(line) > 1:# and line_num < 5:
		explanation, both, explanandum = line[:-1].split(",")
		if len(discourse)>0 and explanandum == discourse[-1]:
			discourse.append(explanation)
		else:
			for sentence in discourse:
				print sentence
			process(discourse)
			print "****"
			discourse = [explanandum, explanation]
	line_num += 1

# result = nlp.parse("I like my friend Amy. She is really cool. My friend David is not so cool. He stole my bike.")
# print result["coref"]

# from nltk.tree import Tree
# tree = Tree.parse(result['sentences'][0]['parsetree'])