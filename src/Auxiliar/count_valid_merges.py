#!/usr/bin/python3
# -*- coding: utf-8 -*-

#switch python versions: sudo update-alternatives --config python3

# Dicas:https://pypi.org/project/PyMySQL/
# https://pymysql.readthedocs.io/en/latest/user/examples.html


import pygit2
import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s : %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def init_analysis(path_repository):			
	global printlog		
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)	
	qty_merge_commits = 0	
	qty_valid_merge_commits = 0		
	commit_visited = set()	
	
	for branch_name in repo.branches:
		for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):							
			if str(commit.id) not in commit_visited:					
				commit_visited.add(str(commit.id))
				#is a merge commit?				
				valid_commit_merge = False
				if len(commit.parents) == 2:						
					qty_merge_commits +=1 	
					base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
					if(base_commit):
						valid_commit_merge = commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex
					if(valid_commit_merge):
						qty_valid_merge_commits+=1

	logger.info("Number of commits = " + str(len(commit_visited)))
	logger.info("Number of merge commits = " + str(qty_merge_commits))
	logger.info("Number of valid merge commits = " + str(qty_valid_merge_commits))

def main():
	parser = argparse.ArgumentParser(description='Count Valid Merges')
	parser.add_argument("--repo_path", help="set a path to local git repository")	
	#Ex: ./count_valid_merges.py --repo_path /mnt/c/Users/aoliv/Repositorios_art2/mockito/ 
	args = parser.parse_args()	
	init_analysis(args.repo_path)

if __name__ == '__main__':
	main()