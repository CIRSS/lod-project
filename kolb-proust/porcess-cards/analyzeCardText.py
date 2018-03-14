import os, nltk, csv, re
from lxml import etree
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.metrics.association import QuadgramAssocMeasures
from nltk.tag import StanfordNERTagger

if os.name == 'nt':
	SLASH = '\\'
else:
	SLASH = '/'

def isntNumber(target):
	if type(target) is str:
		target = unicode(target)
	translation_table = dict.fromkeys(map(ord,u'-:,p./='),None)
	target = target.translate(translation_table)

	try:
		float(target)
		if float(target) < 1000 or float(target) > 2100:
			return False
		else:
			return True
	except ValueError:
		return True

def getTextFromCard(filename,ignore_words,master_word_list):
	with open(filename,'rb') as infile:
		card = infile.read()

	word_count = 0
	all_text = []
	names = {}

	root = etree.fromstring(card)
	div2 = root.xpath('//div2/*[not(self::bibl)]')
	for section in div2:
		text = section.xpath('normalize-space(.)')
		sentences = nltk.sent_tokenize(text)
		for sentence in sentences:
			if sentence[0].isupper():
				sentence = sentence[0].lower() + sentence[1:]

			stanford_classifier = '/Users/deren/StanfordNLP/stanford-ner-2017-06-09/classifiers/english.all.3class.distsim.crf.ser.gz'
			stanford_ner_path = '/Users/deren/StanfordNLP/stanford-ner-2017-06-09/stanford-ner.jar'
			tagger = StanfordNERTagger(stanford_classifier,stanford_ner_path,encoding='utf-8')

			tokens = nltk.word_tokenize(sentence)
			word_count += len(tokens)

#			Very slow code. Comment out this block to run faster			
#			tagged_tokens = tagger.tag(tokens)
#			for tagged in tagged_tokens:
#				if tagged[1] != u'O':
#					if tagged[0] not in names:
#						names[tagged[0]] = 1
#					else:
#						names[tagged[0]] += 1

			for token in tokens:
				if token.lower() not in ignore_words and token not in names and isntNumber(token):
					all_text.append(token)
					if token in master_word_list:
						master_word_list[token] += 1
					else:
						master_word_list[token] = 1

	return all_text, word_count, names

def getNgrams(n,all_text):
	word_fd = nltk.FreqDist(all_text)

	if n == 2:
		ngram_measures = nltk.collocations.BigramAssocMeasures()
		ngram_fd = nltk.FreqDist(nltk.bigrams(all_text))
		finder = BigramCollocationFinder(word_fd,ngram_fd)
	elif n == 3:
		ngram_measures = nltk.collocations.TrigramAssocMeasures()
		finder = TrigramCollocationFinder.from_words(all_text)
	elif n == 4:
		ngram_measures = QuadgramAssocMeasures()
		finder = QuadgramCollocationFinder.from_words(all_text)

	scored = finder.score_ngrams(ngram_measures.raw_freq)
	s = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
	ngrams = []

	for instance in s:
		if n == 2:
			ngrams.append([unicode(instance[0][0]).encode('utf-8') + ' ' + unicode(instance[0][1]).encode('utf-8'),instance[1]])
		elif n == 3:
			ngrams.append([unicode(instance[0][0]).encode('utf-8') + ' ' + unicode(instance[0][1]).encode('utf-8') + ' ' + unicode(instance[0][2]).encode('utf-8'),instance[1]])
		elif n == 4:
			ngrams.append([unicode(instance[0][0]).encode('utf-8') + ' ' + unicode(instance[0][1]).encode('utf-8') + ' ' + unicode(instance[0][2]).encode('utf-8') + ' ' + unicode(instance[0][3]).encode('utf-8'),instance[1]])

	return ngrams

def getCapitals(master_word_list):
	capital_word_list = {}

	for key in master_word_list:
		print key
		if key != key.lower():
			capital_word_list[key] = master_word_list[key]

	print capital_word_list

	return capital_word_list

#Source: http://wortschatz.uni-leipzig.de/en/download, specifically the French Mixed source covering 1 million setences
def getLeipzigDataset():
	dataset = { 'count_total': 0, 'index': {} }
	with open('fra_mixed_2009_1M/fra_mixed_2009_1M-words.txt','r') as readfile:
		reader = csv.reader(readfile,delimiter='\t',quoting=csv.QUOTE_NONE)

		for row in reader:
			dataset['count_total'] += int(row[2])
			dataset['index'][row[1]] = int(row[2])

	return dataset

def determineRarity(master_word_list,total_length,french_dataset):
	word_frequency_ratio = {}

	for word in master_word_list:
		if word in french_dataset['index']:
			kp_ratio = float(master_word_list[word])/float(total_length)
			french_ratio = float(french_dataset['index'][word])/float(french_dataset['count_total'])
			word_frequency_ratio[word] = word,kp_ratio/french_ratio

	return word_frequency_ratio

def outputResults(data,filename,wfr=None):
	if not os.path.exists('./nlp_output'):
		os.makedirs('nlp_output')

	with open('nlp_output/' + filename,'w') as outfile:
		writer = csv.writer(outfile)

		if type(data) is list:
			for row in data:
				writer.writerow(row)
		else:
			if wfr:
				writer.writerow(['WORD','COUNT','KP_FREQUENCY:FRENCH_FREQUENCY'])

			for key in sorted(data.iteritems(), key=lambda (k,v): (v,k)):
				if wfr and key[0] in wfr:
					writer.writerow([unicode(key[0]).encode('utf-8'),unicode(key[1]).encode('utf-8'),wfr[key[0]][1]])
				else:
					writer.writerow([unicode(key[0]).encode('utf-8'),unicode(key[1]).encode('utf-8')])

def traverseFullTree():
	rootdir = 'tei'
	ignore_words = stopwords.words('french')
	ignore_words += [',','.','p.','[',']','``',"''",':','n.',';','...','(',')','?','!',"'",'"','les','-','--','}','{','pp','/','..']
	master_word_list = {}
	names = {}

	total_length = 0
	all_text = []

	for root, dirs, files in os.walk(rootdir):
		for name in files:
			if '.xml' in name:
				if 'dc' not in name:
					print root+SLASH+name
					new_text, added_length, new_names = getTextFromCard(root+SLASH+name,ignore_words,master_word_list)
					all_text += new_text
					total_length += added_length
					for n in new_names:
						if n not in names:
							names[n] = new_names[n]
						else:
							names[n] += new_names[n]

	french_dataset = getLeipzigDataset()
	word_frequency_ratio = determineRarity(master_word_list,total_length,french_dataset)

	outputResults(master_word_list,'1-grams.csv',word_frequency_ratio)
	bigrams = getNgrams(2,all_text)
	outputResults(bigrams,'2-grams.csv')
	trigrams = getNgrams(3,all_text)
	outputResults(trigrams,'3-grams.csv')
	quadgrams = getNgrams(4,all_text)
	outputResults(quadgrams,'4-grams.csv')
	outputResults(getCapitals(master_word_list),'name_counts.csv')
#	outputResults(names,'named_entity_counts.csv')

#On Windows, the Command Prompt doesn't know how to display unicode characters, causing it to halt when it encounters non-ASCII characters
def setupByOS():
	if os.name == 'nt':
		if sys.stdout.encoding != 'cp850':
		  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'replace')
		if sys.stderr.encoding != 'cp850':
		  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'replace')

def main():
	setupByOS()
	traverseFullTree()

main()