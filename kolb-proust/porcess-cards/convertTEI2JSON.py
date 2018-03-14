# -*- coding: utf-8 -*-
import os, json, datetime, re, csv, sys
from shutil import copyfile
from lxml import etree
from unicodedata import normalize
import codecs

if os.name == 'nt':
	SLASH = '\\'
else:
	SLASH = '/'

def readFormattedDate(target_date):
#	print(target_date)
	if len(target_date) == 4:
		return target_date
	elif len(target_date) == 6:
		if target_date[4:6] == '00':
			return target_date[:4]
		elif int(target_date[4:6]) <= 12:
			return target_date[:4] + '-' + target_date[4:6]
		else:
			format = '%Y%d'
	elif len(target_date) == 8:
		if target_date[6:] == '00' and target_date[4:6] == '00':
			return target_date[:4]
		elif target_date[4:6] == '00' and target_date[6:] != '00':
			format = '%Y00%d'
		elif target_date[6:] == '00':
			if int(target_date[4:6]) <= 12:
				return target_date[:4] + '-' + target_date[4:6]
			else:
				format = '%Y%d00'
		else:
			if int(target_date[4:6]) <= 12:
				format = '%Y%m%d'
			else:
				format = '%Y%d%m'
	else:
		if len(target_date) > 8:
			return readFormattedDate(target_date[:8])
		elif len(target_date) > 6:
			return readFormattedDate(target_date[:6])
		elif len(target_date) > 4:
			return target_date[:4]
		elif len(target_date) > 2:
			format = '%y'

	print(target_date)
	return datetime.datetime.strptime(target_date,format).date().isoformat()

def extractDateFromText(text_string):
	print("EXTRACTING DATE")
	print(text_string)
	year_results = re.search(r'[12][890][0-9][0-9]',text_string)
	year = None
	if year_results:
		year = year_results.group(0)
		print(year_results.group(0))

	month = None
	month_results = re.search(ur'(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)',normalize('NFC',(text_string.lower().decode('utf-8') if isinstance(text_string,str) else text_string.lower())))
	months = {u'janvier': '01',u'février': '02',u'mars': '03',u'avril': '04',u'mai': '05',u'juin': '06',u'juillet': '07',u'août': '08',u'septembre': '09',u'octobre': '10',u'novembre': '11',u'décembre': '12'}
	if month_results:
		month = months[month_results.group(0)]
		print(month_results.group(0))
	else:
		month = '00'

	thirty_one_day_re = r'( )?(1er|[1-9]|[12][0-9]|3[01]) '
	thirty_day_re = r'( )?(1er|[1-9]|[12][0-9]|30) '
	twenty_nine_day_re = r'( )?(1er|[1-9]|[12][0-9]) '

	day = None
	if month in ['01','03','05','07','08','10','12']:
		day_result = re.search(thirty_one_day_re,text_string)
	elif month in ['04','06','09','11']:
		day_result = re.search(thirty_day_re,text_string)
	else:
		day_result = re.search(twenty_nine_day_re,text_string)

	if day_result:
		print(day_result.group(0).strip(' '))
		day = day_result.group(0).strip(' ')
		if day == '1er':
			day = '01'
		elif len(day) == 1:
			day = '0' + day
	else:
		day = '00'

	if type(year) is unicode:
		year = year.encode('utf-8')

	if type(day) is unicode:
		day = day.encode('utf-8')
	
	if not year:
		return None
	else:
		try:
			return readFormattedDate(year+month+day)
		except ValueError:
			return None

def extractIssueOrVolumeNumber(text_string,mode):
	if mode == 'volume':
		result = re.search(r'vol\. ([0-9]|[ivx])*,',text_string)
	else:
		result = re.search(r'n\. ([0-9]|[ivx])*,',text_string)

	if result:
		print(result.group(0))
		number = result.group(0)[result.group(0).find('.')+2:-1]
		return number
	else:
		return None

def extractIssueNumber(text_string):
	return extractIssueOrVolumeNumber(text_string,'issue')

def extractVolumeNumber(text_string):
	return extractIssueOrVolumeNumber(text_string,'volume')

