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


REFMINER_TIMEOUT = 300 # 5 min

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
                             database='refactoring_merge_teste', ###ANDRE ALTERAR TESTE 10/09/2022
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
		logger.exception("Unexpected error in commit " + str(merge_commit))
		error = True	
	if error:
		logger.error(f'Project {repo} finished with error!')
	return metrics

def get_refactoring_commit(path_repository,commit_sha1):		
	""" /mnt/c/Users/aoliv/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner -c /mnt/c/Users/aoliv/RepositoriosEO1/spring-boot/ 8364840cd5a0cf7c838085378a275f350a682046 -json teste1.json"""
	commit = []	
	try:
		subprocess.run([refMiner_exec, "-c", path_repository, str(commit_sha1), "-json", "ref_miner_temp.json"],
					timeout=REFMINER_TIMEOUT, capture_output=True) #timeout = 2 hours
		retorno_arq = read_json("ref_miner_temp.json")		
		commit = retorno_arq['commits']
		if len(commit) > 0:
			return (commit[0]['refactorings'], False)
		else:			
			return (commit, False)
	except:	
		logger.info("Refatoring Miner Timeout: " + commit_sha1)		
		return (commit, True)
	finally:
		subprocess.run(["rm", "ref_miner_temp.json"], capture_output=True)

		
def save_refactoring_commit(repo, connection_bd, commit_sha1, commit_seq):	
	(refactorings_list, refminer_timeout) = get_refactoring_commit(repo.workdir, commit_sha1)	
	for refactoring in refactorings_list:
		with connection_bd.cursor() as cursor:
			sql = "INSERT INTO refactoring (id, type, description, id_commit) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (None, refactoring['type'], refactoring['description'][:1000], commit_seq))		
	if len(refactorings_list) > 0:		
		cache_refactoring.add(commit_seq)
	return (len(refactorings_list), refminer_timeout)

"""Not Used"""
def get_db_commit_data(connection_bd, sha1):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT * FROM commit where sha1=%s", sha1)
		row = cursor.fetchone()
	return row

"""Not Used"""
def get_db_merge_commit_data(connection_bd, sha1):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT * FROM commit, merge_commit where commit.id = merge_commit.id_commit and commit.sha1=%s", sha1)
		row = cursor.fetchone()				
	return row

"""Not Used"""
def get_commit_by_seq(connection_bd, commit_seq):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT * FROM commit where id=%s", commit_seq)
		commit = cursor.fetchone()
	return commit['sha1']

	
def find_project_in_db(connection_bd, path_workdir):	
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT id FROM project where project.path_workdir = %s", path_workdir)
		row = cursor.fetchone()	
	if row:
		return row['id']	
	else:
		return False
	

def has_refactorings_by_sha1(connection_bd,commit_sha1):		
	with connection_bd.cursor() as cursor:
		cursor.execute("SELECT c.id FROM commit c, refactoring r where c.id = r.id_commit and c.sha1=%s",commit_sha1)
		rows = cursor.fetchall()		
	if rows:		
		return rows[0]['id']
	else:
		return False

def get_db_commit_seq_by_sha1(connection_bd, sha1):		
	if sha1 not in cache_commit.keys():		
		with connection_bd.cursor() as cursor:
			cursor.execute("SELECT id FROM commit where sha1=%s", sha1)
			row = cursor.fetchone()
		if row:
			return row['id']
		else:
			return False
	else:		
		return cache_commit[sha1] #commit in cache (It's not nececessary read from database)

"""Not Used"""
def get_db_list_of_commit_with_refactoring_in_branches(connection_bd, merge_commit):
	list_commits = []	
	if str(merge_commit.id) not in cache_merge.keys() or len(cache_merge[str(merge_commit.id)]) == 0:
			merge_commit_seq = get_db_commit_seq_by_sha1(connection_bd, str(merge_commit.id))
			with connection_bd.cursor() as cursor:
				cursor.execute("SELECT id_commit FROM merge_branch where id_merge_commit=%s", merge_commit_seq)
				rows = cursor.fetchall()		
				for row in rows:
					list_commits.append(row['id_commit'])			
			
	else: #merge_commit in cache (It's not nececessary read from database)
		list_commits = cache_merge[str(merge_commit.id)]
	
	return list_commits
	
