import csv, json, re, urllib.request, os, sys

class Entity(object):
	def __init__(self, fullname):
		# if there is a link
		if re.search('<(.*)>', fullname):
			name_link = re.match('(.*) (?:<(.*)>)', fullname).groups()
			fullname = name_link[0].strip()
			self.link = name_link[1].strip()
		else:
			self.link = None

		self.name = fullname

class Person(object):
	def __init__(self, fullname):
		# if there is a link
		if re.search('<(.*)>', fullname):
			name_link = re.match('(.*) (?:<(.*)>)', fullname).groups()
			fullname = name_link[0].strip()
			self.link = name_link[1].strip()
		else:
			self.link = None

		if re.search('[0-9]{4}', fullname):
			name_date = re.match('(.*), ([0-9]{4})?\??-?([0-9]{4})?', fullname).groups()
			self.name = name_date[0].strip()
			self.birthdate = name_date[1]
			self.deathdate = name_date[2]
		else:
			self.name = fullname
			self.birthdate = None
			self.deathdate = None

		self.fullname = fullname

def searchAssocPeople(row, role):
	if row[role].strip() != '':
		names = row[role].split(';')
		
		name_srch = []
		for name in names:
			person = Person(name.strip())
			name_srch.append(person.fullname + ', ' + role[role.find('(')+1:role.find(')')])
		
		return name_srch
	else:
		return []
		
def addAssociatedPeople(row, role):
	if row[role].strip() != '':
		names = row[role].split(';')
		
		name_rdfs = []
		for name in names:
			person = Person(name.strip())

			name_rdf = {}
			name_rdf['@type'] = 'Person'
			name_rdf['jobTitle'] = role[role.find('(')+1:role.find(')')]

			if person.link != None:
				name_rdf['@id'] = person.link
			else:
				name_rdf['name'] = person.name
				if person.birthdate != None:
					name_rdf['birthdate'] = person.birthdate
				if person.deathdate != None:
					name_rdf['deathdate'] = person.deathdate

			# niko modified this code to add sameAs						
			if person.fullname in peopleDict.keys():
				sameAs = [];
				lods = peopleDict[person.fullname]['lod'];
				for lod in lods:
					# check if it is dbpedia or viaf
					linkChecker = re.search('viaf.org', lod['link'])
					if '@id' not in name_rdf.keys() and linkChecker is not None:
						#print lod['link']
						name_rdf['@id'] = lod['link']
					else:
						sameAs.append(lod['link']);
				if(len(sameAs) > 0):
					name_rdf['sameAs'] = sameAs;

			name_rdfs.append(name_rdf)

		return name_rdfs
	else:
		return []
					
# Niko add
# Make Dictionary for people, performance and theater
# parse people for people dictionary
peopleDict = {}
with open('Motley_People_Links_Full.csv', 'r') as peopleFile:
	myReader = csv.reader(peopleFile);
	header = next(myReader);
	#print(header);
	peopleReader = csv.DictReader(peopleFile,header,delimiter=',');
	fetchPerson = '';
	for row in peopleReader:
		person = row['Person'];
		if(person!=''):
			fetchPerson = person;	
		role = row['Role'];
		website = row['Website'];
		link = row['Link']
		if fetchPerson not in peopleDict.keys():
			peopleDict[fetchPerson] = {};
			peopleDict[fetchPerson]['lod'] = [];
		
		if(role!=''):
			peopleDict[fetchPerson]['role'] = role;
		if(website!='' and link!=''):
			peopleDict[fetchPerson]['lod'].append({'source': website,'link': link});

	#print(json.dumps(peopleDict));

