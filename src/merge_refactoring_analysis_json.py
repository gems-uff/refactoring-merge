"""

Como executar esse programa
sudo python3 ./merge_refactoring_analysis_json.py --repo_path /mnt/c/Users/aoliv/refactoring-merge/mergeeffort/build/refactoring-toy-example/ --output_path mnt/c/Users/aoliv/refactoring-merge/mergeeffort/build

"""

import pygit2
import os, stat
import time
from datetime import datetime
from datetime import date
import time
import json
import argparse
import logging
from collections import Counter
import subprocess

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = logging.FileHandler(r'merge_analysis.log')

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s : %(message)s')
fh.setFormatter(formatter)
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

logger.addHandler(fh)

refMiner_exec = "/mnt/c/Users/aoliv/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner"

def calculate_rework(parent1_actions, parent2_actions):
	rework_actions = parent1_actions & parent2_actions
	return (sum(rework_actions.values()))

def calculate_wasted_effort(parents_actions, merge_actions):
	wasted_actions = parents_actions - merge_actions

	return (sum(wasted_actions.values()))

def calculate_additional_effort(parents_actions, merge_actions):
	additional_actions = merge_actions - parents_actions
	return (sum(additional_actions.values()))


def calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized, merge_commits_count):    
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

	metrics['merge_commits_count'] = merge_commits_count 
	
	return metrics

def get_actions(diff_a_b):
	actions = Counter()
	for d in diff_a_b:
		file_name = d.delta.new_file.path
		for h in d.hunks:
			for l in h.lines:
				actions.update([file_name+l.origin+l.content])
	return actions

def analyze_merge_effort(project_merge_commits, repo, output_file, normalized=False, collect=False):
	error = False
	commits_metrics = {}
	merge_commits_count = 0	
	without_base_version = 0
	no_ff = 0
	#developer_attributes()
	try:
		for commit in project_merge_commits['mergeCommits']:			
			print('.', end='', flush=True)
			merge_commits_count+=1
			parent1 = repo.get(commit['parent1'])
			parent2 = repo.get(commit['parent2'])
			base = repo.merge_base(parent1.hex, parent2.hex)
			if(base):
				if(parent1.hex != base.hex and parent2.hex != base.hex):						
					base_version = repo.get(base)							
					diff_base_final = repo.diff(base_version, repo.get(commit["sha1"]), context_lines=0)
					diff_base_parent1 = repo.diff(base_version, parent1, context_lines=0)
					diff_base_parent2 = repo.diff(base_version, parent2, context_lines=0)
							
					merge_actions = get_actions(diff_base_final)
					parent1_actions = get_actions(diff_base_parent1)
					parent2_actions = get_actions(diff_base_parent2)

					metrics = calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized, merge_commits_count)
						
					# ??? ENTENDER O OBJETIVO DO COLLECTS
					""" if (collect):
						 metrics.update(collect_attributes(diff_base_parent1, diff_base_parent2, base_version, parent1, parent2, repo, commit))
					"""							
					# metrics['project'] = repo.workdir
					# commits_metrics[commit.hex] = metrics
					# mudou para
					commit["commit_metrics"] = metrics
				else:
					no_ff += 1
			else:
				without_base_version += 1
	except:
		print()
		logger.exception("Unexpected error in commit " + str(commit['sha1']))
		error = True

	# so salvar quando nao tiver erro
	"""if(collect and not error):
		save_attributes_in_csv(commits_metrics, output_file)"""

	if not error:
		print()

	logger.info("Total of merge commits: " + str(merge_commits_count))
	logger.info("Merges without base version: "+ str(without_base_version))
	logger.info("No fast forward merges: "+ str(no_ff))
	logger.info("Total of merge commits analyzed: " + str(len(commits_metrics)))

	if error:
		logger.error(f'Project {repo} finished with error!')


# Carrega um arquivo json e coloca em um dict
def read_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as f:
        return json.load(f)

# Escreve em arquivo json
def write_json(data,file_name):			
	with open(file_name, 'w', encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)	

def get_refactoring_commit(path_repository,commit_sha1):		
	subprocess.call(refMiner_exec + " -c " + path_repository + " " + str(commit_sha1) + " -json " + "ref_miner_temp.json", shell=True)
	retorno_arq = read_json("ref_miner_temp.json")		
	# project_url = 	retorno_arq['commits'][0]['repository']
	subprocess.call("rm ref_miner_temp.json", shell=True)		
	commit = retorno_arq['commits']
	if len(commit) > 0:
		return commit[0]['refactorings']
	else:
		list_refac = []
		return list_refac	


def countCommits(refactorings_set):
	commits = set()
	for item in refactorings_set:
		if item['sha1'] not in commits:
			commits.add(item['sha1'])
	return(len(commits))


