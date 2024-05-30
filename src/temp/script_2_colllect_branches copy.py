#!/usr/bin/python3
# -*- coding: utf-8 -*-

#switch python versions: sudo update-alternatives --config python3

# Dicas:https://pypi.org/project/PyMySQL/
# https://pymysql.readthedocs.io/en/latest/user/examples.html

# Execução programa  = sudo ./mining_refactoring_merge.py --repo_path /mnt/c/Users/aoliv/RepositoriesGiHub/refactoring-toy-example/

#from asyncio.windows_events import NULL
import pygit2
from datetime import datetime
from datetime import date
import argparse
import logging
import pymysql
from collections import Counter
import subprocess
import json
from pathlib import Path

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

def get_db_commit_seq_by_sha1(connection_bd, sha1):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id FROM commit where sha1=%s", sha1)
		row = cursor.fetchone()
	if row:
		return row['id']
	else:
		return False


def save_project_step_and_end_time_exec(connection_bd, id_project):
	with connection_bd.cursor() as cursor:
			sql = "UPDATE project SET date_time_end_exec = CURRENT_TIMESTAMP, step = 'collect_branches' where id = %s"
			cursor.execute(sql,id_project)


def open_connection_db(database_name):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database= database_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection


def find_project_in_db(connection_bd, path_workdir):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id, step FROM project where project.path_workdir = %s", path_workdir)
		row = cursor.fetchone()	
	if row:
		return row['id'], row['step'] 	
	else:
		return False, False


def get_list_commits_branch(repo, connection_bd, commit_evaluated, common_ancestor):	
	commit_list = []		
		
	if common_ancestor:	
		common_ancestor_obj = repo.get(common_ancestor)
		# ATENÇÃO: a segunda parte do while abaixo (depois do and) foi adicionado para resolver questões de ancestrais comuns um pouco confusos, como por exemplo do commit 6c0d2cb4c21d1d0c5fa1570f9d99b4927801e519 (quinta-feira, 27 de setembro de 2012 16:47:37) do projeto mockito
		while (str(commit_evaluated.id) != str(common_ancestor)) and (commit_evaluated.commit_time > common_ancestor_obj.commit_time):			
			
			is_merge_commit = len(commit_evaluated.parents) == 2	

			commit_seq = get_db_commit_seq_by_sha1(connection_bd, str(commit_evaluated.id))			
			commit_list.append(commit_seq)		
						
			if not is_merge_commit: 
				#go do the next commit in the branch
				if len(commit_evaluated.parents) > 0:					
					commit_evaluated = commit_evaluated.parents[0]									
				else: 
					break
			else:									
				# Append in commit_list the list of commits in the branch of this merge commit (only those has refactoring) - não usar, pois o script de coleta que está fazneo esse filtro
				"""list_append = get_db_list_commit_branches_merge(connection_bd, commit_evaluated)
				commit_list.extend(list_append)"""
								
				# follow to the common ancestor of this merge commit, if necessary
				if not ((str(commit_evaluated.parents[0].id) == str(common_ancestor))
					or (str(commit_evaluated.parents[1].id) == str(common_ancestor))):
					next_common_ancestor = repo.merge_base(commit_evaluated.parents[0].hex, commit_evaluated.parents[1].hex)
					
					if next_common_ancestor:						
						nca = repo.get(next_common_ancestor)
						ca = repo.get(common_ancestor)
						if(nca.commit_time > ca.commit_time):
							commit_evaluated = repo.get(next_common_ancestor)
						else:
							break
					else:
						break
				else:							
					break

	#print(commit_list)
	return commit_list

def save_commits_from_branch(connection_bd, merge_seq, commit_seq, type_branch):	
	# get commit id in database	
	
	with connection_bd.cursor() as cursor:
		sql = "INSERT INTO merge_branch (id, id_commit, id_merge_commit, type_branch) VALUES (%s, %s, %s, %s)"
		cursor.execute(sql, (None, commit_seq, merge_seq, type_branch))