performanceDict = {}
with open('Motley_Performance_Links_Full.csv', 'r') as perfFile:
	myReader = csv.reader(perfFile);
	header = next(myReader);
	#print(header);
	perfReader = csv.DictReader(perfFile,header,delimiter=',');
	fetchPerf = '';
	for row in perfReader:
		production = row['Production'];
		if(production!=''):
			fetchPerf = production;
		year = row['Year'];
		location = row['Location'];
		source = row['Source'];
		sourceType = row['Source Type'];
		link = row['Link']
		if fetchPerf not in performanceDict.keys():
			performanceDict[fetchPerf] = {};
			performanceDict[fetchPerf]['lod'] = [];
		
		if(year!=''):
			performanceDict[fetchPerf]['year'] = year;
		if(location!=''):
			performanceDict[fetchPerf]['location'] = location;
		if(source!='' and link!=''):
			performanceDict[fetchPerf]['lod'].append({ 'source': source, 'type': sourceType, 'link': link });

	#print(json.dumps(performanceDict));

theatreDict = {}
with open('Motley_Theatre_Links_Full.csv', 'r') as theaterFile:
	myReader = csv.reader(theaterFile);
	header = next(myReader);
	#print(header);
	theaterReader = csv.DictReader(theaterFile,header,delimiter=',');
	fetchTheater = '';
	for row in theaterReader:
		theater = row['Theatre'];
		if(theater!=''):
			fetchTheater = theater;
		source = row['Source'];
		link = row['Link']
		if fetchTheater not in theatreDict.keys():
			theatreDict[fetchTheater] = {};
			theatreDict[fetchTheater]['lod'] = [];
		
		if(source!='' and link!=''):
			theatreDict[fetchTheater]['lod'].append({ 'source': source, 'link': link });

#dimensionDict = {}
#with open('imageDimentions.csv','r') as dimensionFile:
#	myReader = csv.reader(dimensionFile)
#	header = next(myReader)
#	dimensionReader = csv.DictReader(dimensionFile,header,delimiter=',')
#	for row in dimensionReader:
#		dimensionDict[row['Image URL']] = {'width': row['Width'], 'height': row['Height']}

handleDict = {}
with open('Motley_handles.csv','r') as handlesFile:
	myReader = csv.reader(handlesFile)
	header = next(myReader)
	handlesReader = csv.DictReader(handlesFile,header,delimiter=',')
	for row in handlesReader:
		handleDict[row['@id']] = row['Handle']


	#print(json.dumps(theatreDict));

# End of additional dictionary

def generateNewJSON(row,row_index,csv_length,fail_writer):
	record = {}
	searchRec = {}
	stagework = {}
#	sys.stdout.write('Processed %d out of %d records	\r' % (row_index,csv_length))
#	sys.stdout.flush()
	if row_index >= start_row:
#		stagework = {}
		# parse contentDm number from rdf file
		rdfaLink = row['RDF'].split('/');
		filename = rdfaLink[len(rdfaLink)-1];
		contentDmNumber = filename.split('.')[0];

		refURL2 = row['Reference URL'].replace(':8081/', '/');
		thumbUrl = row['CONTENTdm file name'].replace('.jp2', '.jpg')

		#with open('motley-rdfa-google/' + row['CONTENTdm number'] + '.json', 'w') as output:
		with open('motley-jsonld/' + contentDmNumber + '.json', 'w') as output:
			searchOut = open('motley-solr/' + contentDmNumber + '.json', 'w') 
			print("Remaking " + contentDmNumber + ".json")
			record['@context'] = [ 'http://schema.org/', { 's': 'http://schema.org/', 'scp': 'http://ns.library.illinois.edu/scp/', 'fileFormat': { '@id': 's:fileFormat', '@type': 's:Text' }, 'artform': { '@id': 's:artform', '@type': 's:Text' }, 'artworkSurface': { '@id': 's:artworkSurface', '@type': 's:Text' }, 'artMedium': { '@id': 's:artMedium', '@type': 's:Text' }, 'genre': { '@id': 's:genre', '@type': 's:Text' } } ]
			# this must be changed to reference url
			searchRec['rdfId'] = contentDmNumber;
			record['@id'] = refURL2;
			searchRec['splashUrl'] = refURL2;
			searchRec['thumbUrl'] = 'http://imagesearch-test1.library.illinois.edu/motley/icon/icon' + thumbUrl;
			searchRec['invNo'] = row['Inventory Number'];
			record['sameAs'] = [ 'http://imagesearch-test1.library.illinois.edu/cdm/search/collection/motley-new/searchterm/' + row['Inventory Number']]
			if record['@id'] in handleDict:
				record['sameAs'].append(handleDict[record['@id']])
			record['@type'] = 'CreativeWork'
			record['creator'] = { '@type': 'Organization', '@id': 'http://viaf.org/viaf/121005107', 'name': 'Motley (Organization)', 'sameAs': 'https://en.wikipedia.org/wiki/Motley_Theatre_Design_Group' }
			object_content = row['Object'].strip()
			if object_content != '' and object_content in ['Character sketch', 'Costume design', 'Costume rendering', 'Costume sketch', 'Costume work drawing', 'Instrument rendering', 'Mask sketch', 'Prop design', 'Props', 'Sandals sketch', 'Set design', 'Set desing', 'Set detail', 'Set rendering', 'Sketch', 'Stage props', 'Working drawing']:
				record['@type'] = 'VisualArtwork'
			record['name'] = row['Image Title'].strip()
			searchRec['search_title'] = row['Image Title'].strip()
			record['isPartOf'] = [{ '@id' : 'http://imagesearch-test1.library.illinois.edu/cdm/landingpage/collection/motley-new/',
														'@type' : 'CreativeWork', 'additionalType' : 's:Collection'}]

			#stagework['@id'] = 'http://imagesearch-test1.library.illinois.edu/cdm/landingpage/collection/motley-new/'
			stagework['@type'] = 'CreativeWork'
			stagework['additionalType'] = 'scp:StageWork'

			if row['Performance Title'].strip() != '':			
				stagework['name'] = row['Performance Title'].strip()
				# niko add sameAs attribute
				searchRec['search_performance'] = stagework['name']
				performance = stagework['name'];
				if performance in performanceDict.keys():
					stagework['sameAs'] = [];
					lods = performanceDict[performance]['lod'];
					for lod in lods:
						if '@id' not in stagework and 'wikipedia.org' in lod['link']:
							stagework['@id'] = lod['link']
						else:
							stagework['sameAs'].append(lod['link']);

			if row['Opening Performance Date'].strip() != '':
				stagework['dateCreated'] = row['Opening Performance Date'].strip()
				searchRec['facet_openYear'] = stagework['dateCreated']
				
			# ad multi theater 
			myTheaters = row['Theater'].split(';');
			myStageworks = [];
			searchRec['search_theater'] = [];
			for myTheater in myTheaters: 
				#if row['Theater'].strip() != '':
				print(myTheater)
				if myTheater.strip() != '':
					print(myTheater)
					searchRec['search_theater'].append(myTheater)
					entity = Entity(myTheater.strip())
					theater = {};

					if entity.link != None:
						#stagework['locationCreated'] = { '@id' : entity.link }
						theater = { '@id' : entity.link }
					else:
						#stagework['locationCreated'] =	entity.name 
						theater = { 'name': entity.name };

					#print(theater);
					if entity.name in theatreDict.keys():
							sameAs = [];
							lods = theatreDict[entity.name]['lod'];
							#print(lods);
							for lod in lods:
								if '@id' not in theater and 'wikipedia.org' in lod['link']:
									theater['@id'] = lod['link']
								else:
									sameAs.append(lod['link']);
							if(len(sameAs) > 0):
								theater['sameAs'] = sameAs;

					# sum it up to stagework
					myStageworks.append(theater);

			stagework['locationCreated'] = myStageworks;


			searchRec['search_author'] = [];
			if row['Author'].strip() != '':
				stagework['exampleOfWork'] = { '@type' : 'Book', 'author' : [] }
				names = row['Author'].split(';')
				for name in names:
					person = Person(name.strip())
					searchRec['search_author'].append(person.fullname)
					author = {}
					if person.link != None:				
						# niko modified this code to make element instead of string only
						# stagework['exampleOfWork']['author'].append({ '@type' : 'Person', '@id' : person.link })
						author = { '@type' : 'Person', '@id' : person.link };
					else:
						# niko modified this code to make element instead of string only
						# stagework['exampleOfWork']['author'].append(person.name)
						author = { 'name': person.name }
						# stagework['exampleOfWork']['author'].append(person.name)

					# niko modified this code to add sameAs						
					if person.fullname in peopleDict.keys():
						sameAs = [];						
						lods = peopleDict[person.fullname]['lod'];
						for lod in lods:
							# check if it is dbpedia or viaf
							linkChecker = re.search('viaf.org', lod['link'])
							if '@id' not in author.keys() and linkChecker is not None:
								#print lod['link']
								author['@id'] = lod['link']
							else:
								sameAs.append(lod['link']);
						if(len(sameAs) > 0):
							author['sameAs'] = sameAs;
						else:
							author['sameAs'] = [];

					#add into author	 
					stagework['exampleOfWork']['author'].append(author);

			searchContrib = []
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Composer)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Set Designer)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Translator)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Producer)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Conductor)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Choregrapher)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Director)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Editor)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Actor)')
			searchContrib = searchContrib + searchAssocPeople(row, 'Associated People (Architect)')

			if len(searchContrib) > 0:
				searchRec['search_contributor'] = searchContrib
			else:
				searchRec['search_contributor'] = []
			
			contributors = []
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Composer)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Set Designer)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Translator)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Producer)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Conductor)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Choregrapher)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Director)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Editor)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Actor)')
			contributors = contributors + addAssociatedPeople(row, 'Associated People (Architect)')

			if len(contributors) > 0:
				stagework['contributor'] = contributors
			else:
				stagework['contributor'] = []

			if row['Object'].strip() != '':
				record['genre'] = row['Object'].strip()
				searchRec['genre'] = row['Object'].strip()

			if row['Type'].strip() != '' and record['@type'] == 'VisualArtwork':
				record['artform'] = row['Type'].strip()
				searchRec['artform'] = row['Type'].strip()

			if row['Material/Techniques'].strip() != '' and record['@type'] == 'VisualArtwork':
				record['artMedium'] = [mt.strip() for mt in row['Material/Techniques'].split(';')]
				searchRec['artMedium'] = [mt.strip() for mt in row['Material/Techniques'].split(';')]

			if row['Support'].strip() != '' and record['@type'] == 'VisualArtwork':
				record['artworkSurface'] = row['Support'].strip()
				searchRec['artworkSurface'] = row['Support'].strip()

			if row['Dimensions'].strip() != '':
				dimensions = re.match('(.*)x(.*)', row['Dimensions']).groups()
				record['width'] = { '@type': 'Distance', 'name' : dimensions[0].strip() + ' inches' }
				record['height'] = { '@type': 'Distance', 'name' : dimensions[1].strip() + ' inches' }

			record['description'] = []
			searchRec['description'] = []
			if row['Description'].strip() != '':
				record['description'].append(row['Description'].strip())
				searchRec['description'].append(row['Description'].strip())
				
			if row['Notes'].strip() != '':
				record['description'].append(row['Notes'].strip())
				searchRec['description'].append(row['Notes'].strip())

			if row['Production notes'].strip() != '':
				searchRec['description'].append(row['Production notes'].strip())
				if row['Production notes'].strip().startswith('http'):
					stagework['mainEntityOfPage'] = { '@type': 'WebPage', '@id' : row['Production notes'].strip() }
				else:
					stagework['description'] = row['Production notes'].strip()

			if row['Inscriptions'].strip() != '':
				searchRec['description'].append(row['Inscriptions'].strip())
				record['text'] = row['Inscriptions'].strip()

			record['about'] = []
			searchRec['search_subject'] = []
			if row['Style or Period'].strip() != '':
				record['about'] = record['about'] + [sp.strip() for sp in row['Style or Period'].split(';')]
				searchRec['search_subject'] = searchRec['search_subject'] + [sp.strip() for sp in row['Style or Period'].split(';')]

			record['about'].append({ '@id' : 'http://id.loc.gov/authorities/subjects/sh85134531'})

			if row['Subject I (AAT)'].strip() != '':
				for aat in row['Subject I (AAT)'].split(';'):
					eAAT = Entity(aat);
					searchRec['search_subject'].append(eAAT.name)
					if(eAAT.link!=None):
						record['about'].append({'@id': eAAT.link});
					else:
						record['about'].append({'@id': eAAT.name});
				#record['about'] = record['about'] + [aat.strip() for aat in row['Subject I (AAT)'].split(';')]
			if row['Subject II (TGMI)'].strip() != '':
				for tgmi in row['Subject II (TGMI)'].split(';'):
					eTGMI = Entity(tgmi);
					searchRec['search_subject'].append(eTGMI.name)
					if(eTGMI.link!=None):
						record['about'].append({'@id': eTGMI.link});
					else:
						record['about'].append({'@id': eTGMI.name});

				#record['about'] = record['about'] + [tgmi.strip() for tgmi in row['Subject II (TGMI)'].split(';')]

			if row['JPEG URL'].strip() != '':
				record['associatedMedia'] = { 'contentUrl': row['JPEG URL'].strip(), '@type': 'ImageObject', 'fileFormat': 'image/jpg' }