def get_list_commits_branch(repo, merge_commits, commit_evaluate, common_ancestor):
	refactorings_list = []	
	while str(commit_evaluate.id) != str(common_ancestor):		
		is_merge_commit = len(commit_evaluate.parents) == 2		
		# Get Commit Refactorings
		refactorings_commit_list = get_refactoring_commit(repo.workdir,str(commit_evaluate.id))				
		for refactoring in refactorings_commit_list:
			refactoring_data = 	{
									'sha1': str(commit_evaluate.id),																					
									'type': refactoring['type'],
									'description': refactoring['description']
								}				
			refactorings_list.append(refactoring_data)
				
		if not is_merge_commit: 
			#go do the next commit in the branch			
			if len(commit_evaluate.parents) > 0:
				commit_evaluate = commit_evaluate.parents[0]
			else: 
				break
		else:															
			
			# REFATORAR - CUSTOSO
			refactoring_set_b1 = merge_commits[str(commit_evaluate.id)]['refactoringsBranch1']
			for c_b1 in refactoring_set_b1:
				ok = False
				for c in refactorings_list:
					if 	c['sha1'] == c_b1['sha1'] and c['type'] == c_b1['type'] and c['description'] == c_b1['description']:
						  ok = True
						  break
				if not ok: refactorings_list.append(c_b1)
			# REFATORAR - CUSTOSO
			refactoring_set_b2 = merge_commits[str(commit_evaluate.id)]['refactoringsBranch2']
			for c_b2 in refactoring_set_b2:
				ok = False
				for c in refactorings_list:
					if c['sha1'] == c_b2['sha1'] and c['type'] == c_b2['type'] and c['description'] == c_b2['description']:
						  ok = True
						  break
				if not ok: refactorings_list.append(c_b2)
								
			# Following after common ancestor of the merge in the path
			if not ((str(commit_evaluate.parents[0].id) == str(common_ancestor))
				or (str(commit_evaluate.parents[1].id) == str(common_ancestor))):
				commit_evaluate = repo.get(merge_commits[str(commit_evaluate.id)]['common_ancestor'])
			else:							
				return (countCommits(refactorings_list), refactorings_list)	
	return (countCommits(refactorings_list), refactorings_list)


def get_list_commits_refactoring_branches(repo, merge_commits):	
	total = len(merge_commits.items())
	for key, commit in merge_commits.items():				
		print(f"Commits de merge restantes = {total}")		
		(commit['totalCommitsBranch1'], commit['refactoringsBranch1'])  = get_list_commits_branch(repo, merge_commits, repo.get(commit['parent1']), commit['common_ancestor'])
		(commit['totalCommitsBranch2'], commit['refactoringsBranch2']) = get_list_commits_branch(repo, merge_commits, repo.get(commit['parent2']), commit['common_ancestor'])	
		total -= 1
		# CHAMAR O ANALISADOR DE ESFORÇO AQUI
	return merge_commits

def get_list_merge_commits(repo):	
	merge_commits = {}	
	merge_visited = set()	
	for branch_name in repo.branches:
		for commit in repo.walk(repo.branches[branch_name].peel().id, pygit2.GIT_SORT_REVERSE):
			if len(commit.parents) == 2 and commit.id not in merge_visited:
				merge_visited.add(commit.id)								
				commit_data = 	{									
									'author': str(commit.author.name),
									'message': str(commit.message),
									'commiter': str(commit.committer.name),
									'parent1': str(commit.parents[0].id),
									'parent2': str(commit.parents[1].id),									
									'commit_date_time': str(datetime.fromtimestamp(commit.commit_time)),
									'common_ancestor': str(repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)),
									'totalCommitsBranch1': 0,
									'totalCommitsBranch2': 0,
									'refactoringsBranch1': [],
									'refactoringsBranch2': [],								
									'commit_metrics': {}									
								}				
				merge_commits[str(commit.id)] = commit_data				
	# Da estou de memória quando tento pecorrer para achar os commit dos branches
	get_list_commits_refactoring_branches(repo, merge_commits)
	vetDir = str(repo.workdir).split('/')	
	project_name = vetDir[len(vetDir)-2]
	project_merge_commits = {
								'project': None,							
								'mergeCommits': merge_commits
							}		

	#print(project_merge_commits)

	return (project_name, project_merge_commits)


def init_analysis(path_repository,path_output):	
	start_time = datetime.now()
	repo_path = pygit2.discover_repository(path_repository)
	repo = pygit2.Repository(repo_path)
	logger.info("Starting project" + repo.workdir)
	(project_name, project_merge_commits) = get_list_merge_commits(repo)	
	
	#find_refactorings(repo.workdir, project_merge_commits)
			
	#analyze_merge_effort(project_merge_commits, repo, path_output)
	
	print(f"Commits de Merge: {len(project_merge_commits['mergeCommits'])}")	
	write_json(project_merge_commits,project_name+".json")
	
	logger.info("Finished project " + repo.workdir)
	logger.info('Elapsed time:' + str(datetime.now() - start_time))


def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis - Refactoring')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--repo_path", help="set a path for a local git repository")
	parser.add_argument("--output_path", help="set a path to put the results")
	args = parser.parse_args()	
	init_analysis(args.repo_path,args.output_path)

if __name__ == '__main__':
	main()  
