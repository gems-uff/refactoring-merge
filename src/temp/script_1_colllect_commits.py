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


def save_end_time_exec(connection_bd, id_project):
	with connection_bd.cursor() as cursor:
			sql = "UPDATE project SET date_time_end_exec = CURRENT_TIMESTAMP where id = %s"			
			cursor.execute(sql,id_project)


def open_connection_db(database_name):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database= database_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection

def save_merge_commit(repo, connection_bd, commit, commit_seq):	
	metrics = {}	
	has_base_version = True
	ff_commit = False
	base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)	
	# is fast forward commit?
	if(base_commit):
		ff_commit = commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex
	
	is_fast_forward_merge = False if ff_commit else True

	if not base_commit: # or str(commit.id) == '3d3acf07dddcf51ecf1adf07ce6e6d940d32d9a7' or str(commit.id) == '5357a39ec8cb511b254435107736ea50ce33e036':
		has_base_version = False
	metrics = {'extra':0, 'wasted':0, 'rework':0, 'branch1_actions':0, 'branch2_actions':0, 'merge_actions':0}
	merge_effort_calculated = False
	
	if not is_fast_forward_merge:
		with connection_bd.cursor() as cursor:
				sql = "INSERT INTO merge_commit (id, has_base_version, common_ancestor, parent1, parent2, is_fast_forward_merge, merge_effort_calculated, extra_effort, wasted_effort, rework_effort, branch1_actions, branch2_actions, merge_actions, id_commit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (	None,
										str(has_base_version),
										str(base_commit),
										str(commit.parents[0].id),			
										str(commit.parents[1].id),
										str(is_fast_forward_merge),
										str(merge_effort_calculated),
										metrics['extra'],
										metrics['wasted'],
										metrics['rework'],
										metrics['branch1_actions'],
										metrics['branch2_actions'],
										metrics['merge_actions'],
										commit_seq
									)
				)
				merge_commit_seq = connection_bd.insert_id()
		return merge_commit_seq
	else:
		return False

def save_commit(connection_bd, commit, project_seq):	
	with connection_bd.cursor() as cursor:
			sql = "INSERT INTO commit (id, sha1, author, message, commiter, date_time, is_merge_commit, parent, id_project) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (	None,
									str(commit.id),
								 	commit.author.name,
									commit.message[:500],
									commit.committer.name,
									datetime.fromtimestamp(commit.commit_time),
									str(len(commit.parents) == 2),
									str(commit.parents[0].id) if commit.parents else None,
									project_seq
								)
			)
			commit_seq = connection_bd.insert_id()
	return commit_seq


def find_project_in_db(connection_bd, path_workdir):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id FROM project where project.path_workdir = %s", path_workdir)
		row = cursor.fetchone()	
	if row:
		return row['id']	
	else:
		return False

def save_project(repo, connection_bd):		
	project_id = find_project_in_db(connection_bd, repo.workdir)
	if(not project_id):
		vetDir = str(repo.workdir).split('/')
		project_name = vetDir[len(vetDir)-2]
		with connection_bd.cursor() as cursor:
			sql = "INSERT INTO project (id, name, path_workdir, url, step) VALUES (%s, %s, %s, %s, %s)"
			cursor.execute(sql, (None, project_name, repo.workdir ,None,"collect_commit"))
			project_seq = connection_bd.insert_id()
		return project_seq
	else:		
		if(printlog):
			logger.info("ERROR: Project's "+ repo.workdir + " commits have already saved.")
			exit()
		return project_id
		#raise TypeError("Project " + repo.workdir + " have already processed")

def set_id_commits_processed(connection_bd,path_project):	
	with connection_bd.cursor() as cursor:
		cursor.execute("select c.id, c.sha1 from commit c, project p where c.id_project = p.id and p.path_workdir = %s",path_project)
		rows = cursor.fetchall()			
		for row in rows:
			cache_commit[str(row['sha1'])] = row['id']


def update_table_project(qty_commits, qty_merge_commits, qty_valid_merge_commits, id_project, connection_bd):
	with connection_bd.cursor() as cursor:
		sql = "UPDATE project SET number_commits = %s, number_merge_commits = %s, number_valid_merge_commits = %s where id = %s"
		cursor.execute(sql, (qty_commits, qty_merge_commits, qty_valid_merge_commits, id_project))
    

def mining_repository(path_repository,log=False,database_name="refactoring_merge"):	
	global printlog	
	printlog = log
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)

	connection_bd = open_connection_db(database_name)
	start_time = datetime.now()
	end_time = datetime.now()
	if(printlog):
		logger.info("Starting project" + repo.workdir)	
	qty_commits = 0
	qty_merge_commits = 0	
	qty_valid_merge_commits =0	
	commit_visited = set()	
	set_id_commits_processed(connection_bd,path_repository)
	if(printlog):
		logger.info("Commits already processed = " + str(len(cache_commit)))			
		
	try:
		project_seq = save_project(repo, connection_bd)		
		merge_list = []

		for branch_name in repo.branches:
			for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):						
				if str(commit.id) not in commit_visited:					
					
					commit_visited.add(str(commit.id))									
					commit_processed = str(commit.id) in cache_commit.keys()	

					qty_commits +=1

					#is a merge commit?
					is_merge_commit = False
					if len(commit.parents) == 2:						
						is_merge_commit = True
						if(printlog):
							logger.info("Merge Commit = " + str(commit.id) + " - " + str(datetime.fromtimestamp(commit.commit_time)))
						merge_list.append(commit)
						qty_merge_commits +=1

						#count valid merge commits
						base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
						if(base_commit):							
							if(commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex):
								qty_valid_merge_commits+=1
										
					if not commit_processed:  #commit not saved in database						
						if(printlog):
							logger.info("## Commit " + str(commit.id) + " - " + str(datetime.fromtimestamp(commit.commit_time)) + " was not processed")
						commit_seq = save_commit(connection_bd, commit, project_seq)
						cache_commit[str(commit.id)] = commit_seq #put commit db_sequence in cache				
						
						if is_merge_commit:
							save_merge_commit(repo, connection_bd, commit, commit_seq)
		
		
		update_table_project(qty_commits, qty_merge_commits, qty_valid_merge_commits, project_seq, connection_bd)
		#set end time execution
		save_end_time_exec(connection_bd, project_seq)
		
		end_time = datetime.now() - start_time
		
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
		if(printlog):
			logger.info("Finished project " + repo.workdir)
			logger.info('Elapsed time:' + str(end_time))

cache_merge = {}
cache_commit = {}
printlog = False


def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis - Refactoring')	
	parser.add_argument("--repo_path", help="set a path to local git repository")			
	parser.add_argument("--log", action='store_true', help="print log")
	parser.add_argument("--database", default='refactoring_merge', help="database name.")
	
	# Example	

	#./script_1_colllect_commits.py --repo_path /mnt/c/Users/aoliv/Repositorios_art2/netty/ --log --database banco_teste

	args = parser.parse_args()	
	mining_repository(args.repo_path, args.log, args.database)	

if __name__ == '__main__':
	main()