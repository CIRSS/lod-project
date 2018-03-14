# -*- coding: utf-8 -*-
import csv, os, re
from lxml import etree

def findFullCard(tei_id):
	rootdir = 'tei'

	for root, dirs, files in os.walk(rootdir):
		files = []

#		print(tei_id)

		if tei_id[0] == 'c' or tei_id[0] == 'C':
#			print("HERE")
#			print(root)
			if (root == 'tei'):
				dirs[:] = [d for d in dirs if not re.match(r'(s|p)+[0-9].+',d)]
			else:
				dirs[:] = [d for d in dirs if tei_id in d]

#			print("HERE")
#			dirs[:] = [d for d in dirs if not re.match(r'c?[0-9].+',d)]
		else:
#			print("THERE")
#			print(root)
			if (root == 'tei'):
				dirs[:] = [d for d in dirs if not re.match(r'c?[0-9].+',d)]
			else:
				dirs[:] = [d for d in dirs if tei_id in d]

#			print("THERE")
#			dirs[:] = [d for d in dirs if not re.match(r'(s|p)+[0-9].+',d)]
#		print(dirs)
#		print(root)

		if tei_id in root:
#			print(tei_id, root, dirs, files)
			return root + '\\' + root[root.rfind('\\'):] + '.xml'

def processFullCard(tei_id,journal):
	full_card_location = findFullCard(tei_id)
	print(full_card_location)
	with open(full_card_location,'r') as card:
		tree = etree.parse(card)
		titles = tree.xpath('//bibl[title = "' + journal + '"]')
		for title in titles:
			title_text = etree.tostring(title,encoding="unicode")

			year_results = re.search(r'[12][890][0-9][0-9]',title_text)
			year = None
			if year_results:
				year = year_results[0]

			month = None
			months = {' janvier ': '01',' février ': '02',' mars ': '03',' avril ': '04',' mai ': '05',' juin ': '06',' juillet ': '07',' août ': '08',' septembre ': '09',' octobre ': '10',' novembre ': '11',' décembre ': '12'}
			for mon in months.keys():
				if mon in title_text.lower():
					month = months[mon]

			thirty_one_day_re = r'( )?(1er|[1-9]|[12][0-9]|3[01]) '
			thirty_day_re = r'( )?(1er|[1-9]|[12][0-9]|30) '
			twenty_nine_day_re = r'( )?(1er|[1-9]|[12][0-9]) '

			day = None
			if month in ['01','03','05','07','08','10','12']:
				day_result = re.search(thirty_one_day_re,title_text)
			elif month in ['04','06','09','11']:
				day_result = re.search(thirty_day_re,title_text)
			else:
				day_result = re.search(twenty_nine_day_re,title_text)

			if day_result:
				day = day_result[0].strip(' ')
				if day == '1er':
					day = '01'
				elif len(day) == 1:
					day = '0' + day
#			else:
#				day = '00'

			if day and month and year:
#				print(day,month,year)
				return 'http://gallica.bnf.fr/ark:/12148/cb34355551z/date' + year + month + day + '.item'
			#print(etree.tostring(title))
#		print(titles)
#		print(etree.tostring(tree.getroot()))
#		print(card)

def writeResults(output_table):
	with open('JournalLinks.csv','w') as outfile:
		outfileWriter = csv.writer(outfile)

		for row in output_table:
			outfileWriter.writerow(row)

def addLinks(cardReader,output_table):
	for card in cardReader:
		if card['LEVEL'] == 'j':
			if card['TITLE'] == 'Figaro':
				generated_link = processFullCard(card['TEI ID'],card['TITLE'])
				new_row = [item for (label, item) in card.items()]
				new_row.append(generated_link)
				print(new_row)
				output_table.append(new_row)
			else:
				output_table.append([item for (label, item) in card.items()])
		else:
			output_table.append([item for (label, item) in card.items()])

	writeResults(output_table)

def main():
	output_table = []
	with open('KP TEI Titles.csv','r') as infile:
		headerReader = csv.reader(infile)
		header = next(headerReader)
		cardReader = csv.DictReader(infile,header,delimiter=',');

		output_table.append(header+['LINK'])

		addLinks(cardReader,output_table)

#	print(output_table)

main()