#				record['associatedMedia']['width'] = dimensionDict[record['associatedMedia']['contentUrl']]['width']
#				record['associatedMedia']['height'] = dimensionDict[record['associatedMedia']['contentUrl']]['height']
#				request_url = 'http://djatoka.grainger.illinois.edu/adore-djatoka/resolver?url_ver=Z39.88-2004&rft_id=' + record['associatedMedia']['contentUrl'] + '&svc_id=info:lanl-repo/svc/getMetadata'
#				try:
#					req = urllib.request.Request(request_url)
#					results = urllib.request.urlopen(req)
#					results_string = results.read().decode('utf-8')
#					results_json = json.loads(results_string)
#					record['associatedMedia']['width'] = results_json['width']
#					record['associatedMedia']['height'] = results_json['height']
#				except urllib.error.HTTPError as err:
#					fail_writer.writerow([record['associatedMedia']['contentUrl']])
#					print(record['associatedMedia']['contentUrl']);

			if row['Physical Location'].strip() != '':
				record['provider'] = {'@id' : 'http://viaf.org/viaf/129370513'}

			if row['Collection Title'].strip() != '':
				record['copyrightHolder'] = {'@type' : 'Organization', '@id' : 'http://viaf.org/viaf/129370513', 'name': 'University of Illinois at Urbana-Champaign. Rare Book and Manuscript Library'};

			record['isPartOf'].append(stagework)

			searchOut.write(json.dumps(searchRec, indent=2))
			searchOut.close()
			output.write(json.dumps(record, indent=2))
			print('Processed %d out of %d records	\r' % (row_index,csv_length))
			
