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

def addAssociatedPeople(name):
	person = Person(name.strip())

	name_rdf = {}
	name_rdf['@type'] = 'Person'
	name_rdf['jobTitle'] = 'Actor'

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

#			name_rdfs.append(name_rdf)

	return name_rdf
					
# Niko add
# Make Dictionary for people, performance and theater
# parse people for people dictionary
peopleDict = {}
with open('PoA-Names_WithLinks_Final.csv', 'r',encoding='utf-8') as peopleFile:
	myReader = csv.reader(peopleFile);
	header = next(myReader);
	#print(header);
	peopleReader = csv.DictReader(peopleFile,header,delimiter=',');
	fetchPerson = '';
#	print(peopleReader)
	for row in peopleReader:
#		print(row)
		person = row['NAME'];
		if(person!=''):
			fetchPerson = person;

		peopleDict[fetchPerson] = {};
		peopleDict[fetchPerson]['lod'] = [];	

		if row['VIAF'] != '':
			peopleDict[fetchPerson]['lod'].append({'source': 'VIAF','link': row['VIAF']});
		if row['WIKIPEDIA'] != '':
			peopleDict[fetchPerson]['lod'].append({'source': 'Wikipedia','link': row['WIKIPEDIA']});
		if row['WORLDCAT'] != '':
			peopleDict[fetchPerson]['lod'].append({'source': 'Worldcat Identities','link': row['WORLDCAT']});
		if row['LOC'] != '':
			peopleDict[fetchPerson]['lod'].append({'source': 'LC Name Authority','link': row['LOC']});
		if row['IMDb'] != '':
			peopleDict[fetchPerson]['lod'].append({'source': 'IMDb','link': row['IMDb']});
		if row['IBDb'] != '':
			peopleDict[fetchPerson]['lod'].append({'source': 'IBDb','link': row['IBDb']});
		if row['LOC (Popular Graphic Arts)'] != '':
			peopleDict[fetchPerson]['lod'].append({'source': 'Popular Graphic Arts','link': row['LOC (Popular Graphic Arts)']});
#		role = row['Role'];
#		website = row['Website'];
#		link = row['Link']
#		if fetchPerson not in peopleDict.keys():
#			peopleDict[fetchPerson] = {};
#			peopleDict[fetchPerson]['lod'] = [];
#		
#		if(role!=''):
#			peopleDict[fetchPerson]['role'] = role;
#		if(website!='' and link!=''):
#			peopleDict[fetchPerson]['lod'].append({'source': website,'link': link});

	#print(json.dumps(peopleDict));

#performanceDict = {}
#with open('Motley_Performance_Links_Full.csv', 'r') as perfFile:
#	myReader = csv.reader(perfFile);
#	header = next(myReader);
#	#print(header);
#	perfReader = csv.DictReader(perfFile,header,delimiter=',');
#	fetchPerf = '';
#	for row in perfReader:
#		production = row['Production'];
#		if(production!=''):
#			fetchPerf = production;
#		year = row['Year'];
#		location = row['Location'];
#		source = row['Source'];
#		sourceType = row['Source Type'];
#		link = row['Link']
#		if fetchPerf not in performanceDict.keys():
#			performanceDict[fetchPerf] = {};
#			performanceDict[fetchPerf]['lod'] = [];
#		
#		if(year!=''):
#			performanceDict[fetchPerf]['year'] = year;
#		if(location!=''):
#			performanceDict[fetchPerf]['location'] = location;
#		if(source!='' and link!=''):
#			performanceDict[fetchPerf]['lod'].append({ 'source': source, 'type': sourceType, 'link': link });

	#print(json.dumps(performanceDict));

#theatreDict = {}
#with open('Motley_Theatre_Links_Full.csv', 'r') as theaterFile:
#	myReader = csv.reader(theaterFile);
#	header = next(myReader);
#	#print(header);
#	theaterReader = csv.DictReader(theaterFile,header,delimiter=',');
#	fetchTheater = '';
#	for row in theaterReader:
#		theater = row['Theatre'];
#		if(theater!=''):
#			fetchTheater = theater;
#		source = row['Source'];
#		link = row['Link']
#		if fetchTheater not in theatreDict.keys():
#			theatreDict[fetchTheater] = {};
#			theatreDict[fetchTheater]['lod'] = [];
#		
#		if(source!='' and link!=''):
#			theatreDict[fetchTheater]['lod'].append({ 'source': source, 'link': link });

