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
import pymysql
from collections import Counter
import subprocess
import json
import sys
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

refMiner_exec = "/mnt/c/Users/aoliv/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner"
REFMINER_TIMEOUT = 1200 # 20 min

def read_json(arq_json):	
	my_file = Path(arq_json)
	result = []
	if my_file.exists():		
		with open(arq_json, 'r', encoding='utf8') as f:
			return json.load(f)
	else:
		return result

def write_json(data,file_name):			
	with open(file_name, 'w', encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)

def open_connection_db():
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='refactoring_merge',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection



def save_merge_attribute(repo, connection_bd, merge_commit, path_repository):		
	time_ini_me = datetime.now()
	#logger.info("Starting Merge Effort process - merge: "+str(merge_commit))	
	commit = repo.get(merge_commit)
	base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)		
	
	if base_commit:						
		has_base_version = 'True'
	else:
		has_base_version = 'False'
	
	with connection_bd.cursor() as cursor:			
		sql = "UPDATE merge_commit SET has_base_version = %s WHERE id_commit = (SELECT c.id from commit c, project p WHERE p.id = c.id_project and p.path_workdir=%s and c.sha1=%s)"
		cursor.execute(sql, (	
								has_base_version,
								path_repository,
								merge_commit
							)
		)
	connection_bd.commit()
	#logger.info('End Merge Effort process:' + str(datetime.now() - time_ini_me))

def get_unprocessed_merge_effort_commits(connection_bd,path_project):
	merge_commit_list = []
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT c.sha1 FROM project p, commit c, merge_commit m where p.id = c.id_project and c.id = m.id_commit and p.path_workdir=%s",path_project)
		rows = cursor.fetchall()		
		for row in rows:
			merge_commit_list.append(row['sha1'])
	return merge_commit_list


def execute_script(path_repository):	
	try:
		connection_bd = open_connection_db()
		start_time = datetime.now()
		end_time = datetime.now()
		repo_path = pygit2.discover_repository(path_repository)
		repo = pygit2.Repository(repo_path)		
		logger.info("Starting project" + repo.workdir)
		list_merge_unprocessed_effort = get_unprocessed_merge_effort_commits(connection_bd,path_repository)
		logger.info("Number of merge commit unprocessed: " + str(len(list_merge_unprocessed_effort)))
		
		for commit in list_merge_unprocessed_effort:
			save_merge_attribute(repo, connection_bd, commit, path_repository)
			
		end_time = datetime.now() - start_time		
	except TypeError as err:
		logger.info("Type Error: " + str(err))
		connection_bd.rollback()
	except pymysql.Error as mySqlErr:
		logger.info("Database Error: " + str(mySqlErr))
		connection_bd.rollback()	
	finally:				
		connection_bd.close()
		logger.info("Finished project " + repo.workdir)
		logger.info('Elapsed time:' + str(end_time))

def main():
	parser = argparse.ArgumentParser(description='Merge include atribute')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--repo_path", help="set a path for a local git repository")	
	args = parser.parse_args()	
	execute_script(args.repo_path)

	"""
		./APAGAR.py --repo_path /mnt/c/Users/aoliv/RepositoriesGiHub/refactoring-toy-example/
	"""

if __name__ == '__main__':
	main()