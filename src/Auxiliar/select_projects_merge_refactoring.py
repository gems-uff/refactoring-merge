#!/usr/bin/python3

import pygit2
from datetime import datetime
from datetime import date
import argparse
import logging
import subprocess
import json

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

refMiner_exec = "/mnt/c/Users/aoliv/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner"

def read_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as f:
        return json.load(f)

def write_json(data,file_name):			
	with open(file_name, 'w', encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)


def get_project_path_list(path_projects):	
	subprocess.call("ls -d " + path_projects + "* > path_projects_list.txt", shell=True)
	f = open("path_projects_list.txt",'r')
	return f.read().splitlines()

def contar_commits(path_projects):
	list_path_projects = get_project_path_list(path_projects)
	
	for project_path in list_path_projects:
		repo = pygit2.Repository(project_path)
		last_commit = repo[repo.head.target]		
		print(f"qtd commits - {project_path} :{len(list(repo.walk(last_commit.id)))}")

def analyse_projects(path_projects):	
	#try:	
				
		list_path_projects = get_project_path_list(path_projects)
		projects_evalueted = []		
		for project_path in list_path_projects:
			commit_visited = set()
			qty_commits = 0
			qty_merge_commits = 0
			qty_no_has_base_version_merge_commit = 0
			qty_no_fast_forward_merge_commit = 0
			start_time = datetime.now()	
			logger.info('Evalueted Project: ' + project_path)
			repo_path = pygit2.discover_repository(project_path)
			repo = pygit2.Repository(repo_path)			
			for branch_name in repo.branches:
				for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):							
					if commit.id not in commit_visited:																		
						qty_commits += 1
						commit_visited.add(commit.id)																	
						# is a merge commit?
						if len(commit.parents) == 2:
							qty_merge_commits +=1
							#Does it have base version?
							base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)							
							if not base_commit:
								qty_no_has_base_version_merge_commit +=1
							# is it a fast forward commit?
							else:
								no_ff_commit = commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex
								if not no_ff_commit:
									qty_no_fast_forward_merge_commit +=1

			project_data = 	{
								'project': project_path,
								'qtyCommits': qty_commits,
								'qtyMergeCommits': qty_merge_commits,
								'qty_no_has_base_version_merge_commit':qty_no_has_base_version_merge_commit,
								'qty_no_fast_forward_merge_commit': qty_no_fast_forward_merge_commit,
								'valids_merge_commit': qty_merge_commits - (qty_no_has_base_version_merge_commit + qty_no_fast_forward_merge_commit),
								'executed': 'false'
							}
			projects_evalueted.append(project_data)
		logger.info('Evaluation Elapsed time:' + str(datetime.now() - start_time))
		
		write_json(projects_evalueted,'projectsSelected.json')
	#except:
	#	logger.info("Error ...")
	
		
def init_analysis(path_projects):	
	start_time = datetime.now()	
	logger.info("Starting evaluation")		
	analyse_projects(path_projects)		
	#contar_commits(path_projects)
	logger.info("Finished evaluation")
	logger.info('Elapsed time:' + str(datetime.now() - start_time))

def main():
	parser = argparse.ArgumentParser(description='Select dataset projects')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--path", help="set the base path for git repositories")
	"""Exemplo
	./select_projects_merge_refactoring.py --path /mnt/c/Users/aoliv/RepositoriosEO1/
	"""
	args = parser.parse_args()	
	init_analysis(args.path)

if __name__ == '__main__':
	main()