def getPages(text_string):
	page_results = re.search(r'p\. ([0-9]*:)?[0-9]+-?[0-9]*(, ([0-9]*:)?[0-9]+-?[0-9]*)*',text_string)
	if page_results:
		page_results_string = page_results.group(0)[3:]

		first_dash = page_results_string.find('-')
		first_colon = page_results_string.find(':')
		first_comma = page_results_string.find(',')

		#cases:
		#p. #:#  		X
		#p. #:#- 		X
		#p. #:#, 		X
		#p. #-			X
		#p. #,			X
		#p. #    		X
		#Null cases     X

		if first_dash < 0 and first_colon < 0 and first_comma < 0:
			first_page = page_results_string
		if first_colon > 0 and ((first_colon < first_dash or first_colon < first_comma) or (first_dash < 0 and first_comma < 0)):
			first_page = page_results_string[:first_colon]
		elif first_colon < 0 or (first_dash > 0 and first_dash < first_colon) or (first_comma > 0 and first_comma < first_colon):
			if (first_dash < first_comma and first_dash > 0) or (first_dash > 0 and first_comma < 0):
				first_page = page_results_string[:first_dash]
			elif (first_comma < first_dash and first_comma > 0) or (first_comma > 0 and first_dash < 0):
				first_page = page_results_string[:first_comma]
		else:
			first_page = None

		last_dash = page_results_string.rfind('-')
		last_colon = page_results_string.rfind(':')
		last_comma = page_results_string.rfind(',')

		#cases:
		# -#
		# , #
		# , #:#

		if last_dash < 0 and last_colon < 0 and last_comma < 0:
			last_page = None
		elif last_dash >= first_dash and last_dash > last_colon and last_dash > last_comma:
			last_page = page_results_string[last_dash+1:]
		elif last_comma >= first_comma and last_comma > last_dash:
			if last_colon > last_comma:
				last_page = page_results_string[last_comma+2:last_colon]
			else:
				last_page = page_results_string[last_comma+2:]
		else:
			last_page = None

		if last_page and len(last_page) < len(first_page):
			last_page = first_page[:len(first_page)-len(last_page)] + last_page

		return first_page, last_page

	return None, None

def getTitle(root,path):
	rs_title = root.xpath(path+'rs//text()')
	if rs_title:
		return ' '.join(' '.join(rs_title).strip().split())
	else:
		title = root.xpath(path+'/text()')
		if title:
			return ' '.join(' '.join(title).strip().split())
		else:
			return None

def addLinkToCitation(new_citation,tei_file):
	if ('isPartOf' in new_citation and ('name' in new_citation['isPartOf'] or ('isPartOf' in new_citation['isPartOf'] and 'name' in new_citation['isPartOf']['isPartOf']))) or 'name' in new_citation:
		if 'isPartOf' in new_citation and 'isPartOf' in new_citation['isPartOf'] and 'name' in new_citation['isPartOf']['isPartOf']:
			journal_name = new_citation['isPartOf']['isPartOf']['name']
			link_location = new_citation
#			link_location = new_citation['isPartOf']['isPartOf']
		elif 'isPartOf' in new_citation and 'name' in new_citation['isPartOf']:
			journal_name = new_citation['isPartOf']['name']
			link_location = new_citation
