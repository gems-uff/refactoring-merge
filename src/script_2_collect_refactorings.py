#!/usr/bin/python3
# -*- coding: utf-8 -*-

#switch python versions: sudo update-alternatives --config python3

# Dicas:https://pypi.org/project/PyMySQL/
# https://pymysql.readthedocs.io/en/latest/user/examples.html


from ctypes import sizeof
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

"""fh = logging.FileHandler(r'merge_commits_extract_db.log')"""

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s : %(message)s')
"""fh.setFormatter(formatter)"""
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
"""logger.addHandler(fh)"""


REFMINER_TIMEOUT = 6000 # 5 min = 300

def read_json(arq_json):	
	my_file = Path(arq_json)
	result = []
	if my_file.exists():		
		with open(arq_json, 'r', encoding='utf8') as f:
			return json.load(f)
	else:
		return result

def open_connection_db(database_name):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database= database_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection

def has_duplicated_refac_in_merge(connection_bd, merge_sha1, project_seq, type_refac, description_refac, leftSideLocations, rightSideLocations):
	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT r.type from refactoring r, commit c, project p where p.id = c.id_project and c.id = r.id_commit and p.id=%s and r.type=%s and r.description=%s and CAST(r.leftSideLocations AS JSON)=CAST(%s AS JSON) and CAST(r.rightSideLocations AS JSON)=CAST(%s AS JSON) and c.sha1!=%s",(str(project_seq), type_refac, description_refac, json.dumps(leftSideLocations), json.dumps(rightSideLocations), merge_sha1))
		rows = cursor.fetchall()		
	if rows:			
		if(printlog):
			logger.info("######## Duplicated refactoring in merge commit " + merge_sha1 + " - found the same refactoring in the branches")
		return True
	else:
		if(printlog):
			logger.info("Has specific refactoring in the merge commit - " + merge_sha1 + " - " + description_refac)			
		return False


def get_refactoring_commit(path_repository,commit_sha1,name_arq):		
	""" /mnt/c/Users/aoliv/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner -c /mnt/c/Users/aoliv/RepositoriosEO1/spring-boot/ 49525b0a83e7809a603f420d807b433b268dd2b4 -json teste1.json"""
	commit = []	
	try:
		subprocess.run([refMiner_exec, "-c", path_repository, str(commit_sha1), "-json", name_arq],
					timeout=REFMINER_TIMEOUT, capture_output=True) #timeout = 2 hours
		retorno_arq = read_json(name_arq)		
		commit = retorno_arq['commits']
		if len(commit) > 0:
			return (commit[0]['refactorings'], False)
		else:			
			return (commit, False)
	except:	
		if(printlog):
			logger.info("Refatoring Miner Timeout: " + commit_sha1)		
		return (commit, True)
	finally:
		subprocess.run(["rm", name_arq], capture_output=True)

		
def save_refactoring_commit(repo, connection_bd, commit_sha1, commit_seq, project_seq, is_merge_commit,name_arq):	
	(refactorings_list, refminer_timeout) = get_refactoring_commit(repo.workdir, commit_sha1,name_arq)	
	for refactoring in refactorings_list:
		save_refac = True
		if(is_merge_commit):
			duplicated_refac = has_duplicated_refac_in_merge(connection_bd, commit_sha1, project_seq, refactoring['type'], refactoring['description'][:1000],refactoring['leftSideLocations'],refactoring['rightSideLocations'])
			if(duplicated_refac):
				save_refac = False
		
		#print(json.dumps(refactoring['leftSideLocations']))
		#print(json.dumps(refactoring['rightSideLocations']))
		
		if(save_refac):
			with connection_bd.cursor() as cursor:
				sql = "INSERT INTO refactoring (id, type, description, leftSideLocations, rightSideLocations, id_commit) VALUES (%s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (None, refactoring['type'], refactoring['description'][:1000], json.dumps(refactoring['leftSideLocations']), json.dumps(refactoring['rightSideLocations']), commit_seq))
		
	return (len(refactorings_list), refminer_timeout)