def get_list_commits_branch(repo, connection_bd, merge_commit, commit_evaluated, common_ancestor):	
	commit_list = []		
		
	if common_ancestor:	
		common_ancestor_obj = repo.get(common_ancestor)
		# ATENÇÃO: a segunda parte do while abaixo (depois do and) foi adicionado para resolver questões de ancestrais comuns um pouco confusos, como por exemplo do commit 6c0d2cb4c21d1d0c5fa1570f9d99b4927801e519 (quinta-feira, 27 de setembro de 2012 16:47:37) do projeto mockito
		while (str(commit_evaluated.id) != str(common_ancestor)) and (commit_evaluated.commit_time > common_ancestor_obj.commit_time):			
			is_merge_commit = len(commit_evaluated.parents) == 2
			commit_seq = get_db_commit_seq_by_sha1(connection_bd, str(commit_evaluated.id))			
			
			if commit_seq in cache_refactoring: #just include in branch commit with refactorings
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
	list_commit_seq_branch1 = get_list_commits_branch(repo, connection_bd, merge_commit.id, merge_commit.parents[0], common_ancestor)
	for commit_seq in list_commit_seq_branch1:		
		save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 1)

	
	"""#if str(merge_commit.id) == "9208854ef64240ebfb72e21e97e7434e8b60fbe8":	
	print(f"L1 = {list_commit_seq_branch1}")
	print("branch-1")
	for c in list_commit_seq_branch1:
		a = repo.get(get_commit_by_seq(connection_bd,c))
		print(f"B1 - {a.id} = {datetime.fromtimestamp(a.commit_time)}")"""
	
	# Save commit from branch 2
	list_commit_seq_branch2 = get_list_commits_branch(repo, connection_bd, merge_commit.id, merge_commit.parents[1], common_ancestor)
	for commit_seq in list_commit_seq_branch2:
		save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 2)
	
	
	"""#if str(merge_commit.id) == "9208854ef64240ebfb72e21e97e7434e8b60fbe8":
	print(f"L2 = {list_commit_seq_branch2}")
	print("branch-2")	
	for c in list_commit_seq_branch2:
		a = repo.get(get_commit_by_seq(connection_bd,c))
		print(f"B2 - {a.id} = {datetime.fromtimestamp(a.commit_time)}")
	print("====================================================")"""

	#Save in cache
	cache_merge[str(merge_commit.id)] = list_commit_seq_branch1	
	(cache_merge[str(merge_commit.id)]).extend(list_commit_seq_branch2)

def save_merge_commit(repo, connection_bd, commit, commit_seq,merge_effort):	
	has_base_version = True
	metrics = {}	
	base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
	merge_effort_calculated = True
	# is fast forward commit?
	ff_commit = commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex
	is_fast_forward_merge = False if ff_commit else True
		
	if base_commit and merge_effort:				
		time_ini_me = datetime.now()
		if(printlog):
			logger.info("Starting Merge Effort process")
		metrics = analyze_merge_effort(commit, base_commit, repo)
		if(printlog):
			logger.info('End Merge Effort process:' + str(datetime.now() - time_ini_me))
	else:
		if not base_commit:
			has_base_version = False
			metrics = {'extra':0, 'wasted':0, 'rework':0, 'branch1_actions':0, 'branch2_actions':0, 'merge_actions':0}
			merge_effort_calculated = False
	

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