#dimensionDict = {}
#with open('imageDimentions.csv','r') as dimensionFile:
#	myReader = csv.reader(dimensionFile)
#	header = next(myReader)
#	dimensionReader = csv.DictReader(dimensionFile,header,delimiter=',')
#	for row in dimensionReader:
#		dimensionDict[row['Image URL']] = {'width': row['Width'], 'height': row['Height']}

#handleDict = {}
#with open('Motley_handles.csv','r') as handlesFile:
#	myReader = csv.reader(handlesFile)
#	header = next(myReader)
#	handlesReader = csv.DictReader(handlesFile,header,delimiter=',')
#	for row in handlesReader:
#		handleDict[row['@id']] = row['Handle']


	#print(json.dumps(theatreDict));

# End of additional dictionary

def generateNewJSON(row,row_index,csv_length,fail_writer):
	record = {}
	stagework = {}
	sys.stdout.write('Processed %d out of %d records	\r' % (row_index,csv_length))
	sys.stdout.flush()
	if row_index >= start_row:
#		stagework = {}
		# parse contentDm number from rdf file
		rdfaLink = 'http://imagesearch-test1.library.illinois.edu/jsonld/actors/' + row['CONTENTdm number'] + '.json'
		filename = row['CONTENTdm number'] + '.json'

		refURL2 = row['Reference URL'].replace('imagesearchnew', 'imagesearch-test1')


		#with open('motley-rdfa-google/' + row['CONTENTdm number'] + '.json', 'w') as output:
		with open('PoA_JSON-LDs/' + filename, 'w') as output:
			record['@context'] = [ 'http://schema.org/', { 's': 'http://schema.org/', 'scp': 'http://ns.library.illinois.edu/scp/', 'fileFormat': { '@id': 's:fileFormat', '@type': 's:Text' }, 'artform': { '@id': 's:artform', '@type': 's:Text' }, 'artworkSurface': { '@id': 's:artworkSurface', '@type': 's:Text' }, 'artMedium': { '@id': 's:artMedium', '@type': 's:Text' }, 'genre': { '@id': 's:genre', '@type': 's:Text' } } ]
			# this must be changed to reference url
			record['@id'] = refURL2;
#			record['sameAs'] = [ 'http://imagesearch-test1.library.illinois.edu/cdm/search/collection/motley-new/searchterm/' + row['Inventory Number']]
#			if record['@id'] in handleDict:
#				record['sameAs'].append(handleDict[record['@id']])
			record['@type'] = 'CreativeWork'
			if row['Creator'].strip() != '':
				if ';' in row['Creator']:
					record['creator'] = []
					creators = row['Creator'].split(';')
					for creator in creators:
						record['creator'].append({ '@type': 'Person', 'name': creator })
				else:
					record['creator'] = { '@type': 'Person', 'name': row['Creator'] }
#			object_content = row['Object'].strip()
#			if object_content != '' and object_content in ['Character sketch', 'Costume design', 'Costume rendering', 'Costume sketch', 'Costume work drawing', 'Instrument rendering', 'Mask sketch', 'Prop design', 'Props', 'Sandals sketch', 'Set design', 'Set desing', 'Set detail', 'Set rendering', 'Sketch', 'Stage props', 'Working drawing']:
#				record['@type'] = 'VisualArtwork'
			record['name'] = row['Title'].strip()
			record['isPartOf'] = [{ '@id' : 'http://http://imagesearch-test1.library.illinois.edu/cdm/landingpage/collection/actors/',
														'@type' : 'CreativeWork', 'additionalType' : 's:Collection'}]

			#stagework['@id'] = 'http://imagesearch-test1.library.illinois.edu/cdm/landingpage/collection/motley-new/'
			stagework['@type'] = 'CreativeWork'
			stagework['additionalType'] = 'scp:StageWork'

			if row['Play'].strip() != '':			
				stagework['name'] = row['Play'].strip()
				# niko add sameAs attribute
				performance = stagework['name'];
#				if performance in performanceDict.keys():
#					stagework['sameAs'] = [];
#					lods = performanceDict[performance]['lod'];
#					for lod in lods:
#						if '@id' not in stagework and 'wikipedia.org' in lod['link']:
#							stagework['@id'] = lod['link']
#						else:
#							stagework['sameAs'].append(lod['link']);

			if row['Date'].strip() != '':
				stagework['dateCreated'] = row['Date'].strip()

			# ad multi theater 
