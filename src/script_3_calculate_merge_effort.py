#!/usr/bin/python3
# -*- coding: utf-8 -*-

#switch python versions: sudo update-alternatives --config python3

# Dicas:https://pypi.org/project/PyMySQL/
# https://pymysql.readthedocs.io/en/latest/user/examples.html


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
from timeout_decorator import timeout


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

"""fh = logging.FileHandler(r'merge_commits_extract_db.log')"""

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s : %(message)s')
"fh.setFormatter(formatter)"
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
"""logger.addHandler(fh)"""



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

def open_connection_db(database_name):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database=database_name,
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
		# context_lines - is the number of unchanged lines that define the boundary of a hunk (and to display before and after) 
		diff_base_final = repo.diff(base_version, merge_commit, context_lines=0)
		diff_base_parent1 = repo.diff(base_version, merge_commit.parents[0], context_lines=0)
		diff_base_parent2 = repo.diff(base_version, merge_commit.parents[1], context_lines=0)				
		merge_actions = get_actions(diff_base_final)
		parent1_actions = get_actions(diff_base_parent1)		
		parent2_actions = get_actions(diff_base_parent2)		
		metrics = calculate_metrics(merge_actions, parent1_actions, parent2_actions)		
	except:		
		logger.exception("ERROR: Unexpected error in commit " + str(merge_commit))
		error = True	
	if error:
		logger.error(f'ERROR: Project {repo} finished with error!')
	return metrics

#TIMEOUT  = 600 sec = 10 min
@timeout(seconds=6000, timeout_exception=StopIteration, exception_message="Timeout ERROR", use_signals=False)
def save_merge_effort_metrics(repo, connection_bd, merge_commit, path_repository):		
	time_ini_me = datetime.now()
	if(printlog):
		logger.info("Starting Merge Effort process - merge: "+str(merge_commit))
	metrics = {}
	commit = repo.get(merge_commit)	
	base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)		
	if base_commit:			
		metrics = analyze_merge_effort(commit, base_commit, repo)		
		if not metrics: #apenas uma proteção - o commit db53e5f7fe634aa0db9a012b2125782d76d66d63 do projeto intelliJ-community não retornou métricas. Avaliar
			metrics = {'extra':0, 'wasted':0, 'rework':0, 'branch1_actions':0, 'branch2_actions':0, 'merge_actions':0}				

	else:		
		metrics = {'extra':0, 'wasted':0, 'rework':0, 'branch1_actions':0, 'branch2_actions':0, 'merge_actions':0}

	with connection_bd.cursor() as cursor:			
		sql = "UPDATE merge_commit SET merge_effort_calculated='True', extra_effort = %s, wasted_effort = %s, rework_effort=%s, branch1_actions=%s, branch2_actions=%s, merge_actions=%s, merge_effort_calc_timeout='False' WHERE id_commit = (SELECT c.id from commit c, project p WHERE p.id = c.id_project and p.path_workdir=%s and c.sha1=%s)"		
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
	if(printlog):
		logger.info('End Merge Effort process:' + str(datetime.now() - time_ini_me))


def set_timeout_false_no_ff_merge_commit(connection_bd, id_project):
	with connection_bd.cursor() as cursor:
		sql = "UPDATE merge_commit SET merge_effort_calc_timeout='False' WHERE is_fast_forward_merge = 'True' and id_commit in (SELECT c.id from commit c, project p WHERE p.id = c.id_project and p.id = %s)"
		cursor.execute(sql,id_project)
	connection_bd.commit()

