from datetime import datetime
from datetime import timedelta
startTime = datetime.now()
from collections import Counter

from pygit2 import *
import os
import shutil
import argparse
import time
import traceback
import csv
import subprocess

def filter_repos_and_clone():
	with open('/Users/tayanemoura/Documents/git/merge-effort-mining/aux/selectedprojects.csv') as csv_file:

		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				#print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				if(int(row[5])>10000 and int(row[5])<20000 and row[0] != "ptmt/react-native-macos" and row[0] !="eugenp/tutorials"): 
					print(f'\t{row[0]} {row[1]} {row[5]} ')
					line_count += 1
					url = row[1]
					clone(url)
					time.sleep(60)

		print(f'Processed {line_count} lines.')


def write_csv(row):
	with open('cloned.csv', 'a') as csvFile:
	    writer = csv.writer(csvFile)
	    writer.writerow(row)

	csvFile.close()


def clone(path):


	git_command = "git clone " + path + ".git"

	output = " "

	try:
		output = subprocess.check_output([git_command], stderr=subprocess.STDOUT,shell=True)
	
	except: 
		output = "error"
	
	print(output)
	write_csv([path, output])

	return output


#def count_merge(commits):
#	merge_commits_count = 0
#
#	for commit in commits:
#		if (len(commit.parents)==2):
#			merge_commits_count+=1
#
#	return merge_commits_count
			
def main():
	filter_repos_and_clone()
	
if __name__ == '__main__':
	main()	