#			myTheaters = row['Theater'].split(';');
#			myStageworks = [];
#			for myTheater in myTheaters: 
#				#if row['Theater'].strip() != '':
#				print(myTheater)
#				if myTheater.strip() != '':
#					print(myTheater)
#					entity = Entity(myTheater.strip())
#					theater = {};
#
#					if entity.link != None:
#						#stagework['locationCreated'] = { '@id' : entity.link }
#						theater = { '@id' : entity.link }
#					else:
#						#stagework['locationCreated'] =	entity.name 
#						theater = { 'name': entity.name };
#
#					#print(theater);
#					if entity.name in theatreDict.keys():
#							sameAs = [];
#							lods = theatreDict[entity.name]['lod'];
#							#print(lods);
#							for lod in lods:
#								if '@id' not in theater and 'wikipedia.org' in lod['link']:
#									theater['@id'] = lod['link']
#								else:
#									sameAs.append(lod['link']);
#							if(len(sameAs) > 0):
#								theater['sameAs'] = sameAs;
#
#					# sum it up to stagework
#					myStageworks.append(theater);
#
#			stagework['locationCreated'] = myStageworks;



#			if row['Author'].strip() != '':
#				stagework['exampleOfWork'] = { '@type' : 'Book', 'author' : [] }
#				names = row['Author'].split(';')
#				for name in names:
#					person = Person(name.strip())
#					author = {}
#					if person.link != None:				
#						# niko modified this code to make element instead of string only
#						# stagework['exampleOfWork']['author'].append({ '@type' : 'Person', '@id' : person.link })
#						author = { '@type' : 'Person', '@id' : person.link };
#					else:
#						# niko modified this code to make element instead of string only
#						# stagework['exampleOfWork']['author'].append(person.name)
#						author = { 'name': person.name }
#						# stagework['exampleOfWork']['author'].append(person.name)
#
#					# niko modified this code to add sameAs						
#					if person.fullname in peopleDict.keys():
#						sameAs = [];						
#						lods = peopleDict[person.fullname]['lod'];
#						for lod in lods:
#							# check if it is dbpedia or viaf
#							linkChecker = re.search('viaf.org', lod['link'])
#							if '@id' not in author.keys() and linkChecker is not None:
#								#print lod['link']
#								author['@id'] = lod['link']
#							else:
#								sameAs.append(lod['link']);
#						if(len(sameAs) > 0):
#							author['sameAs'] = sameAs;
#						else:
#							author['sameAs'] = [];
#
#					#add into author	 
#					stagework['exampleOfWork']['author'].append(author);


			
			contributors = []
			subjects = row['Subject'].split(';')

			record['about'] = []
			for instance in subjects:
				if re.match(".* 1[2-9][0-9]",instance):
					contributors.append(addAssociatedPeople(instance.strip()))
				else:
					record['about'].append({"name": instance.strip()})
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Composer)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Set Designer)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Translator)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Producer)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Conductor)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Choregrapher)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Director)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Editor)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Actor)')
#			contributors = contributors + addAssociatedPeople(row, 'Associated People (Architect)')

			if len(contributors) > 0:
				stagework['contributor'] = contributors
			else:
				stagework['contributor'] = []


			record['genre'] = 'Portrait'

			if row['Type'].strip() != '' and record['@type'] == 'VisualArtwork':
				record['artform'] = [t.strip() for t in row['Type'].split(';')]

			if row['Technique'].strip() != '' and record['@type'] == 'VisualArtwork':
				record['artMedium'] = [mt.strip() for mt in row['Technique'].split(';')]

#			if row['Support'].strip() != '' and record['@type'] == 'VisualArtwork':
#				record['artworkSurface'] = row['Support'].strip()

			if row['Dimensions'].strip() != '':
				try:
					dimensions = re.match('(.*)x(.*)', row['Dimensions']).groups()
					record['width'] = { '@type': 'Distance', 'name' : dimensions[0].strip() + ' inches' }
					record['height'] = { '@type': 'Distance', 'name' : dimensions[1].strip() + ' inches' }
				except:
					pass

			record['description'] = []
			if row['Description'].strip() != '':
				record['description'].append(row['Description'].strip())
#			if row['Notes'].strip() != '':
#				record['description'].append(row['Notes'].strip())

#			if row['Production notes'].strip() != '':
#				if row['Production notes'].strip().startswith('http'):
#					stagework['mainEntityOfPage'] = { '@type': 'WebPage', '@id' : row['Production notes'].strip() }
#				else:
#					stagework['description'] = row['Production notes'].strip()

