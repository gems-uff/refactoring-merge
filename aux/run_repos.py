import logging

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
import ntpath


def select_repos():
	repos = []
	with open('merges_count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if(int(row[1])>500 and int(row[1])<28000): 
				line_count += 1
				repos.add(row[0])
				#run_script(path)

		print('Processed' + str(line_count))
	return repos

def run_script(path):
	global REPO_PATH
	repo = Repository(path)
	REPO_PATH = path
	commits = list(merge_commits({repo.branches[branch_name].peel() for branch_name in repo.branches}))
	logger.info("Starting project" + repo.workdir)
	commits_metrics = analyse(commits, repo, False, True)
	print(commits_metrics)
	logger.info("Total of merge commits analyzed: " + str(len(commits_metrics)))
	if(ERROR):
		logger.error("Completed with error!")

	logger.info(datetime.now() - startTime)
	logger.info("Finished project" + repo.workdir)



			
def main():
	selected_repos = select_repos()
	
if __name__ == '__main__':
	main()	

