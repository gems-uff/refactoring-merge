#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Obs: We are storing all merge commits in the database, including those that: 
i) do not have a base commit
ii) were generated via --no-ff
"""

#switch python versions: sudo update-alternatives --config python3

# Dicas:https://pypi.org/project/PyMySQL/
# https://pymysql.readthedocs.io/en/latest/user/examples.html


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



def open_connection_db(database_name):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database= database_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection


def get_count_commits(connection_bd, id_project):	
	with connection_bd.cursor() as cursor:		
		cursor.execute("SELECT count(*) as total_commits FROM commit c, project p where c.id_project = p.id and p.id = %s",id_project)
		row = cursor.fetchone()
	if row:
		return row['total_commits']
	else:
		return False

def get_db_commit_seq_by_sha1(connection_bd, sha1):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id FROM commit where sha1=%s", sha1)
		row = cursor.fetchone()
	if row:
		return row['id']
	else:
		return False

def save_project_end_time_exec(connection_bd, id_project):
	with connection_bd.cursor() as cursor:
			sql = "UPDATE project SET date_time_end_exec = CURRENT_TIMESTAMP where id = %s"
			cursor.execute(sql,id_project)
	#connection_bd.commit()

def update_table_project(qty_commits, qty_merge_commits, qty_valid_merge_commits, qty_commits_refminer, id_project, connection_bd):
	with connection_bd.cursor() as cursor:
		sql = "UPDATE project SET date_time_end_exec = CURRENT_TIMESTAMP, exec_script_branches = 'True', number_commits = %s, number_merge_commits = %s, number_valid_merge_commits = %s, number_commits_refminer = %s where id = %s"
		cursor.execute(sql, (qty_commits, qty_merge_commits, qty_valid_merge_commits, qty_commits_refminer, id_project))


def find_project_in_db(connection_bd, path_workdir):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id, exec_script_branches FROM project where project.path_workdir = %s", path_workdir)
		row = cursor.fetchone()	
	if row:
		return row['id'], eval(row['exec_script_branches'])
	else:
		return False, False


def get_list_commits_branch(repo, connection_bd, commit_evaluated, common_ancestor, project_id, merge_commit_sha1):	
	commit_list = []		
	
	if common_ancestor:	
		common_ancestor_obj = repo.get(common_ancestor)
		# ATENÇÃO: a segunda parte do while abaixo (depois do and) foi adicionado para resolver questões de ancestrais comuns um pouco confusos, como por exemplo do commit 6c0d2cb4c21d1d0c5fa1570f9d99b4927801e519 (quinta-feira, 27 de setembro de 2012 16:47:37) do projeto mockito
		while (str(commit_evaluated.id) != str(common_ancestor)) and (commit_evaluated.commit_time > common_ancestor_obj.commit_time):			
			
			is_merge_commit = len(commit_evaluated.parents) == 2	
					
			#check if commit has already stored in database
			commit_id = get_db_commit_seq_by_sha1(connection_bd, str(commit_evaluated.id))
			if not commit_id:
				if is_merge_commit:					
					commit_id = save_merge_commit(repo, connection_bd, commit_evaluated, project_id)					
				else:					
					commit_id = save_commit(connection_bd, commit_evaluated, project_id)					

			
			if(commit_id):
				commit_list.append(commit_id)

			if str(commit_evaluated.id) == commit_teste: # TODO TIRAR
				print("PROCURADO")
				print(commit_id)

			if str(merge_commit_sha1) == commit_teste: # TODO TIRAR
				print(str(commit_evaluated.id))
				print(commit_id)
				print(is_merge_commit)
				print(commit_list)

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
						#print("entrou aqui")						
						#print(str(next_common_ancestor.hex))
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
	return commit_list


def save_commits_from_branch(connection_bd, merge_seq, commit_seq, type_branch, merge_commit_sha1):	
	with connection_bd.cursor() as cursor:
		sql = "INSERT INTO merge_branch (id, id_commit, id_merge_commit, type_branch) VALUES (%s, %s, %s, %s)"
		cursor.execute(sql, (None, commit_seq, merge_seq, type_branch))
		merge_branch_seq = connection_bd.insert_id()		
		#connection_bd.commit()
		return merge_branch_seq

def save_merge_commit(repo, connection_bd, commit, project_id):		
	
	common_ancestor = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
   		
	is_fast_forward_merge = False	   
	if common_ancestor:
		has_base_version = True
		no_ff = commit.parents[0].hex != common_ancestor.hex and commit.parents[1].hex != common_ancestor.hex		
		is_fast_forward_merge = False if no_ff else True
	else:		
		has_base_version = False		

	commit_id = save_commit(connection_bd, commit, project_id)		
	
	metrics = {'extra':0, 'wasted':0, 'rework':0, 'branch1_actions':0, 'branch2_actions':0, 'merge_actions':0}
	with connection_bd.cursor() as cursor:
		sql = "INSERT INTO merge_commit (id, has_base_version, common_ancestor, parent1, parent2, is_fast_forward_merge, merge_effort_calculated, extra_effort, wasted_effort, rework_effort, branch1_actions, branch2_actions, merge_actions, id_commit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(sql, (	None,
								str(has_base_version),						
								str(common_ancestor),						
								str(commit.parents[0].id),			
								str(commit.parents[1].id),
								str(is_fast_forward_merge),
								str(False),
								metrics['extra'],
								metrics['wasted'],
								metrics['rework'],
								metrics['branch1_actions'],
								metrics['branch2_actions'],
								metrics['merge_actions'],
								commit_id
							)
		)
		merge_commit_seq = connection_bd.insert_id()
		#connection_bd.commit()
	return commit_id #return id commit associeted to merge_commit 

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
		#connection_bd.commit()
	return commit_seq


def save_merge_branches(repo, connection_bd, merge_commit, project_id):	
    
	#check if merge_commit_has already saved	

	follow = False

	
	commit_id = get_db_commit_seq_by_sha1(connection_bd, str(merge_commit.id))
	if not commit_id:				
		merge_commit_seq = save_merge_commit(repo, connection_bd, merge_commit, project_id)		
		
		if str(merge_commit.id) == commit_teste: # TODO: TIRAR
			print("AQUI")
		
		if(merge_commit_seq):			
			follow = True		
				
	if follow:
		common_ancestor = repo.merge_base(merge_commit.parents[0].hex, merge_commit.parents[1].hex)	
		
		# Save commit from branch 1	
		list_commit_seq_branch1 = get_list_commits_branch(repo, connection_bd, merge_commit.parents[0], common_ancestor, project_id, str(merge_commit.id))
		
		if str(merge_commit.id) == commit_teste: #TODO: TIRAR
			print("###### Retorno Lista 1")
			print(list_commit_seq_branch1)
		
		if str(merge_commit.id) == commit_teste: #TODO: TIRAR
			print("###### Merge commit seq")
			print(merge_commit_seq)

		for commit_seq in list_commit_seq_branch1:		
			save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 1, str(merge_commit.id))

	
		# Save commit from branch 2
		list_commit_seq_branch2 = get_list_commits_branch(repo, connection_bd, merge_commit.parents[1], common_ancestor, project_id, str(merge_commit.id))
		
		if str(merge_commit.id) == commit_teste: #TODO: TIRAR
			print("###### Retorno Lista 2")
			print(list_commit_seq_branch2)
		
		for commit_seq in list_commit_seq_branch2:
			save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 2, str(merge_commit.id))

	else:
		if(printlog):
			logger.error("Error: " + str(merge_commit.id) + " - " + str(datetime.fromtimestamp(merge_commit.commit_time))+ " was not saved")
	

def save_project(repo, connection_bd):		
	project_id, exec_collect_branches = find_project_in_db(connection_bd, repo.workdir)	
	if(not project_id):
		vetDir = str(repo.workdir).split('/')
		project_name = vetDir[len(vetDir)-2]
		with connection_bd.cursor() as cursor:
			sql = "INSERT INTO project (id, name, path_workdir, url, exec_script_branches) VALUES (%s, %s, %s, %s, %s)"
			cursor.execute(sql, (None, project_name, repo.workdir, None, 'False'))
			project_seq = connection_bd.insert_id()
		return project_seq
	else:		
		if(printlog):
			logger.error("ERROR: Project's "+ repo.workdir + " commits have already saved.")
			exit()
		return project_id


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
		logger.info('Elapsed time:' + str(start_time))
		
	qty_commits = 0
	qty_merge_commits = 0	
	qty_valid_merge_commits = 0	
	commit_visited = set()	
	merge_commit_visited = set()
	
	try:
		project_id, exec_script_branches = find_project_in_db(connection_bd, repo.workdir)		
		
		if(exec_script_branches):
			logger.error("ERROR: This script has already been run.")
			exit()
		project_id = save_project(repo, connection_bd)
		
		for branch_name in repo.branches:
			for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):											
				if str(commit.id) not in commit_visited:										
					commit_visited.add(str(commit.id))
					qty_commits +=1
					#is a merge commit?					
					if len(commit.parents) == 2 and (str(commit.id) not in merge_commit_visited):												
						qty_merge_commits += 1
						base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)						
						if(base_commit):
							if(commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex):
								qty_valid_merge_commits +=1							
						merge_commit_visited.add(str(commit.id))						
						if(printlog):
							logger.info("## Processing Merge Commit " + str(commit.id) + " - " + str(datetime.fromtimestamp(commit.commit_time)))
						save_merge_branches(repo, connection_bd, commit, project_id)
					
		if(project_id):
			qty_commits_refminer = get_count_commits(connection_bd, project_id)
			update_table_project(qty_commits, qty_merge_commits, qty_valid_merge_commits, qty_commits_refminer, project_id, connection_bd)			
		else:
			print("Error: Project not found")
		
	except TypeError as err:
		logger.exception("Type Error: " + str(err))
		connection_bd.rollback()
	except pymysql.Error as mySqlErr:
		logger.exception("Data base Error: " + str(mySqlErr))
		connection_bd.rollback()
	except Exception as ex:
		logger.exception("General Error: " + str(ex))
		connection_bd.rollback()
	finally:				
		#connection_bd.rollback()		
		connection_bd.commit()		
		connection_bd.close()
		end_time = datetime.now()
		if(printlog):
			logger.info("Finished project " + repo.workdir)
			logger.info('Elapsed time:' + str(end_time))
     

printlog = False
commit_teste = "10aee0c2becfcf8e7fa4e76f70bedea2d600a1ca"

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