def get_unprocessed_merge_effort_commits(connection_bd,path_project, retry):
	merge_commit_list = []
	if(not retry):		
		sql = "SELECT c.sha1 FROM project p, commit c, merge_commit mc where p.id = c.id_project and c.id = mc.id_commit and mc.is_fast_forward_merge = 'False' and mc.merge_effort_calculated = 'False' and p.path_workdir=%s"
	else:
		sql = "SELECT c.sha1 FROM project p, commit c, merge_commit mc where p.id = c.id_project and c.id = mc.id_commit and mc.is_fast_forward_merge = 'False' and (mc.merge_effort_calculated = 'False' or mc.merge_effort_calc_timeout = 'True') and p.path_workdir=%s"

	with connection_bd.cursor() as cursor:
		cursor.execute(sql,path_project)
		rows = cursor.fetchall()		
		for row in rows:
			merge_commit_list.append(row['sha1'])
		
	return merge_commit_list


def find_project_in_db(connection_bd, path_workdir):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id, exec_script_branches, exec_script_merge_effort FROM project where project.path_workdir = %s", path_workdir)
		row = cursor.fetchone()	
	if row:
		return row['id'], eval(row['exec_script_branches']), eval(row['exec_script_merge_effort'])
	else:
		return False, False, False


def update_table_project(connection_bd, id_project):
	with connection_bd.cursor() as cursor:
			sql = "UPDATE project SET date_time_end_exec = CURRENT_TIMESTAMP, exec_script_merge_effort = 'True' where id = %s"
			cursor.execute(sql,id_project)


def calculate_merge_effort(path_repository,log=False,retry=False, database_name="refactoring_merge"):	
	
	global printlog	
	printlog = log
	
	start_time = datetime.now()		
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)	
	
	try:
		connection_bd = open_connection_db(database_name)
				
		project_id, exec_script_branches, exec_script_merge_effort = find_project_in_db(connection_bd, repo.workdir)
		
		if(exec_script_merge_effort and not retry):
			logger.error("This script has already been run.")
			exit()

		if(not exec_script_branches):
			logger.error("ERROR: You first need execute the script_1_colllect_branches.py script.")
			exit()

		
		logger.info("Starting project" + repo.workdir)	
		logger.info('Elapsed time:' + str(start_time))
		
		list_merge_unprocessed_effort = get_unprocessed_merge_effort_commits(connection_bd,path_repository, retry)		
		
		#set timeout false in --no-ff merge commits - won't be computed
		set_timeout_false_no_ff_merge_commit(connection_bd, project_id)
		
		number_pending_merge_commits = len(list_merge_unprocessed_effort)
		logger.info("Number of merge commit unprocessed: " + str(number_pending_merge_commits))
		
		for commit in list_merge_unprocessed_effort:
			if(printlog): 
				logger.info("Number of merge commit unprocessed: " + str(number_pending_merge_commits))				
			try:				
				if(str(commit) != "398cf997b3dfc415520d9c56e0bc1a49e4473bee"): #TIRAR
					save_merge_effort_metrics(repo, connection_bd, commit, path_repository)				
			except StopIteration as errorTimeout:
				if(printlog): 
					logger.info("ERROR: Timeout during merge effort calculation.")
			

			number_pending_merge_commits-=1

		if(project_id):			
			update_table_project(connection_bd, project_id)
			end_time = datetime.now() - start_time
			logger.info("Finished project " + repo.workdir)
			logger.info('Elapsed time:' + str(end_time))
		else:
			logger.error("ERROR: Project not found.")
							
	except TypeError as err:
		logger.exception("Type Error: " + str(err))
		connection_bd.rollback()
	except pymysql.Error as mySqlErr:
		logger.exception("Database Error: " + str(mySqlErr))
		connection_bd.rollback()	
	finally:				
		connection_bd.commit()
		connection_bd.close()			
		

def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--repo_path", help="set a path for a local git repository")	
	parser.add_argument("--log", action='store_true', help="print log")
	parser.add_argument("--retry", action='store_true', help="retry execute")	
	parser.add_argument("--database", default='refactoring_merge', help="database name.")

	# ./script_3_calculate_merge_effort.py --repo_path /mnt/c/Users/aoliv/Repositorios_art2/netty/ --log --database banco_teste

	args = parser.parse_args()		

	calculate_merge_effort(args.repo_path,args.log, args.retry, args.database)


if __name__ == '__main__':
	main()