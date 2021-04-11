#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

def calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized):    
	metrics = {}	
	parents_actions = parent1_actions + parent2_actions 	
	if(normalized):
		metrics['rework'] = calculate_rework(parent1_actions, parent2_actions)/sum(parents_actions.values())
		metrics['wasted']  = calculate_wasted_effort(parents_actions, merge_actions)/sum(parents_actions.values())
		metrics['extra'] =calculate_additional_effort(parents_actions, merge_actions)/sum(merge_actions.values())
	else:
		metrics['branch1'] = sum(parent1_actions.values())
		metrics['branch2'] = sum(parent2_actions.values())
		metrics['merge'] = sum(merge_actions.values())
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

def analyze_merge_effort(merge_commit, base, repo, normalized=False):
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
		metrics = calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized)		
	except:
		print()
		logger.exception("Unexpected error in commit " + str(merge_commit))
		error = True	
	if error:
		logger.error(f'Project {repo} finished with error!')
	return metrics

def get_refactoring_commit(path_repository,commit_sha1):		
	subprocess.run([refMiner_exec, "-c", path_repository, str(commit_sha1), "-json", "ref_miner_temp.json"],
					capture_output=True)
	retorno_arq = read_json("ref_miner_temp.json")		
	# project_url = 	retorno_arq['commits'][0]['repository']
	subprocess.run(["rm", "ref_miner_temp.json"], capture_output=True)		
	commit = retorno_arq['commits']
	if len(commit) > 0:
		return commit[0]['refactorings']
	else:
		return commit	

def save_refactoring_commit(repo, connection_bd, commit_sha1, commit_seq):	
	refactorings_list = get_refactoring_commit(repo.workdir, commit_sha1)
	for refactoring in refactorings_list:
		with connection_bd.cursor() as cursor:
			sql = "INSERT INTO refactoring (id, type, description, id_commit) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (None, refactoring['type'], refactoring['description'][:1000], commit_seq))		
	if len(refactorings_list) > 0:
		#print("Commit add in cache refactoring")
		cache_refactoring.add(commit_seq)	

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
	return row

def get_db_commit_seq_by_sha1(connection_bd, sha1):		
	if sha1 not in cache_commit.keys():		
		with connection_bd.cursor() as cursor:
			cursor.execute("SELECT id FROM commit where sha1=%s", sha1)
			row = cursor.fetchone()
		return row['id']
	else:		
		return cache_commit[sha1] #commit in cache (It's not nececessary read from database)

def get_db_list_commit_branches_merge(connection_bd, merge_commit):
	list_commits = []	
	if str(merge_commit.id) not in cache_merge.keys() or len(cache_merge[str(merge_commit.id)]) == 0:
			#print("Not in Merge Cache")
			merge_commit_seq = get_db_commit_seq_by_sha1(connection_bd, str(merge_commit.id))
			with connection_bd.cursor() as cursor:
				cursor.execute("SELECT id_commit FROM merge_branch where id_merge_commit=%s", merge_commit_seq)
				rows = cursor.fetchall()		
				for row in rows:
					list_commits.append(row['id_commit'])			
			
	else: #merge_commit in cache (It's not nececessary read from database)
		#print("In Merge Cache")
		list_commits = cache_merge[str(merge_commit.id)]
	
	return list_commits
	
def get_list_commits_branch(repo, connection_bd, commit_evaluated, common_ancestor):	
	commit_list = []	
	while str(commit_evaluated.id) != str(common_ancestor):		
		is_merge_commit = len(commit_evaluated.parents) == 2												
		#print(f"Commit avaliado no branch = {str(commit_evaluated.id)}")
		commit_seq = get_db_commit_seq_by_sha1(connection_bd, str(commit_evaluated.id))
		#print(f"Seq do Commit avaliado no branch = {commit_seq}")
		if commit_seq in cache_refactoring: #commit has refactoring
			commit_list.append(commit_seq)
		if not is_merge_commit: 
			#go do the next commit in the branch
			if len(commit_evaluated.parents) > 0:				
				commit_evaluated = commit_evaluated.parents[0]				
			else: 
				break
		else:									
			# Append in commit_list the list of commits in the branch of this merge commit (only those has refactoring)			
			list_append = get_db_list_commit_branches_merge(connection_bd, commit_evaluated)
			commit_list.extend(list_append)
			# follow after common ancestor if necessary
			if not ((str(commit_evaluated.parents[0].id) == str(common_ancestor))
				or (str(commit_evaluated.parents[1].id) == str(common_ancestor))):
				commit_evaluated = repo.get(repo.merge_base(commit_evaluated.parents[0].hex, commit_evaluated.parents[1].hex))
			else:							
				break
	return commit_list

def save_commits_from_branch(connection_bd, merge_seq, commit_seq, type_branch):	
	# get commit id in database	
	with connection_bd.cursor() as cursor:
		sql = "INSERT INTO merge_branch (id, id_commit, id_merge_commit, type_branch) VALUES (%s, %s, %s, %s)"
		cursor.execute(sql, (None, commit_seq, merge_seq, type_branch))