def get_commit_by_seq(connection_bd, commit_seq):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT * FROM commit where id=%s", commit_seq)
		commit = cursor.fetchone()
	return commit['sha1']

	
def find_project_in_db(connection_bd, path_workdir):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id, exec_script_branches, exec_script_refactorings FROM project where project.path_workdir = %s", path_workdir)
		row = cursor.fetchone()	
	if row:
		return row['id'], eval(row['exec_script_branches']), eval(row['exec_script_refactorings'])
	else:
		return False, False, False
	

def has_refactorings_by_sha1(connection_bd,commit_sha1):		
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT c.id FROM commit c, refactoring r where c.id = r.id_commit and c.sha1=%s",commit_sha1)
		rows = cursor.fetchall()		
	if rows:		
		return rows[0]['id']
	else:
		return False

def set_refminer_data_in_commit(connection_bd, sha1,refminer_timeout):
	rft = 'False'
	if(refminer_timeout):
		if(printlog):
				logger.info("## Refminer timeout in commit: " + str(sha1))
		rft = 'True'		
	
	with connection_bd.cursor() as cursor:
			sql = "UPDATE commit SET refminer_timeout = %s, refminer_execute = 'True' where sha1=%s"
			cursor.execute(sql,(rft,sha1))

def update_table_project(connection_bd, id_project):
	with connection_bd.cursor() as cursor:
			sql = "UPDATE project SET date_time_end_exec = CURRENT_TIMESTAMP, exec_script_refactorings = 'True' where id = %s"
			cursor.execute(sql,id_project)


def is_merge_commit(connection_bd, sha1):
	with connection_bd.cursor() as cursor:
		sql = "select count(*) as total from commit c, merge_commit mc where c.id = mc.id_commit and sha1 = %s";
		cursor.execute(sql,str(sha1))
		rows = cursor.fetchall()
		total = rows[0]['total']
		if(total == 1):
			return True
		else:
			return False


def delete_refacs_to_retry_refminer(connection_bd, id_project):
	sql = "delete from refactoring where id_commit in (select c.id from commit c, project p where c.refminer_timeout = 'True' and c.id_project = p.id and p.id = %s)"
	with connection_bd.cursor() as cursor:
		cursor.execute(sql,id_project)

def get_list_of_pending__refminer_commits(connection_bd, id_project, retry):	

	dict_pendings_commits = {}

	with connection_bd.cursor() as cursor:

		if not retry:		
			#including merge commits
			#sql = "select c.id, c.sha1 from commit c, project p where c.id_project = p.id and p.id = %s and c.refminer_execute = 'False' order by c.date_time asc;"
			#Excluding merge commits
			sql = "select c.id, c.sha1 from commit c, project p where c.id_project = p.id and p.id = %s and  c.refminer_execute = 'False' and c.id not in (select id_commit from merge_commit mc, commit c, project p where p.id = c.id_project and c.id = mc.id_commit and p.id = %s) order by c.date_time asc;"
		else:			
			delete_refacs_to_retry_refminer(connection_bd, id_project) #to avoid duplicate
			#including merge commits
			#sql = "select c.id, c.sha1 from commit c, project p where c.id_project = p.id and p.id = %s and (c.refminer_execute = 'False' or c.refminer_timeout = 'True') order by c.date_time asc;"
			#Excluding merge commits
			sql = "select c.id, c.sha1 from commit c, project p where c.id_project = p.id and p.id = %s and (c.refminer_execute = 'False' or c.refminer_timeout = 'True') and c.id not in (select id_commit from merge_commit mc, commit c, project p where p.id = c.id_project and c.id = mc.id_commit and p.id = %s) order by c.date_time asc;"

		cursor.execute(sql,(id_project,id_project))
		list_pending_refminer_commits = cursor.fetchall()		
		for commit in list_pending_refminer_commits:
			dict_pendings_commits[commit["sha1"]] = [commit["id"], is_merge_commit(connection_bd, commit["sha1"])]
			
	return dict_pendings_commits