#			link_location = new_citation['isPartOf']
		else:
			journal_name = new_citation['name']
			link_location = new_citation

		if journal_name.strip() == 'Figaro' or journal_name.strip() == 'Le Figaro':
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb34355551z/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'Gaulois' or journal_name.strip() == 'Le Gaulois':
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb32779904b/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'Journal des Debats' or journal_name.strip() == 'Le Journal des Debats' or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u'Journal des Débats') or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u'Le Journal des Débats'):
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb39294634r/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'Echo de Paris' or journal_name.strip() == 'Écho de Paris' or journal_name.strip() == "L'Echo de Paris" or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u'Écho de Paris') or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u"L'Echo de Paris"):
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb34429768r/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'Gil Blas':
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb344298410/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'Le Temps' or journal_name.strip() == 'Temps':
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb34431794k/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'La Presse':
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb34448033b/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'Chronique des Arts et de la Curiosité' or journal_name.strip() == 'Chroniques des Arts et de la curiosité' or journal_name.strip() == 'Voir Chronique des Arts et de la curiosité' or journal_name.strip() == 'Chronique des Arts et de la curiosité' or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u'Chronique des Arts et de la Curiosité') or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u'Chroniques des Arts et de la curiosité') or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u'Voir Chronique des Arts et de la curiosité') or normalize('NFC',journal_name.encode('utf-8').decode('utf-8').strip()) == normalize('NFC',u'Chronique des Arts et de la curiosité'):
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://gallica.bnf.fr/ark:/12148/cb34421972m/date' + new_citation['datePublished'][:4] + new_citation['datePublished'][5:7] + new_citation['datePublished'][8:] + '.item'
				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])
		elif journal_name.strip() == 'The New York Herald' or journal_name.strip() == 'New York Herald':
			if 'datePublished' in new_citation:
				link_location['sameAs'] = 'http://fultonhistory.com/my%20photo%20albums/All%20Newspapers/New%20York%20NY%20Herald/New%20York%20NY%20Herald%20' + new_citation['datePublished'][:4] + '/index.html'

				print(link_location['sameAs'])

#				with open('JournalLinks.csv','a') as outfile:
#					outfileWriter = csv.writer(outfile)
#
#					outfileWriter.writerow([tei_file[tei_file.rfind('/')+1:],link_location['sameAs']])


	return new_citation

def generateChronologyCitation(bibl_root,linked_names,tei_file):
	new_citation = {}