def save_merge_branches(repo, connection_bd, merge_commit, merge_commit_seq):		
	#print(f"{merge_commit.id} - {merge_commit.message}")
	common_ancestor = repo.merge_base(merge_commit.parents[0].hex, merge_commit.parents[1].hex)	
	# Save commit from branch 1
	list_commit_seq_branch1 = get_list_commits_branch(repo, connection_bd, merge_commit.parents[0], common_ancestor)
	for commit_seq in list_commit_seq_branch1:		
		save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 1)
	"""print(f"L1 = {list_commit_seq_branch1}")
	print("branch-1")
	for c in list_commit_seq_branch1:
		print(repo.get(get_commit_by_seq(connection_bd,c)).id)"""	
	# Save commit from branch 2
	list_commit_seq_branch2 = get_list_commits_branch(repo, connection_bd, merge_commit.parents[1], common_ancestor)
	for commit_seq in list_commit_seq_branch2:
		save_commits_from_branch(connection_bd, merge_commit_seq, commit_seq, 2)
	"""print(f"L2 = {list_commit_seq_branch2}")
	print("branch-2")	
	for c in list_commit_seq_branch2:
		print(repo.get(get_commit_by_seq(connection_bd,c)).id)"""

	#Save in cache
	cache_merge[str(merge_commit.id)] = list_commit_seq_branch1	
	(cache_merge[str(merge_commit.id)]).extend(list_commit_seq_branch2)
	"""print(cache_merge)"""
	"""print(cache_refactoring)"""

def save_merge_commit(repo, connection_bd, commit, commit_seq):
	# has base version commit?
	base_commit = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
	has_base_version = True if base_commit else False
	# is fast forward commit?
	ff_commit = commit.parents[0].hex != base_commit.hex and commit.parents[1].hex != base_commit.hex
	is_fast_forward_merge = False if ff_commit else True
	
	time_ini_me = datetime.now()
	logger.info("Starting Merge Effort process")
	metrics = analyze_merge_effort(commit, base_commit, repo, False)
	logger.info('End Merge Effort process:' + str(datetime.now() - time_ini_me))
	
	with connection_bd.cursor() as cursor:
			sql = "INSERT INTO merge_commit (id, has_base_version, common_ancestor, parent1, parent2, is_fast_forward_merge, extra_effort, wasted_effort, rework_effort, id_commit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (	None,
									str(has_base_version),
									str(base_commit),
									str(commit.parents[0].id),			
									str(commit.parents[1].id),
									str(is_fast_forward_merge),
									metrics['extra'],
									metrics['wasted'],
									metrics['rework'],
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
	projectFound = find_project_in_db(connection_bd, repo.workdir)
	if(not projectFound):
		vetDir = str(repo.workdir).split('/')
		project_name = vetDir[len(vetDir)-2]
		with connection_bd.cursor() as cursor:
			sql = "INSERT INTO project (id, name, path_workdir, url) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (None, project_name, repo.workdir ,None))
			project_seq = connection_bd.insert_id()
		return project_seq
	else:
		logger.info("Project " + repo.workdir + " have already processed.")
		sys.exit()

def merge_analysis(connection_bd, repo, merge_list):	
	qtd = len(merge_list)	
	for commit in merge_list:		
		print(f"QTD: {qtd} - Commit_time: {str(datetime.fromtimestamp(commit.commit_time))}")
		qtd -=1
		cache_merge[str(commit.id)] = [] # prepare cache of merge commits branches
		time_ini_mc = datetime.now()
		logger.info("Starting Merge Commit save process")
		save_merge_commit(repo, connection_bd, commit, cache_commit[str(commit.id)])
		logger.info('End Merge Commit save process:' + str(datetime.now() - time_ini_mc))
		time_ini_mb = datetime.now()
		logger.info("Starting Merge Branch save process")
		save_merge_branches(repo, connection_bd, commit, cache_commit[str(commit.id)])
		logger.info('End Merge Branch save process:' + str(datetime.now() - time_ini_mb))

cache_merge = {}
cache_commit = {}
cache_refactoring = set()

def mining_repository(repo):
	connection_bd = open_connection_db()
	try:
		project_seq = save_project(repo, connection_bd)
		commit_visited = set()
		merge_list = []	
		for branch_name in repo.branches:
			for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):							
				if commit.id not in commit_visited:				
					print(f"{commit.id} - {str(datetime.fromtimestamp(commit.commit_time))}")
					commit_seq = save_commit(connection_bd, commit, project_seq)
					cache_commit[str(commit.id)] = commit_seq #put commit db_sequence in cache
					commit_visited.add(commit.id)				
					time_ini_rm = datetime.now()
					logger.info("Starting Refactoring Miner process")
					save_refactoring_commit(repo, connection_bd, str(commit.id), commit_seq)				
					logger.info('End Refactoring Miner process:' + str(datetime.now() - time_ini_rm))				
					
					if len(commit.parents) == 2:													
						merge_list.append(commit)
	
		merge_analysis(connection_bd, repo, merge_list)					
		connection_bd.commit()
		connection_bd.close()
	except:
		logger.info("Error ...")
		connection_bd.rollback()
		connection_bd.close()
		

def init_analysis(path_repository):	
	start_time = datetime.now()
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)
	logger.info("Starting project" + repo.workdir)

	mining_repository(repo)
		
	logger.info("Finished project " + repo.workdir)
	logger.info('Elapsed time:' + str(datetime.now() - start_time))

def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis - Refactoring')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--repo_path", help="set a path for a local git repository")
	args = parser.parse_args()	
	init_analysis(args.repo_path)

if __name__ == '__main__':
	main()