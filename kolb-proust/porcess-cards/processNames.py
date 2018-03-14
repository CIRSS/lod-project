# -*- coding: utf-8 -*-
import os, json

if os.name == 'nt':
	SLASH = '\\'
else:
	SLASH = '/'

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

def outputTurtleFile(write_file,turtle_strings):
	with open(write_file,'a') as output_file:
		for turtle_string in turtle_strings:
			print turtle_string
			output_file.write(turtle_string.encode('utf-8'))

def buildNewOutput(output_directory):
	core_name = output_directory[output_directory.rfind('/')+1:]
	with open(output_directory + '/' + core_name + '.ttl.graph','w') as graph_write_file:
		graph_write_file.write('http://localhost:8890/DAV/')

	output_text = 'PREFIX schema: <http://schema.org/>\n\n'
	with open(output_directory + '/' + core_name + '.ttl','w') as write_file:
		write_file.write(output_text.encode('utf-8'))

	return output_directory + '/' + core_name + '.ttl'

def addPersonToTurtle(person):
	print(person)
	output_text = '\n<' + person['id'] + '>\n'
	output_text += '\ta\tschema:' + person['type'] + ' ;\n'
	output_text += '\tschema:name\t"' + person['name'].replace('"','\\"') + '" ;\n'

	if 'birthDate' in person:
		output_text += '\tschema:birthDate\t"' + person['birthDate'] + '"^^schema:Date ;\n'
	if 'deathDate' in person:
		output_text += '\tschema:deathDate\t"' + person['deathDate'] + '"^^schema:Date ;\n'
	if 'gender' in person:
		output_text += '\tschema:gender\t"' + person['gender'] + '" ;\n'
	if 'nationality' in person:
		output_text += '\tschema:nationality\t"' + person['nationality'] + '" ;\n'
	if 'description' in person:
		output_text += '\tschema:description\t"' + person['description'].replace('"','\\"') + '" ;\n'
	if 'jobTitle' in person:
		job_title_list = person['jobTitle'].replace('"','\\"').split(';')
		for jt in job_title_list:
			output_text += '\tschema:jobTitle\t"' + jt.strip() + '" ;\n'
	if 'givenName' in person:
		output_text += '\tschema:givenName\t"' + person['givenName'].replace('"','\\"') + '" ;\n'
	if 'familyName' in person:
		if type(person['familyName']) is list:
			for family_name in person['familyName']:
				output_text += '\tschema:familyName\t"' + family_name + '" ;\n'
		else:
			output_text += '\tschema:familyName\t"' + person['familyName'] + '" ;\n'
	if 'honorificPrefix' in person:
		output_text += '\tschema:honorificPrefix\t"' + person['honorificPrefix'] + '" ;\n'
	if 'sameAs' in person:
		if type(person['sameAs']) is list:
			for link in person['sameAs']:
				output_text += '\tschema:sameAs\t<' + link + '> ;\n'
		else:
			output_text += '\tschema:sameAs\t<' + person['sameAs'] + '> ;\n'
	if 'memberOf' in person:
		if type(person['memberOf']) is list:
			for link in person['memberOf']:
				output_text += '\tschema:sameAs\t<' + link + '> ;\n'
		else:
			output_text += '\tschema:memberOf\t<' + person['memberOf'] + '> ;\n'
	if 'spouse' in person:
		if type(person['spouse']) is list:
			for link in person['spouse']:
				output_text += '\tschema:spouse\t<' + link + '> ;\n'
		else:
			if ',' in person['spouse']:
				spouse_list = person['spouse'].split(',')
				for sp in spouse_list:
					if 'http' in sp:
						output_text += '\tschema:spouse\t<' + sp.strip() + '> ;\n'
					else:
						output_text += '\tschema:spouse\t<http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + sp.strip() + '> ;\n'
			else:
				output_text += '\tschema:spouse\t<' + person['spouse'] + '> ;\n'
	if 'children' in person:
		if type(person['children']) is list:
			for link in person['children']:
				output_text += '\tschema:children\t<' + link + '> ;\n'
		else:
			if ',' in person['children']:
				children_list = person['children'].split(',')
				for ch in children_list:
					if 'http' in ch:
						output_text += '\tschema:children\t<' + ch.strip() + '> ;\n'
					else:
						output_text += '\tschema:children\t<http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + ch.strip() + '> ;\n'
			else:
				output_text += '\tschema:children\t<' + person['children'] + '> ;\n'
	if 'parent' in person:
		if type(person['parent']) is list:
			for link in person['parent']:
				output_text += '\tschema:parent\t<' + link + '> ;\n'
		else:
			if ',' in person['parent']:
				parent_list = person['parent'].split(',')
				for pr in parent_list:
					if 'http' in pr:
						output_text += '\tschema:parent\t<' + pr.strip() + '> ;\n'
					else:
						output_text += '\tschema:parent\t<http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + pr.strip() + '> ;\n'
			else:
				output_text += '\tschema:parent\t<' + person['parent'] + '> ;\n'
	if 'sibling' in person:
		if type(person['sibling']) is list:
			for link in person['sibling']:
				output_text += '\tschema:sibling\t<' + link + '> ;\n'
		else:
			if ',' in person['sibling']:
				sibling_list = person['sibling'].split(',')
				for sb in sibling_list:
					if 'http' in sb:
						output_text += '\tschema:sibling\t<' + sb.strip() + '> ;\n'
					else:
						output_text += '\tschema:sibling\t<http://catalogdata.library.illinois.edu/lod/entities/Persons/kp/' + sb.strip() + '> ;\n'
			else:
				output_text += '\tschema:sibling\t<' + person['sibling'] + '> ;\n'

	output_text = output_text[:-2] + '.\n'

	return output_text

def traverseFullTree():
	rootdir = 'names'
	results_folder, results_folder_name = makeOutputFolder('name_ttl',None)

	names_converted = 1
	file_iterator = 1
	turle_strings = []
	specific_write_folder, specific_write_folder_name = makeOutputFolder(results_folder_name + '/' + str(file_iterator),None)

	write_file = buildNewOutput(specific_write_folder_name)
#	unique_fields = []

	for root, dirs, files in os.walk(rootdir):
		for name in files:
			with open(root+SLASH+name,'r') as readfile:
				data_string = ''
				for line in readfile:
					first_square_bracket = line.find('[')
					start_bound = line.find(':')+3
					if line.count('"') > 4 and (first_square_bracket == -1 or first_square_bracket > start_bound):
						end_bound = line.rfind('"')
						new_line = line[:start_bound] + line[start_bound:end_bound].replace('"','\\"') + line[end_bound:]
						data_string += new_line
					else:
						data_string += line

				data = json.JSONDecoder().decode(data_string)
#				for entry in data:
#					if entry not in unique_fields:
#						unique_fields.append(entry)

#	with open('name_fields.txt','w') as outfile:
#		for field in unique_fields:
#			outfile.write(field + '\n')


			if names_converted%1000 == 0:
				outputTurtleFile(write_file,turle_strings)
				file_iterator += 1
				turle_strings = []
				specific_write_folder, specific_write_folder_name = makeOutputFolder(results_folder_name + '/' + str(file_iterator),None)
				write_file = buildNewOutput(specific_write_folder_name)

			turle_strings.append(addPersonToTurtle(data))

			names_converted += 1

	outputTurtleFile(write_file,turle_strings)

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