def save_merge_branches(repo, connection_bd, merge_commit, merge_commit_seq):	
	common_ancestor = repo.merge_base(merge_commit.parents[0].hex, merge_commit.parents[1].hex)	
	
	"""#if str(merge_commit.id) == "9208854ef64240ebfb72e21e97e7434e8b60fbe8":
	print("====================================================")
	print(str(merge_commit.id))
	print("====================================================")"""

	# Save commit from branch 1	
	list_commit_seq_branch1 = get_list_commits_branch(repo, connection_bd, merge_commit.parents[0], common_ancestor)
	for commit_seq in list_commit_seq_branch1:		
		save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 1)

	##if str(merge_commit.id) == "9208854ef64240ebfb72e21e97e7434e8b60fbe8":	
	#print(f"L1 = {list_commit_seq_branch1}")
	#print("branch-1")
	#for c in list_commit_seq_branch1:
	#	a = repo.get(get_commit_by_seq(connection_bd,c))
	#	print(f"B1 - {a.id} = {datetime.fromtimestamp(a.commit_time)}")
	
	# Save commit from branch 2
	list_commit_seq_branch2 = get_list_commits_branch(repo, connection_bd, merge_commit.parents[1], common_ancestor)
	for commit_seq in list_commit_seq_branch2:
		save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 2)
	
	
	#if str(merge_commit.id) == "9208854ef64240ebfb72e21e97e7434e8b60fbe8":
	#print(f"L2 = {list_commit_seq_branch2}")
	#print("branch-2")	
	#for c in list_commit_seq_branch2:
	#	a = repo.get(get_commit_by_seq(connection_bd,c))
	#	print(f"B2 - {a.id} = {datetime.fromtimestamp(a.commit_time)}")
	#print("====================================================")

def mining_repository(path_repository,log=False,database_name="refactoring_merge"):	
		
	global printlog	
	printlog = log
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)
	connection_bd = open_connection_db(database_name)

	project_id, step = find_project_in_db(connection_bd, repo.workdir)
	
	if(step != "collect_commit" or step == "collect_branches"):
		logger.info("ERROR: This script has already been run, or you have not yet run the script 'script_1_colllect_commits.py'.")
		exit()
		
		
	start_time = datetime.now()
	
	if(printlog):
		logger.info("Starting project" + repo.workdir)			
		
	merge_commit_visited = set()
	try:
		for branch_name in repo.branches:
			for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):											
				#is a merge commit?
				is_merge_commit = False
				if len(commit.parents) == 2:						
					is_merge_commit = True
					base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
					# is fast forward commit?
					
					## TESTAR ESSA PARTE
					no_ff_commit = True
					if(base_commit):
						no_ff_commit = commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex
					
				if(is_merge_commit) and (base_commit) and (str(commit.id) not in merge_commit_visited) and no_ff_commit:
					merge_commit_visited.add(str(commit.id))
					merge_commit_id = get_db_commit_seq_by_sha1(connection_bd, str(commit.id))
					save_merge_branches(repo, connection_bd, commit, merge_commit_id)					
				
		if(project_id):
			save_project_step_and_end_time_exec(connection_bd, project_id)
			end_time = datetime.now() - start_time
		else:
			print("Project not found")
		
	#except TypeError as err: #ANDRE DESCOMENTAR
	#	logger.info("Type Error: " + str(err))
	#	connection_bd.rollback()
	#except pymysql.Error as mySqlErr:
	#	logger.info("Data base Error: " + str(mySqlErr))
	#	connection_bd.rollback()
	#except Exception as ex: #ANDRE DESCOMENTAR
	#	logger.info("General Error: " + str(ex))
	#	connection_bd.rollback()
	finally:				
		connection_bd.commit()
		connection_bd.close()
		end_time = datetime.now()
		if(printlog):
			logger.info("Finished project " + repo.workdir)
			logger.info('Elapsed time:' + str(end_time))

printlog = False

def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis - Refactoring')	
	parser.add_argument("--repo_path", help="set a path to local git repository")			
	parser.add_argument("--log", action='store_true', help="print log")
	parser.add_argument("--database", default='refactoring_merge', help="database name.")
	
	# Example	

	args = parser.parse_args()	
	mining_repository(args.repo_path, args.log, args.database)	

if __name__ == '__main__':
	main()