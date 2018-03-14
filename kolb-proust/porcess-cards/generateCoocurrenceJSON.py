import csv, json, requests

def main():
	force_direct_output = { 'nodes': [], 'links': [] }

	id_indexes = []
	row_count = 0
	with open('coocurrences_family.csv','r') as infile:
		reader = csv.reader(infile)
		for row in reader:
#			print row[0]
			if row[0] == '':
				for index in range(1,len(row)):
					results = requests.get('http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + row[index]).content
					json_results = json.loads(results)
					id_indexes.append('http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + row[index])
					force_direct_output['nodes'].append({'id': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + row[index], 'name': json_results['name']})
			else:
				for index in range(row_count+1,len(row)):
					if row[index] != '':
						force_direct_output['links'].append({'source': 'http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + row[0], 'target': id_indexes[index-1], 'value': int(row[index]), 'name': force_direct_output['nodes'][row_count-1]['name'] + ' & ' + force_direct_output['nodes'][index-1]['name'] + ': ' + row[index]})

				if row[row_count] != '':
					force_direct_output['nodes'][row_count-1]['mention_count'] = int(row[row_count])
				else:
					force_direct_output['nodes'][row_count-1]['mention_count'] = 0

			row_count += 1

#	print force_direct_output
	with open('coocurrences_family.json','w') as outfile:
		json.dump(force_direct_output,outfile,indent=4)


main()