#!/usr/bin/python3
# -*- coding: utf-8 -*-

#switch python versions: sudo update-alternatives --config python3

# Dicas:https://pypi.org/project/PyMySQL/
# https://pymysql.readthedocs.io/en/latest/user/examples.html

# Execução programa  = sudo ./mining_refactoring_merge.py --repo_path /mnt/c/Users/aoliv/RepositoriesGiHub/refactoring-toy-example/

import pygit2
from datetime import datetime
from datetime import date
import argparse
import logging
from collections import Counter
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = logging.FileHandler(r'merge_commits_extract_db.log')

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s : %(message)s')
fh.setFormatter(formatter)
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)
		

def init_analysis(path_repository,merge_commit_sha1):		
	
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)
	merge_commit = repo.get(merge_commit_sha1)							
	print("PAI-1")
	print(merge_commit.parents[0].hex)
	print("PAI-2")
	print(merge_commit.parents[1].hex)
	common_ancestor = repo.merge_base(merge_commit.parents[0].hex, merge_commit.parents[1].hex)
	ca = repo.get(common_ancestor)
	print(f"ANCESTRAL COMUM - {common_ancestor} = {datetime.fromtimestamp(ca.commit_time)}")	

def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis - Refactoring')	
	parser.add_argument("--repo_path", help="set a path to local git repository")		
	parser.add_argument("--merge", help="set sha1 merge commit")		

	# Example
	# ./discovery_common_ancestor.py --repo_path /mnt/c/Users/aoliv/RepositoriosEO1/ExoPlayer --merge 16bf7f9106258eb92f66dbaedff39b28e21ae0fb

	args = parser.parse_args()	
	init_analysis(args.repo_path, args.merge)

if __name__ == '__main__':
	main()