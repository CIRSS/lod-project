import os, json, csv

if os.name == 'nt':
	SLASH = '\\'
else:
	SLASH = '/'

def getPersonIDsFromCSV():
	person_ids = []

	with open('KolbProustNameData.csv','rU') as readfile:
		headerReader = csv.reader(readfile)
		header = next(headerReader)
		name_reader = csv.DictReader(readfile,header,delimiter=',');
		for name in name_reader:
			person_ids.append(name['KeyCode'])

	return person_ids

def getPersonIDsFromCards():
	person_ids = []

	rootdir = 'tei'
	for root, dirs, files in os.walk(rootdir):
		for name in files:
			if '.json' in name:
				with open(root+SLASH+name,'r') as data_file:
					card = json.load(data_file)

				if 'mentions' in card:
					if type(card['mentions']) is list:
						for mention in card['mentions']:
							if mention['@type'] == 'Person' and mention['@id'][64:] not in person_ids:
								person_ids.append(mention['@id'][64:])

	return sorted(person_ids)

def outputSpreadsheet(rows,ids,filename):
	with open(filename,'w') as outfile:
		writer = csv.writer(outfile)
		writer.writerow([''] + [unicode(s).encode('utf-8') for s in ids])

		for subject in ids:
			writer.writerow([subject] + [('' if p == 0 else p) for p in rows[subject]])

def isFamilyMember(family_ids,id):
	reverse_index = -1
	while id[reverse_index:reverse_index+1].isdigit():
		reverse_index -= 1
	root_id = id[:reverse_index] + '0'

	if root_id in family_ids:
		return True
	else:
		return False

def getFamilyId(id):
	if id[-1:] == '0' and not id[-2:-1].isdigit():
		return id
	else:
		reverse_index = -1
		while id[reverse_index:reverse_index+1].isdigit():
			reverse_index -= 1
		root_id = id[:reverse_index] + '0'
		return root_id


def traverseFullTree():
	rootdir = 'tei'
	coocurrence_count = 0
	family_coocurrence_count = 0

#	person_ids = getPersonIDsFromCSV()
	person_ids = getPersonIDsFromCards()
	family_ids = getFamilies()

	column_numbers = {}
	for index in range(0,len(person_ids)):
		column_numbers[person_ids[index]] = index

	family_column_numbers = {}
	for index in range(0,len(family_ids)):
		family_column_numbers[family_ids[index]] = index
	
	for fn in family_column_numbers:
		print(fn,family_column_numbers[fn])

	rows = {}
	for person in person_ids:
		rows[person] = [0] * len(person_ids)

	family_rows = {}
	for family in family_ids:
		family_rows[family] = [0] * len(family_ids)

	for root, dirs, files in os.walk(rootdir):
		for name in files:
			if '.json' in name:
				with open(root+SLASH+name,'r') as data_file:
					card = json.load(data_file)

				if 'mentions' in card:
					card_families = []

					if type(card['mentions']) is list:
						for mention in card['mentions']:
							if mention['@type'] == 'Person':
								for other_mention in card['mentions']:
									if other_mention['@type'] == 'Person' and other_mention != mention:
										print(mention['@id'][64:], other_mention['@id'][64:])
										rows[mention['@id'][64:]][column_numbers[other_mention['@id'][64:]]] += 1
										coocurrence_count += 1

										if isFamilyMember(family_ids,mention['@id'][64:]) and isFamilyMember(family_ids,other_mention['@id'][64:]):
											mention0 = getFamilyId(mention['@id'][64:])
											if mention0 not in card_families:
												card_families.append(mention0)

											other_mention0 = getFamilyId(other_mention['@id'][64:])
											if other_mention0 not in card_families:
												card_families.append(other_mention0)

						for fam_index in range(0,len(card_families)):
							for fam2_index in range(fam_index+1,len(card_families)):
								print(card_families[fam_index],card_families[fam2_index])
								family_rows[card_families[fam_index]][family_column_numbers[card_families[fam2_index]]] += 1
								family_rows[card_families[fam2_index]][family_column_numbers[card_families[fam_index]]] += 1
								family_coocurrence_count += 1

							family_rows[card_families[fam_index]][family_column_numbers[card_families[fam_index]]] += 1	
					else:
						if card['mentions']['@type'] == 'Person':
							if isFamilyMember(family_ids,card['mentions']['@id'][64:]):
								mention0 = getFamilyId(card['mentions']['@id'][64:])
								family_rows[mention0][family_column_numbers[mention0]] += 1

	print(person_ids)
	print(len(person_ids))
	outputSpreadsheet(rows,person_ids,'coocurrences.csv')
	outputSpreadsheet(family_rows,family_ids,'coocurrences_family.csv')
	print(coocurrence_count/2)
	print(family_coocurrence_count)

def getFamilies():
	family_ids = []
	for root, dirs, files in os.walk('names'):
		for name in files:
			isolated_id = name[:-7]
			if isolated_id[-1:] == '0' and not isolated_id[-2:-1].isdigit():
				family_ids.append(isolated_id)

	return family_ids

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