#	text_data = max([ x.strip() for x in bibl_root.xpath('./text()') ],key=len)
	print(bibl_root)
	text_data = bibl_root.xpath('normalize-space(.)')
	print("TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA TEXT DATA")
	print(text_data)

	new_titles = bibl_root.xpath('.//title')

	if len(new_titles) > 1:
		check_levels = bibl_root.xpath('.//title/@level')
		if check_levels.count('j') > 1:
			return new_citation

	title_counter = 0
	new_author = bibl_root.xpath('.//author/name/@key')
	if new_author:
		new_citation['author'] = { '@type': 'Person', '@id': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + new_author[0] }

	date_published = extractDateFromText(text_data)
	if date_published:
		new_citation['datePublished'] = date_published

	for title in new_titles:
		new_types = title.xpath('./@type')
		new_levels = title.xpath('./@level')

		if title_counter > 0:
			print("Multiple Titles")
			if 'j' in new_levels:
				new_citation['isPartOf'] = { '@type': 'PublicationIssue' }
				date_created = extractDateFromText(text_data)
				if date_created:
					new_citation['isPartOf']['dateCreated'] = date_created
				issue_number = extractIssueNumber(text_data)
				if issue_number:
					new_citation['isPartOf']['issueNumber'] = issue_number

				new_citation['isPartOf']['isPartOf'] = { '@type': 'PublicationVolume' }
				new_citation['isPartOf']['isPartOf']['name'] = getTitle(title,'./')

				volume_number = extractVolumeNumber(text_data)
				if volume_number:
					new_citation['isPartOf']['isPartOf']['volumeNumber'] = volume_number
				
				print(new_citation['isPartOf']['isPartOf']['name'])

			if 'isPartOf' in new_citation and 'isPartOf' in new_citation['isPartOf'] and 'issueNumber' in new_citation['isPartOf'] and 'volumeNumber' in new_citation['isPartOf']['isPartOf']:
				new_citation['isPartOf']['name'] = new_citation['isPartOf']['isPartOf']['name'] + ', ' + new_citation['isPartOf']['isPartOf']['volumeNumber'] + ', ' + new_citation['isPartOf']['issueNumber']

		else:
			new_citation['@type'] = 'CreativeWork'
			page_start, page_end = getPages(text_data)
			if page_start:
				new_citation['pageStart'] = page_start
			if page_end:
				new_citation['pageEnd'] = page_end

			if ('es' in new_types or 're' in new_types) or 'a' in new_levels:
				new_citation['headline'] = getTitle(title,'./')

				new_citation['additionalType'] = 'http://schema.org/Article'
			else:
				if 'j' in new_levels:
					new_citation['additionalType'] = 'http://schema.org/Article'

					new_citation['isPartOf'] = { '@type': 'PublicationIssue' }
					date_created = extractDateFromText(text_data)
					if date_created:
						new_citation['isPartOf']['dateCreated'] = date_created
					issue_number = extractIssueNumber(text_data)
					if issue_number:
						new_citation['isPartOf']['issueNumber'] = issue_number

					new_citation['isPartOf']['isPartOf'] = { '@type': 'PublicationVolume' }
					new_citation['isPartOf']['isPartOf']['name'] = getTitle(title,'./')

					volume_number = extractVolumeNumber(text_data)
					if volume_number:
						new_citation['isPartOf']['isPartOf']['volumeNumber'] = volume_number
					
					print(new_citation['isPartOf']['isPartOf']['name'])
				else:
					new_citation['name'] = getTitle(title,'./')


		title_counter += 1

	cor_find = re.search(r', Cor [XIVL]+,',text_data)
	if cor_find:
		cor_volume = cor_find.group(0)[6:-1]
		new_citation['@type'] = 'CreativeWork'
		new_citation['name'] = 'Correspondance'
		new_citation['author'] = { '@type': 'Person', '@id': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/proust1' }
		new_citation['isPartOf'] = { '@type': 'PublicationVolume', 'volumeNumber': cor_volume }
		new_citation['editor'] = { '@type': 'Person', '@id': 'http://viaf.org/viaf/44300868'}
		new_citation['datePublished'] = '1970--1993'
		page_start, page_end = getPages(text_data)
		if page_start:
			new_citation['isPartOf']['pageStart'] = page_start
		if page_end:
			new_citation['isPartOf']['pageEnd'] = page_end
		print("CORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXTCORTEXT")
		print(text_data)

	new_citation = addLinkToCitation(new_citation,tei_file)

	return new_citation

def getDate(root,path):
	when_dates = root.xpath(path + '@when')
	if when_dates:
		try:
			int(when_dates[0])
			return readFormattedDate(when_dates[0])
		except:
			value_dates = root.xpath(path + '@value')
			if value_dates:
				try:
					int(value_dates[0])
					return readFormattedDate(value_dates[0])
				except:
					text_dates = root.xpath(path + 'text()')
					if text_dates:
						return extractDateFromText(text_dates[0])
					else:
						return None
			else:
				text_dates = root.xpath(path + 'text()')
				if text_dates:
					return extractDateFromText(text_dates[0])
				else:
					return None
	else:
		value_dates = root.xpath(path + '@value')
		if value_dates:
			try:
				int(value_dates[0])
				return readFormattedDate(value_dates[0])
			except:
				text_dates = root.xpath(path + 'text()')
				print(text_dates)
				if text_dates:
					print(extractDateFromText(text_dates[0]))
					return extractDateFromText(text_dates[0])
				else:
					return None
		else:
			text_dates = root.xpath(path + 'text()')
			if text_dates:
				return extractDateFromText(text_dates[0])
			else:
				return None

def generateBibCitation(bibl_root,linked_names,tei_file):
	new_citation = {}
	text_data = bibl_root.xpath('normalize-space(.)')
	new_titles = bibl_root.xpath('.//title')

	if len(new_titles) > 1:
		check_levels = bibl_root.xpath('.//title/@level')
		if check_levels.count('j') > 1:
			return new_citation

	title_counter = 0
	new_author = bibl_root.xpath('.//author/name/@key')
	if new_author:
		new_citation['author'] = { '@type': 'Person', '@id': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + new_author[0] }
	else:
		new_authors = bibl_root.xpath('.//author/name/text()')
		if new_authors:
			for author in new_authors:
				if author in linked_names[1]:
					new_citation['author'] = { '@type': 'Person', '@id': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + linked_names[0][linked_names[1].index(author)] }
					print("FOUND AUTHOR IN CITATION")
					print(author)
					print(linked_names[0][linked_names[1].index(author)])

	new_citation['datePublished'] = getDate(bibl_root,'./date/')
	if not new_citation['datePublished']:
		del new_citation['datePublished']

	for title in new_titles:
		new_types = title.xpath('./@type')
		new_levels = title.xpath('./@level')

		if title_counter > 0:
			print("Multiple Titles")
#			text_data = max([ x.strip() for x in bibl_root.xpath('./text()') ],key=len)

			if 'j' in new_levels or 'm' in new_levels:
				new_issue_number = bibl_root.xpath('./biblScope[@type="issue"]/text()')
				if new_issue_number:
					new_is_part_of = { '@type': 'PublicationIssue', 'issueNumber' : new_issue_number[0] }

					new_is_part_of['dateCreated'] = getDate(bibl_root,'./date/')
					if not new_is_part_of['dateCreated']:
						del new_is_part_of['dateCreated']

					if 'isPartOf' not in new_citation:
						new_citation['isPartOf'] = new_is_part_of
					else:
						new_is_part_of['isPartOf'] = new_citation['isPartOf']
						new_citation['isPartOf'] = new_is_part_of

				journal_title = getTitle(title,'./')
				if journal_title:
					if 'm' in new_levels:
						new_is_part_of = { '@type': 'Book', 'name': journal_title }
					else:
						new_is_part_of = { '@type': 'PublicationVolume', 'name': journal_title }

					new_volume_number = bibl_root.xpath('./biblScope[@type="vol"]/text()')
					if new_volume_number:
						new_is_part_of['volumeNumber'] = new_volume_number[0]

					if 'isPartOf' not in new_citation:
						new_citation['isPartOf'] = new_is_part_of
					else:
						new_citation['isPartOf']['isPartOf'] = new_is_part_of

				pub_place = bibl_root.xpath('./pubPlace/text()')
				if pub_place:
					new_citation['locationCreated'] = pub_place[0]

				new_publisher = bibl_root.xpath('./publisher/text()')
				if new_publisher:
					new_citation['publisher'] = new_publisher[0]

			else:
				new_citation['isPartOf'] = { '@type': 'PublicationVolume' }

				new_volume_number = bibl_root.xpath('./biblScope[@type="vol"]/text()')
				if new_volume_number:
					new_citation['isPartOf']['volumeNumber'] = new_volume_number[0]

			if 'isPartOf' in new_citation and 'isPartOf' in new_citation['isPartOf'] and 'volumeNumber' in new_citation['isPartOf']['isPartOf']:
				new_citation['isPartOf']['name'] = new_citation['isPartOf']['isPartOf']['name'] + ', ' + new_citation['isPartOf']['isPartOf']['volumeNumber'] + ', ' + new_citation['isPartOf']['issueNumber']

		else:
			new_citation['@type'] = 'CreativeWork'
			new_pages = bibl_root.xpath('./biblScope[@type="pages"]/text()')
			if new_pages:
				page_start, page_end = getPages(new_pages[0])
				if page_start:
					new_citation['pageStart'] = page_start
				if page_end:
					new_citation['pageEnd'] = page_end

			if ('es' in new_types or 're' in new_types) or 'a' in new_levels:
				new_citation['headline'] = getTitle(title,'./')
				if not new_citation['headline']:
					del new_citation['headline']
				else:
					new_citation['additionalType'] = 'http://schema.org/Article'
			else:
				new_citation['name'] = getTitle(title,'./')
				if not new_citation['name']:
					del new_citation['name']

				if 'j' in new_levels:
					new_citation['additionalType'] = 'http://schema.org/Article'

		title_counter += 1

	new_citation = addLinkToCitation(new_citation,tei_file)

	return new_citation

def processTEIFile(tei_file,linked_names):
	with open(tei_file,'rb') as infile:
		card = infile.read()

	output_card = {
		'@context': [ 
			'http://schema.org/',
			{
				'temporalCoverage': {
					'@id': 'schema:temporalCoverage',
					'@type': 'Date'
				}
			}
		]
	}
#	print(card)
	root = etree.fromstring(card)

	output_card['@id'] = 'http://kolbproust.library.illinois.edu/proust/data/' + tei_file[:-4]

	card_type = tei_file[tei_file.rfind('/')+1:][0]
	if card_type == 's' or card_type == 'p':
		#bibliography
		output_card['@type'] = 'Dataset'
		output_card['author'] = { '@type': 'Person', '@id': 'http://viaf.org/viaf/44300868'}
		print(output_card['@id'])
#		print(root.xpath('/TEI/teiHeader/fileDesc/titleStmt/title/text()'))
		output_card['name'] = [ "Fiches bibliographiques des oeuvres de Marcel Proust 1959 - 1965", "Bibliographical cards: Works by Marcel Proust, 1959 - 1965" ]
#		print(root.xpath('/TEI/teiHeader/fileDesc/editionStmt/edition/date/@when')[0])
		output_card['dateCreated'] = getDate(root,'/TEI/teiHeader/fileDesc/editionStmt/edition/date/')
		if not output_card['dateCreated']:
			del output_card['dateCreated']
#		if root.xpath('/TEI/teiHeader/fileDesc/editionStmt/edition/date/@when'):
#			output_card['dateCreated'] = readFormattedDate(root.xpath('/TEI/teiHeader/fileDesc/editionStmt/edition/date/@when')[0]).date().isoformat()
#		elif root.xpath('/TEI/teiHeader/fileDesc/editionStmt/edition/date/@value'):
#			output_card['dateCreated'] = readFormattedDate(root.xpath('/TEI/teiHeader/fileDesc/editionStmt/edition/date/@value')[0]).date().isoformat()
		output_card['temporalCoverage'] = getDate(root,'/TEI/text/body/div1/head/date/')
		if not output_card['temporalCoverage']:
			del output_card['temporalCoverage']
#		if root.xpath('/TEI/text/body/div1/head/date/@when'):
#			output_card['temporalCoverage'] = readFormattedDate(root.xpath('/TEI/text/body/div1/head/date/@when')[0]).date().isoformat()
#		elif root.xpath('/TEI/text/body/div1/head/date/@value'):
#			output_card['temporalCoverage'] = readFormattedDate(root.xpath('/TEI/text/body/div1/head/date/@value')[0]).date().isoformat()

		titles = ( root.xpath('/TEI/text/body/div2/p/title/rs') + root.xpath('/TEI/text/body/div2/note/title/rs') if len(root.xpath('/TEI/text/body/div2/p/title/rs') + root.xpath('/TEI/text/body/div2/note/title/rs')) > 0 else root.xpath('/TEI/text/body/div2/p/title') + root.xpath('/TEI/text/body/div2/note/title') )
		output_card['mentions'] = []
		for t in titles:
			output_card['mentions'].append({ '@type': 'CreativeWork', 'name': t.xpath('normalize-space(.)') })
#		output_card['mentions'] = [ { '@type': 'CreativeWork', 'title': x } for x in ( root.xpath('/TEI/text/body/div2/p/title/rs[normalize-space()]') + root.xpath('/TEI/text/body/div2/note/title/rs[normalize-space()]') if len(root.xpath('/TEI/text/body/div2/p/title/rs[normalize-space()]') + root.xpath('/TEI/text/body/div2/note/title/rs[normalize-space()]')) > 0 else root.xpath('/TEI/text/body/div2/p/title[normalize-space()]') + root.xpath('/TEI/text/body/div2/note/title[normalize-space()]') ) ]
		output_card['mentions'] += [ { '@type': 'Person', '@id': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + x } for x in root.xpath('/TEI/text/body/div2/p/name/@key') + root.xpath('/TEI/text/body/div2/note/name/@key') if x in linked_names[0] ]
		print(output_card['mentions'])
		if len(output_card['mentions']) == 1:
			output_card['mentions'] = output_card['mentions'][0]
		elif len(output_card['mentions']) == 0:
			del output_card['mentions']

		if 'mentions' in output_card:
			print(output_card['mentions'])

		output_card['citation'] = [ generateBibCitation(y,linked_names,tei_file) for y in root.xpath('//div2/bibl') + root.xpath('//div2/p/bibl') + root.xpath('//div2/note/bibl') ]
		print(output_card['citation'])
		output_card['citation'] = [ z for z in output_card['citation'] if len(z) > 0 ]
		if len(output_card['citation']) == 1:
			output_card['citation'] = output_card['citation'][0]
		elif len(output_card['citation']) == 0:
			del output_card['citation']

		if 'citation' in output_card:
			print(output_card['@id'])
	else:
		#chronology
		output_card['@type'] = 'Dataset'
		output_card['author'] = { '@type': 'Person', '@id': 'http://viaf.org/viaf/44300868'}
		output_card['name'] = 'Chronologie'
		output_card['temporalCoverage'] = getDate(root,'//head/date/')
		if not output_card['temporalCoverage']:
			del output_card['temporalCoverage']
#		if root.xpath('//head/date/@value'):
#			output_card['temporalCoverage'] = readFormattedDate(root.xpath('//head/date/@value')[0]).date().isoformat()
#		elif root.xpath('//head/date/@when'):
#			output_card['temporalCoverage'] = readFormattedDate(root.xpath('//head/date/@when')[0]).date().isoformat()
		
		titles = root.xpath('//div1//p/title') + root.xpath('//div1//note/title')
		print(titles)
		output_card['mentions'] = []
		for t in titles:
			output_card['mentions'].append({ '@type': 'CreativeWork', 'name': t.xpath('normalize-space(.)') })
#			print(t.xpath('normalize-space(.)'))
#		output_card['mentions'] = [ { '@type': 'CreativeWork', 'title': x } for x in root.xpath('//div1//p/title[normalize-space(.)]') + root.xpath('//div1//note/title[normalize-space(.)]') ]
		output_card['mentions'] += [ { '@type': 'Person', '@id': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + x } for x in root.xpath('//div1//p/name/@key') + root.xpath('//div1//note/name/@key') if x in linked_names[0] ]
#		output_card['mentions'] += [ { '@type': 'Person', '@id': 'catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + linked_names[0][linked_names[1].index(x)] } for x in root.xpath('//div1//p/name/text()') + root.xpath('//div1//note/name/text()') if x in linked_names[1] ]
		print("MENTIONS")
		print(output_card['mentions'])
		if len(output_card['mentions']) == 1:
			output_card['mentions'] = output_card['mentions'][0]
		elif len(output_card['mentions']) == 0:
			del output_card['mentions']

		output_card['citation'] = [ generateChronologyCitation(y,linked_names,tei_file) for y in root.xpath('//div1//bibl') ]
		output_card['citation'] = [ z for z in output_card['citation'] if len(z) > 0 ]
		if len(output_card['citation']) == 1:
			output_card['citation'] = output_card['citation'][0]
		elif len(output_card['citation']) == 0:
			del output_card['citation']

		if 'citation' in output_card:
			print(tei_file)

	return json.dumps(output_card,indent=4,ensure_ascii=False).encode('utf-8')

def makeOutputFolder(folder_name,counter):
	try:
		if counter is not None:
			write_folder_name = folder_name + ' (' + str(counter) + ')'
		else:
			write_folder_name = folder_name

		write_folder = os.mkdir(write_folder_name)
		return write_folder, write_folder_name
	except OSError:
		if counter is not None:
			return makeOutputFolder(folder_name,counter+1)
		else:
			return makeOutputFolder(folder_name,0)

def writeNewFile(file_path,copy=False,file_contents=None):
	path_elements = file_path.split(SLASH)
#	print(path_elements)

	built_path = path_elements[0] + SLASH

	for index in range(1,len(path_elements)-1):
		if not os.path.exists(built_path + path_elements[index]):
			os.makedirs(built_path + path_elements[index])

		built_path += path_elements[index] + SLASH

	if copy:
		copyfile('tei'+file_path[file_path.find(SLASH):],file_path)
	elif file_contents:
		with open(file_path,'w') as writefile:
			writefile.write(file_contents)

def addJournalLinksToXML(file_name):
	with open(file_name,'rb') as infile:
		card = infile.read()

	root = etree.fromstring(card)
	bibls = root.xpath('//bibl')
	for bibl in bibls:
		titles = bibl.xpath('.//title/text()')
		text_data = bibl.xpath('normalize-space(.)')
		date_published = extractDateFromText(text_data)

		if date_published and len(titles) > 0:
			processed_names = [ x.strip() for x in titles ]
			normalized_names = [ normalize('NFC',y.encode('utf-8').decode('utf-8').strip()) for y in processed_names ]
			
			link = None
			if 'Figaro' in processed_names or 'Le Figaro' in processed_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb34355551z/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'Gaulois' in processed_names or 'Le Gaulois' in processed_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb32779904b/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'Journal des Debats' in processed_names or 'Le Journal des Debats' in processed_names or normalize('NFC',u'Journal des Débats') in normalized_names or normalize('NFC',u'Le Journal des Débats') in normalized_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb39294634r/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'Echo de Paris' in processed_names or 'Écho de Paris' in processed_names or "L'Echo de Paris" in processed_names or normalize('NFC',u'Écho de Paris') in normalized_names or normalize('NFC',u"L'Echo de Paris") in normalized_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb34429768r/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'Gil Blas' in processed_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb344298410/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'Le Temps' in processed_names or 'Temps' in processed_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb34431794k/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'La Presse' in processed_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb34448033b/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'Chronique des Arts et de la Curiosité' in processed_names or 'Chroniques des Arts et de la curiosité' in processed_names or 'Voir Chronique des Arts et de la curiosité' in processed_names or 'Chronique des Arts et de la curiosité' in processed_names or normalize('NFC',u'Chronique des Arts et de la Curiosité') in normalized_names or normalize('NFC',u'Chroniques des Arts et de la curiosité') in normalized_names or normalize('NFC',u'Voir Chronique des Arts et de la curiosité') in normalized_names or normalize('NFC',u'Chronique des Arts et de la curiosité') in normalized_names:
				link = 'http://gallica.bnf.fr/ark:/12148/cb34421972m/date' + date_published[:4] + date_published[5:7] + date_published[8:] + '.item'
			elif 'The New York Herald' in processed_names or 'New York Herald' in processed_names:
				link = 'http://fultonhistory.com/my%20photo%20albums/All%20Newspapers/New%20York%20NY%20Herald/New%20York%20NY%20Herald%20' + date_published[:4] + '/index.html'

			if link:
				ref = etree.Element('ref', target=link)
				ref.extend(bibl)
				bibl.append(ref)

	revised_string = etree.tostring(root, pretty_print=True, encoding='unicode')

	with open(file_name,'wb') as outfile:
		outfile.write(revised_string.encode('utf-8'))

def traverseFullTree(processorFunction,linked_names):
	rootdir = 'tei'
	results_folder, results_folder_name = makeOutputFolder('json',None)

	for root, dirs, files in os.walk(rootdir):
		for name in files:
			if '.xml' in name:
				if 'dc.xml' in name:
					writeNewFile(results_folder_name+root[3:]+SLASH+name,copy=True)
				else:
					writeNewFile(results_folder_name+root[3:]+SLASH+name,copy=True)
					addJournalLinksToXML(results_folder_name+root[3:]+SLASH+name)
					writeNewFile(results_folder_name+root[3:]+SLASH+name[:-3]+'json',file_contents=processorFunction(root+SLASH+name,linked_names))

def getNameData():
	linked_name_keys = []
	linked_names = []
	with open('KolbProustNameData.csv','rU') as readfile:
		headerReader = csv.reader(readfile)
		header = next(headerReader)
		name_reader = csv.DictReader(readfile,header,delimiter=',');
		for name in name_reader:
			linked_name_keys.append(name['KeyCode'])
			linked_names.append(name['FullName'])

	return [linked_name_keys, linked_names]

#On Windows, the Command Prompt doesn't know how to display unicode characters, causing it to halt when it encounters non-ASCII characters
def setupByOS():
	if os.name == 'nt':
		if sys.stdout.encoding != 'cp850':
		  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'replace')
		if sys.stderr.encoding != 'cp850':
		  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'replace')

def main():
	setupByOS()
#	with open('JournalLinks.csv','w') as outfile:
#		outfileWriter = csv.writer(outfile)
#		outfileWriter.writerow(['FILE',"LINK"])

	linked_names = getNameData()
	traverseFullTree(processTEIFile,linked_names)

main()