def addComponentToCompoundObject(row,row_index,csv_length,fail_writer,parent_file):
#	sys.stdout.write('Processed %d out of %d records	\r' % (row_index,csv_length))
#	sys.stdout.flush()
	print('Processed %d out of %d records	\r' % (row_index,csv_length))
	
	with open('motley-jsonld/' + parent_file, 'r') as compound_object_file:
		json_data = json.load(compound_object_file)

	try:
		if type(json_data['associatedMedia']) is dict:
			json_data['associatedMedia'] = [json_data['associatedMedia']]
	except (NameError, KeyError):
		json_data['associatedMedia'] = []
		
	new_associated_media = { 'contentUrl': row['JPEG URL'].strip(), '@type': 'ImageObject', 'fileFormat': 'image/jpg', 'name': row['Image Title'].strip() }
	request_url = 'http://djatoka.grainger.illinois.edu/adore-djatoka/resolver?url_ver=Z39.88-2004&rft_id=' + new_associated_media['contentUrl'] + '&svc_id=info:lanl-repo/svc/getMetadata'
	try:
		req = urllib.request.Request(request_url)
		results = urllib.request.urlopen(req)
		results_string = results.read().decode('utf-8')
		results_json = json.loads(results_string)
		new_associated_media['width'] = results_json['width']
		new_associated_media['height'] = results_json['height']
	except urllib.error.HTTPError as err:
		fail_writer.writerow([new_associated_media['contentUrl']])
		
	json_data['associatedMedia'].append(new_associated_media)
	with open('motley-jsonld/' + parent_file, 'w') as compound_object_file:
		compound_object_file.write(json.dumps(json_data, indent=2))