#			if row['Inscriptions'].strip() != '':
#				record['text'] = row['Inscriptions'].strip()

#			record['about'] = []
#			if row['Style or Period'].strip() != '':
#				record['about'] = record['about'] + [sp.strip() for sp in row['Style or Period'].split(';')]

#			record['about'].append({ '@id' : 'http://id.loc.gov/authorities/subjects/sh85134531'})
#
#			if row['Subject I (AAT)'].strip() != '':
#				for aat in row['Subject I (AAT)'].split(';'):
#					eAAT = Entity(aat);
#					if(eAAT.link!=None):
#						record['about'].append({'@id': eAAT.link});
#					else:
#						record['about'].append({'@id': eAAT.name});
#				#record['about'] = record['about'] + [aat.strip() for aat in row['Subject I (AAT)'].split(';')]
#			if row['Subject II (TGMI)'].strip() != '':
#				for tgmi in row['Subject II (TGMI)'].split(';'):
#					eTGMI = Entity(tgmi);
#					if(eTGMI.link!=None):
#						record['about'].append({'@id': eTGMI.link});
#					else:
#						record['about'].append({'@id': eTGMI.name});

				#record['about'] = record['about'] + [tgmi.strip() for tgmi in row['Subject II (TGMI)'].split(';')]

			if row['CONTENTdm file path'].strip() != '':
				record['associatedMedia'] = { 'contentUrl': row['CONTENTdm file path'].strip().replace('image','jpg'), '@type': 'ImageObject', 'fileFormat': 'image/jpg' }
#				record['associatedMedia']['width'] = dimensionDict[record['associatedMedia']['contentUrl']]['width']
#				record['associatedMedia']['height'] = dimensionDict[record['associatedMedia']['contentUrl']]['height']
				request_url = 'http://djatoka.grainger.illinois.edu/adore-djatoka/resolver?url_ver=Z39.88-2004&rft_id=' + record['associatedMedia']['contentUrl'] + '&svc_id=info:lanl-repo/svc/getMetadata'
				try:
					req = urllib.request.Request(request_url)
					results = urllib.request.urlopen(req)
					results_string = results.read().decode('utf-8')
					results_json = json.loads(results_string)
					record['associatedMedia']['width'] = results_json['width']
					record['associatedMedia']['height'] = results_json['height']
				except urllib.error.HTTPError as err:
					fail_writer.writerow([record['associatedMedia']['contentUrl']])
					print(record['associatedMedia']['contentUrl']);

			if row['Physical Collection'].strip() != '':
				record['provider'] = {'@id' : 'http://viaf.org/viaf/129370513'}

			if row['Repository'].strip() != '':
				record['copyrightHolder'] = {'@type' : 'Organization', '@id' : 'http://viaf.org/viaf/129370513', 'name': 'University of Illinois at Urbana-Champaign. Rare Book and Manuscript Library'};

			record['isPartOf'].append(stagework)

			output.write(json.dumps(record, indent=2))
			
def addComponentToCompoundObject(row,row_index,csv_length,fail_writer,parent_file):
	sys.stdout.write('Processed %d out of %d records	\r' % (row_index,csv_length))
	sys.stdout.flush()
	
	with open('motley-rdfa-google/' + parent_file, 'r') as compound_object_file:
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
	with open('motley-rdfa-google/' + parent_file, 'w') as compound_object_file:
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
with open('PoANew.csv', 'rU') as csvfile:
#with open('sample2.csv', 'rU') as csvfile:
	reader = csv.DictReader(csvfile, delimiter = ',')
	
	row_index = 0
	start_row = 0
	open_mode = 'w'
	if os.path.isfile('poa_halt_row.txt'):
		open_mode = 'a'
		with open('poa_halt_row.txt','r') as start_row_reader:
			content = start_row_reader.readlines()
			start_row = int(content[0].strip())
	with open('poa_404.csv',open_mode) as fails:
		fail_writer = csv.writer(fails)
		try:
			single_objects = []
			for row in reader:
				print(row)
				single_objects.append(row)
			csv_length = len(single_objects)
				
			for row in single_objects:
				generateNewJSON(row,row_index,csv_length,fail_writer)
				row_index += 1

			sys.stdout.write('Processed %d out of %d records	\r' % (row_index,csv_length))
			sys.stdout.flush()
				
			if os.path.isfile('poa_halt_row.txt'):
				os.remove('poa_halt_row.txt')
		except:
			fails.close()
#			print(row_index)
			with open('poa_halt_row.txt','w') as halt_row:
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
