import csv

def outputResults(processed_results,rows,label_row):
	output_csvfile = open('results_Kolb-Proust-Name-Database-FamilyNames-New.csv','w')
	output_writer = csv.writer(output_csvfile)
	output_writer.writerow(label_row)

	for row in rows:
		if row[1] in processed_results:
			person_results = processed_results[row[1]]
			output_writer.writerow(row + [person_results['VIAF NAME'],person_results['VIAF NUMBER'],person_results['EN_WIKIPEDIA'],person_results['FR_WIKIPEDIA']])
		else:
			output_writer.writerow(row)
	
	output_csvfile.close()

def main():
	with open('KolbProustNameData_VIAF.csv','r') as processed_readfile:
		processed_reader = csv.reader(processed_readfile)

		processed_results = {}
		for row in processed_reader:
			if row[0] != 'FullName':
				processed_results[row[2]] = { 'VIAF NAME': row[27], 'VIAF NUMBER': row[28], 'EN_WIKIPEDIA': row[29], 'FR_WIKIPEDIA': row[30] }

	with open('Kolb-Proust-Name-Database-FamilyNames-New_Unicode.csv','r') as ann_readfile:
		ann_reader = csv.reader(ann_readfile)

		rows = []
		label_row = ['VIAF NAME','VIAF NUMBER','EN_WIKIPEDIA', 'FR_WIKIPEDIA']
		for row in ann_reader:
			if row[0] == 'FullName':
				label_row = row + label_row
			else:
				rows.append(row)

	outputResults(processed_results,rows,label_row)

main()