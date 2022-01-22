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


def calculate_rework(parent1_actions, parent2_actions):
	rework_actions = parent1_actions & parent2_actions
	return (sum(rework_actions.values()))

def calculate_wasted_effort(parents_actions, merge_actions):
	wasted_actions = parents_actions - merge_actions

	return (sum(wasted_actions.values()))

def calculate_additional_effort(parents_actions, merge_actions):
	additional_actions = merge_actions - parents_actions
	return (sum(additional_actions.values()))

def calculate_metrics(merge_actions, parent1_actions, parent2_actions):
	metrics = {}		
	parents_actions = parent1_actions + parent2_actions	
	sum_parents_actions = sum(parents_actions.values()) if sum(parents_actions.values()) > 0 else 1
	sum_merge_actions = sum(merge_actions.values()) if sum(merge_actions.values()) > 0 else 1	
	metrics['rework_n'] = calculate_rework(parent1_actions, parent2_actions)/sum_parents_actions
	metrics['wasted_n']  = calculate_wasted_effort(parents_actions, merge_actions)/sum_parents_actions
	metrics['extra_n'] =calculate_additional_effort(parents_actions, merge_actions)/sum_merge_actions
	metrics['branch1_actions'] = sum(parent1_actions.values())
	metrics['branch2_actions'] = sum(parent2_actions.values())
	metrics['merge_actions'] = sum(merge_actions.values())
	metrics['rework'] = calculate_rework(parent1_actions, parent2_actions)
	metrics['wasted']  = calculate_wasted_effort(parents_actions, merge_actions)
	metrics['extra'] = calculate_additional_effort(parents_actions, merge_actions)	
	return metrics

def get_actions(diff_a_b):
	actions = Counter()
	for d in diff_a_b:
		file_name = d.delta.new_file.path
		for h in d.hunks:
			for l in h.lines:
				actions.update([file_name+l.origin+l.content])
	return actions

def analyze_merge_effort(merge_commit, base, repo):
	error = False	
	metrics = {}
	try:
		base_version = repo.get(base)							
		diff_base_final = repo.diff(base_version, merge_commit, context_lines=0)
		diff_base_parent1 = repo.diff(base_version, merge_commit.parents[0], context_lines=0)
		diff_base_parent2 = repo.diff(base_version, merge_commit.parents[1], context_lines=0)				
		merge_actions = get_actions(diff_base_final)
		parent1_actions = get_actions(diff_base_parent1)
		parent2_actions = get_actions(diff_base_parent2)
		metrics = calculate_metrics(merge_actions, parent1_actions, parent2_actions)		
	except:
		print()
		logger.exception("Unexpected error in commit " + str(merge_commit))
		error = True	
	if error:
		logger.error(f'Project {repo} finished with error!')
	return metrics


def save_merge_effort_metrics(repo, connection_bd, merge_commit, path_repository):		
	time_ini_me = datetime.now()
	logger.info("Starting Merge Effort process - merge: "+str(merge_commit))
	metrics = {}
	commit = repo.get(merge_commit)	
	base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)		
	if base_commit:						
		metrics = analyze_merge_effort(commit, base_commit, repo)

	else:		
		metrics = {'extra':0, 'wasted':0, 'rework':0, 'branch1_actions':0, 'branch2_actions':0, 'merge_actions':0}

	with connection_bd.cursor() as cursor:			
		sql = "UPDATE merge_commit SET merge_effort_calculated='True', extra_effort = %s, wasted_effort = %s, rework_effort=%s, branch1_actions=%s, branch2_actions=%s, merge_actions=%s WHERE id_commit = (SELECT c.id from commit c, project p WHERE p.id = c.id_project and p.path_workdir=%s and c.sha1=%s)"
		cursor.execute(sql, (	
								metrics['extra'],
								metrics['wasted'],
								metrics['rework'],
								metrics['branch1_actions'],
								metrics['branch2_actions'],
								metrics['merge_actions'],
								path_repository,
								merge_commit
							)
		)
	connection_bd.commit()
	logger.info('End Merge Effort process:' + str(datetime.now() - time_ini_me))

def get_unprocessed_merge_effort_commits(connection_bd,path_project):
	merge_commit_list = []
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT c.sha1 FROM project p, commit c, merge_commit m where p.id = c.id_project and c.id = m.id_commit and m.merge_effort_calculated = 'False' and p.path_workdir=%s",path_project)
		rows = cursor.fetchall()		
		for row in rows:
			merge_commit_list.append(row['sha1'])
	return merge_commit_list


def calculate_merge_effort(path_repository):	
	try:
		connection_bd = open_connection_db()
		start_time = datetime.now()
		end_time = datetime.now()
		repo_path = pygit2.discover_repository(path_repository)
		repo = pygit2.Repository(repo_path)
		#### TEMP TIRAR ####
		"""merge_commit_list = []
		with connection_bd.cursor() as cursor:
			cursor.execute("SELECT c.sha1 FROM project p, commit c, merge_commit m where p.id = c.id_project and m.is_fast_forward_merge='True' and c.id = m.id_commit and p.path_workdir=%s",path_repository)
			rows = cursor.fetchall()		
			for row in rows:
				merge_commit_list.append(row['sha1'])
		
		print(len(merge_commit_list))

		for c in merge_commit_list:
			commit_merge = repo.get(c)	
			base_commit = repo.merge_base(commit_merge.parents[0].hex, commit_merge.parents[1].hex)
			ff_commit = commit_merge.parents[0].hex != base_commit.hex and commit_merge.parents[1].hex != base_commit.hex
			is_fast_forward_merge = False if ff_commit else True
			print(c)
			with connection_bd.cursor() as cursor:							
				sql = "UPDATE merge_commit SET is_fast_forward_merge=%s WHERE id_commit = (SELECT id from commit WHERE sha1=%s)"
				cursor.execute(sql,(str(is_fast_forward_merge),c))
			connection_bd.commit()		

		###################"""


		logger.info("Starting project" + repo.workdir)
		list_merge_unprocessed_effort = get_unprocessed_merge_effort_commits(connection_bd,path_repository)
		logger.info("Number of merge commit unprocessed: " + str(len(list_merge_unprocessed_effort)))
		
		for commit in list_merge_unprocessed_effort:
			save_merge_effort_metrics(repo, connection_bd, commit, path_repository)
			
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
	parser = argparse.ArgumentParser(description='Merge effort analysis')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--repo_path", help="set a path for a local git repository")	
	args = parser.parse_args()	
	calculate_merge_effort(args.repo_path)

	"""
		./extract_merge_effort.py --repo_path /mnt/c/Users/aoliv/RepositoriesGiHub/refactoring-toy-example/
	"""

if __name__ == '__main__':
	main()