# -*- coding: utf-8 -*-
import os
from shutil import copyfile

if os.name == 'nt':
	SLASH = '\\'
else:
	SLASH = '/'

def writeNewFile(file_path):
	path_elements = file_path.split(SLASH)
#	print(path_elements)

	built_path = path_elements[0] + SLASH

	for index in range(1,len(path_elements)-1):
		if not os.path.exists(built_path + path_elements[index]):
			os.makedirs(built_path + path_elements[index])

		built_path += path_elements[index] + SLASH

	copyfile('tei'+file_path[file_path.find(SLASH):],file_path)

def traverseFullTree():
	rootdir = 'json'
	results_folder_name = 'tei'

	for root, dirs, files in os.walk(rootdir):
		for name in files:
			if '.json' in name:
				source_file = rootdir+root[4:]+SLASH+name
				target_file = results_folder_name+root[4:]+SLASH+name
				print(source_file)
				print(target_file)
				copyfile(source_file,target_file)
#				writeNewFile(results_folder_name+root[3:]+SLASH+name,copy=True)

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