def save_project(repo, connection_bd):		
	projec_id = find_project_in_db(connection_bd, repo.workdir)
	if(not projec_id):
		vetDir = str(repo.workdir).split('/')
		project_name = vetDir[len(vetDir)-2]
		with connection_bd.cursor() as cursor:
			sql = "INSERT INTO project (id, name, path_workdir, url) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (None, project_name, repo.workdir ,None))
			project_seq = connection_bd.insert_id()
		return project_seq
	else:		
		return projec_id
		#raise TypeError("Project " + repo.workdir + " have already processed")

def set_refminer_timeout_in_commit(connection_bd, sha1):
	with connection_bd.cursor() as cursor:
			sql = "UPDATE commit SET refminer_timeout = 'True' where sha1=%s"			
			cursor.execute(sql, sha1)
			
def merge_analysis(connection_bd, repo, merge_list, merge_effort):	
	qtd = len(merge_list)	
	for commit in merge_list:

		base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
		"""TODO: ESSE IF FOI COLOCADO PARA OTIMIZAR, POIS NÃO EXECUTAR O MERGE EFFORT E MERGE BRANCH DE 
		COMMITS DE MERGE MARCADOS COMO --NO-FF.
		OUTRA OTIMIZAÇÃO É USAR PANDAS E NÃO CHAMAR O REFMINER PARA TODOS OS COMMITS. PRIMEIRO MONTAR O BRANCH
		EM MEMÓRIA E DEPOIS SÓ CHAMAR ESSE O REF MINER E ESSE TRECHO DE MERGE EFFORT
		"""
		if base_commit:		
			# is fast forward commit?
			valid_commit_merge = commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex
			
			if valid_commit_merge:	
				if(printlog):
					logger.info("Qtd = "+ str(qtd) + " Commit_time = " + str(datetime.fromtimestamp(commit.commit_time)))
				qtd -=1
				cache_merge[str(commit.id)] = [] # prepare cache of merge commits branches		
				save_merge_commit(repo, connection_bd, commit, cache_commit[str(commit.id)],merge_effort)		
				time_ini_mb = datetime.now()
				if(printlog):
					logger.info("Starting Merge Branch save process")
				save_merge_branches(repo, connection_bd, commit, cache_commit[str(commit.id)])
				if(printlog):
					logger.info('End Merge Branch save process:' + str(datetime.now() - time_ini_mb))
			else:
				if(printlog):
					logger.info("Commit: "+ str(commit.id) + " inválido - no-ff")
		else:
			if(printlog):
				logger.info("Commit: "+ commit.id + " inválido - has no base version")
cache_merge = {}
cache_commit = {}
cache_refactoring = set()
refMiner_exec = ""
printlog = False

def save_json_project_results(project_data):	
	list_projects = read_json("../output/projects_results.json")
	list_projects.append(project_data)	
	write_json(list_projects,"../output/projects_results.json")

def get_qty_merge_commits_involving_refactoring():
	qty = 0
	for sha1, list_refac in cache_merge.items():		
		if len(list_refac) > 0:
			qty +=1
	return qty

def set_id_commits_processed(connection_bd,path_project):
	with connection_bd.cursor() as cursor:
		cursor.execute("select c.id, c.sha1 from commit c, project p where c.id_project = p.id and p.path_workdir = %s",path_project)
		rows = cursor.fetchall()			
		for row in rows:
			cache_commit[str(row['sha1'])] = row['id']

def set_id_commits_with_refactoring(connection_bd,path_project):
	with connection_bd.cursor() as cursor:
		cursor.execute("select c.id, count(*) from commit c, project p, refactoring r where c.id_project = p.id and r.id_commit = c.id and p.path_workdir =%s group by c.id",path_project)
		rows = cursor.fetchall()				
		for row in rows:
			cache_refactoring.add(row['id'])