def getRootInventoryNumber(code):
	first_seperator_index = code[:10].find('-')
	if first_seperator_index == -1:
		first_seperator_index = code[:10].find('_')
	return code[:first_seperator_index] + code[first_seperator_index+1:first_seperator_index+4]
	
#def getRootInventoryNumber(url):
#	first_seperator_index = url[:10].find('-')
#	if first_seperator_index == -1:
#		first_seperator_index = url[:10].find('_')
#	return url[:first_seperator_index+4]

#with open('ContentDM-Motley-Links.csv', 'rU') as csvfile:
#with open('MotleyTest-FromCDM-27Feb2017.csv', 'rU') as csvfile:
#with open('MotleyTest-FromCDM-20Mar2017.csv', 'rU') as csvfile:
with open('MotleyTest-FromCDM-20Jun2017.csv', 'rU') as csvfile:
#with open('MotleyTest-FromCDM-10Oct2017.csv', 'rU') as csvfile:
#with open('sample2.csv', 'rU') as csvfile:
	reader = csv.DictReader(csvfile, delimiter = ',')
	
	row_index = 0
	start_row = 0
	open_mode = 'w'
	if os.path.isfile('halt_row.txt'):
		open_mode = 'a'
		with open('halt_row.txt','r') as start_row_reader:
			content = start_row_reader.readlines()
			start_row = int(content[0].strip())
	with open('404.csv',open_mode) as fails:
		fail_writer = csv.writer(fails)
		try:
			compound_objects = []
			single_objects = []
			for row in reader:
				if '.cpd' in row['CONTENTdm file path']:
					compound_objects.append(row)
				else:
					single_objects.append(row)
			csv_length = len(compound_objects) + len(single_objects)
			
			compound_object_inventory_numbers = {}
			for row in compound_objects:
				if (row['Inventory Number'] != '') and (row['RDF'] != ''):
					generateNewJSON(row,row_index,csv_length,fail_writer)
					compound_object_inventory_numbers[getRootInventoryNumber(row['Inventory Number'])] = row['RDF'][row['RDF'].rfind('/')+1:-4] + 'json'
				row_index += 1
				
#			print(compound_object_inventory_numbers)
				
			for row in single_objects:
				root_inventory_number = getRootInventoryNumber(row['Inventory Number'])
				if len(root_inventory_number) < len(row['Inventory Number']) and root_inventory_number in compound_object_inventory_numbers:
					addComponentToCompoundObject(row,row_index,csv_length,fail_writer,compound_object_inventory_numbers[root_inventory_number])
				else:
					generateNewJSON(row,row_index,csv_length,fail_writer)
				row_index += 1

			sys.stdout.write('Processed %d out of %d records	\r' % (row_index,csv_length))
			sys.stdout.flush()
				
			if os.path.isfile('halt_row.txt'):
				os.remove('halt_row.txt')
		except:
			fails.close()
#			print(row_index)
			with open('halt_row.txt','w') as halt_row:
				halt_row.write(str(row_index))
				
			raise

					# if row['Inventory Number'].strip() != '':
					#	 output.write('<tr>')
					#	 output.write('<td class="description_col1">')
					#	 output.write('Inventory Number')
					#	 output.write('</td>')
					#	 output.write('<td class="description_col2">')
					#	 #output.write('<span property="scp:standardNumber" content="' + row['Inventory Number'].strip() + '"/>')
					#	 output.write('<span>' + row['Inventory Number'].strip() + '</span>')
					#	 output.write('</td>')
					#	 output.write('</tr>')