def mining_repository(path_repository,refminer_path,name_arq,log=False, retry=False, database_name="refactoring_merge"):
		
	global refMiner_exec
	global printlog
	refMiner_exec = refminer_path
	printlog = log
	
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)
	
	connection_bd = open_connection_db(database_name)	
	start_time = datetime.now()
	
	
	if(repo.workdir):
		logger.info("Starting project" + repo.workdir)		
	else:
		logger.info("Error: Repositorie not identified")
		
	qty_refactoring_commit = 0
	
	pending_refminer_commits = {}
		
	try:		
		project_id, exec_script_branches, exec_script_refactorings = find_project_in_db(connection_bd, repo.workdir)
			
		if(exec_script_refactorings and not retry):
			logger.info("This script has already been run.")
			exit()

		if(not exec_script_branches):
			logger.info("ERROR: You first need execute the script_1_colllect_branches.py script.")
			exit()	
		
		pending_refminer_commits = get_list_of_pending__refminer_commits(connection_bd, project_id, retry)
		count_pending_commit = len(pending_refminer_commits)

		logger.info("## Number of refminer pending commits: " + str(len(pending_refminer_commits)))
		
		for sha1, commit_data in pending_refminer_commits.items():			
			if(printlog):
				logger.info("## Pending commits " + str(count_pending_commit))
			#call RefactoringMiner and save commit refactorings
			#commit_data[0] = id_commit and commit_data[1] = boolean (True if is merge commit)
			
			qty_refactoring_commit, refminer_timeout = save_refactoring_commit(repo, connection_bd, str(sha1), commit_data[0], project_id, commit_data[1], name_arq)
			set_refminer_data_in_commit(connection_bd, str(sha1), refminer_timeout)			
			if(printlog):
				if not commit_data[1]: #not is a merge commit
					logger.info("## Commit " + str(sha1) + " Refacs=" + str(qty_refactoring_commit))
				else:
					logger.info("## Merge Commit " + str(sha1) + " Refacs=" + str(qty_refactoring_commit))
			connection_bd.commit()
			count_pending_commit-=1
	
		#set end time execution			
		if(project_id):
			update_table_project(connection_bd, project_id)
			end_time = datetime.now() - start_time
			logger.info("Finished project " + repo.workdir)
			logger.info('Elapsed time:' + str(end_time))
		else:
			logger.info("ERROR: Project not found.")
		
	except TypeError as err:
		logger.info("Type Error: " + str(err))
		connection_bd.rollback()
	except pymysql.Error as mySqlErr:
		logger.info("Data base Error: " + str(mySqlErr))
		connection_bd.rollback()
	except Exception as ex:
		logger.info("General Error: " + str(ex))
		connection_bd.rollback()
	finally:				
		connection_bd.commit()
		connection_bd.close()
	

def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis - Refactoring')	
	parser.add_argument("--repo_path", help="set a path to local git repository")	
	parser.add_argument("--refminer_path", help="set a path to RefactoringMiner executable code")
	parser.add_argument("--arq_ref_miner", help="set the refmine results file name")
	parser.add_argument("--log", action='store_true', help="print log")
	parser.add_argument("--retry", action='store_true', help="retry execute")
	parser.add_argument("--database", default='refactoring_merge', help="database name.")
	

	# Example
	# ./script_2_collect_refactorings.py --log --repo_path /mnt/d/OpenSourceProjects/RxJava/ --refminer_path  /mnt/c/Users/aoliv/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner --arq_ref_miner ref_miner_rxjava.json --database db_refac_merge_os

	args = parser.parse_args()	

	mining_repository(args.repo_path, args.refminer_path, args.arq_ref_miner, args.log, args.retry, args.database)

if __name__ == '__main__':
	main()