def mining_repository(repo,merge_effort,path_repository):	
	connection_bd = open_connection_db()
	start_time = datetime.now()
	end_time = datetime.now()
	if(printlog):
		logger.info("Starting project" + repo.workdir)	
	qty_merge_commits = 0	
	qty_refminer_timeout = 0
	qty_refactoring_commit = 0
	commit_visited = set()	
	set_id_commits_processed(connection_bd,path_repository)
	if(printlog):
		logger.info("Commits already processed = " + str(len(cache_commit)))
	
	if(len(cache_commit)>0):
		set_id_commits_with_refactoring(connection_bd,path_repository)
		
	if(printlog):
		logger.info("Commits with refactoring already processed = " + str(len(cache_refactoring)))
		
	try:
		project_seq = save_project(repo, connection_bd)		
		merge_list = []

		for branch_name in repo.branches:
			for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):				
				if str(commit.id) not in commit_visited:					
					commit_visited.add(str(commit.id))					
					#commit_seq = get_db_commit_seq_by_sha1(connection_bd, str(commit.id))					
					commit_processed = str(commit.id) in cache_commit.keys()									
					
					if not commit_processed: #commit not saved in database
						if(printlog):
							logger.info("## Commit " + str(commit.id) + " was not processed")
						commit_seq = save_commit(connection_bd, commit, project_seq)
						cache_commit[str(commit.id)] = commit_seq #put commit db_sequence in cache
						(qty_refactoring_commit, refminer_timeout) = save_refactoring_commit(repo, connection_bd, str(commit.id), commit_seq)
						if(printlog):
							logger.info("## Saving refactoring " + str(commit.id) + " Refacs=" + str(qty_refactoring_commit))
						if(refminer_timeout):
							set_refminer_timeout_in_commit(connection_bd, str(commit.id))
							qty_refminer_timeout += 1										
					
					if len(commit.parents) == 2:
						if not commit_processed:
							if(printlog):
								logger.info("Merge Commit = " + str(commit.id) + " - " + str(datetime.fromtimestamp(commit.commit_time)))
						merge_list.append(commit)
						qty_merge_commits +=1
										
					connection_bd.commit()

		merge_analysis(connection_bd, repo, merge_list, merge_effort)
		
		connection_bd.commit()

		end_time = datetime.now() - start_time
		project_data = {
						'projectWorkDir': repo.workdir,
						'dateTimeExecution': str(datetime.now()),
						'elapsedTime': str(end_time),						
						'qtyCommits':len(commit_visited),
						'qtyMergeCommits':qty_merge_commits						
					   }	
		save_json_project_results(project_data)		
	#except TypeError as err: #ANDRE DESCOMENTAR
	#	logger.info("Type Error: " + str(err))
	#	connection_bd.rollback()
	except pymysql.Error as mySqlErr:
		logger.info("Data base Error: " + str(mySqlErr))
		connection_bd.rollback()
	#except Exception as ex: #ANDRE DESCOMENTAR
	#	logger.info("General Error: " + str(ex))
	#	connection_bd.rollback()
	finally:				
		connection_bd.close()
		if(printlog):
			logger.info("Finished project " + repo.workdir)
			logger.info('Elapsed time:' + str(end_time))
		

def init_analysis(path_repository,refminer_path,merge_effort=False,log=False):		
	global refMiner_exec
	global printlog
	refMiner_exec = refminer_path
	printlog = log
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)
	mining_repository(repo,merge_effort,path_repository)

def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis - Refactoring')	
	parser.add_argument("--repo_path", help="set a path to local git repository")
	parser.add_argument("--merge_effort", action='store_true', help="boolean to compute or not the merge effort")
	parser.add_argument("--refminer_path", help="set a path to RefactoringMiner executable code")
	parser.add_argument("--log", action='store_true', help="print log")

	# Example
	# ./mining_refactoring_merge.py --log --merge_effort --repo_path /mnt/c/Users/aoliv/RepositoriosEO1/XXXX --refminer_path  /mnt/c/Users/aoliv/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner

	args = parser.parse_args()	
	init_analysis(args.repo_path, args.refminer_path, args.merge_effort,args.log)

if __name__ == '__main__':
	main()