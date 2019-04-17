import logging

from datetime import datetime
from datetime import timedelta
startTime = datetime.now()
from collections import Counter

from pygit2 import *
import os
import shutil
import argparse
import time
import traceback
import csv
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

#current_working_directory = os.getcwd()
#REPO_PATH = current_working_directory + "/build/" + str(time.time())
ERROR = False

def save_attributes_in_csv(commits_attributes):
	filename = '/Users/tayanemoura/Documents/git/merge-effort-mining/aux/attributes/old/mergeeffortprojectsattributesNEW.csv'
	file_exists = os.path.isfile(filename)

	attributes = []
	if(commits_attributes):
		attributes.append('commit')
		for attr in list(commits_attributes.values())[0]:
			attributes.append(attr)

		with open(filename, 'a', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=attributes)
			if(not file_exists):
				writer.writeheader()
			for commit, attribute in commits_attributes.items():
				attribute['commit'] = commit
				writer.writerow(attribute)


def git_checkout(path, hash):
	#Executando 'git checkout HASH', para mudar para o commit 'parent1'
	p = subprocess.Popen(["git", "checkout", hash], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	p.kill
	if err:
		return not err.decode().startswith("error:")

def git_reset(path):
	#Executando 'git reset', para remover eventuais conflitos restantes
	p = subprocess.Popen(["git", "reset", "--hard"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	p.kill
	if out:
		return out.decode().startswith("HEAD is now")

def git_merge_nocommit(path, hash):
	#Executando 'git merge --nocommit HASH', para gerar os conflitos
	p = subprocess.Popen(["git", "merge", "--no-commit", hash], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	p.kill
	if out:
		for line in out.decode().split("\n"):
			if line.startswith("CONFLICT "):
				return True

		return False
	elif err:
		return err.decode()

def git_diff(path):
	#Executando o comando 'git diff' para obter o conteudo modificado
	p = subprocess.Popen(["git", "diff"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	p.kill
	if out and len(out.decode(errors='ignore')) > 0:
		chunks = 0
		ln = out.decode(errors='ignore').replace("+", "").replace(" ", "").split("\n")#Removendo os caracteres '+' e ' ' para facilitar

		if ln is not None:
			#Percorrendo todas as linhas do 'diff'
			#Caso a linha inicie com o marcador '<<<<<<<', significa que um chunk foi encontrado
			for line in ln:
				if line.startswith("<<<<<<<"):
					chunks += 1

		return chunks
	elif err:
		return err.decode()
	else:
		return None


#Refaz o merge e coleta os dados
def redo_merge(repo, commit):
	path = repo.workdir
	index = repo.merge_commits(commit.parents[0], commit.parents[1])

	conflict = False
	conflicted_files = 0
	chunks = 0

	if index.conflicts is not None and len(list(index.conflicts)) > 0:

		#Caso tenha conflito, serao executados os comandos: 'git checkout', 'git merge' e 'git diff'
		conflict = True
		conflicted_files = len(list(index.conflicts))

		#Chamada dos comandos git
		git_checkout(path, commit.parents[0].hex)
		git_merge_nocommit(path, commit.parents[1].hex)
		chunks = git_diff(path)

		#Protecao para caso o valor retornado nao seja numerico
		if not str(chunks).isdigit():
			chunks = 0
		git_reset(repo.workdir)

	line = dict()
	#line["commit"] = commit.hex
	line["conflict"] = conflict
	line["conflict_chunks"] = chunks
	line["conflict_files"] = conflicted_files

	

	return line

def get_number_of_commits(git_command):
	output = subprocess.check_output([git_command], stderr=subprocess.STDOUT,shell=True)
	
	developer_commits = output.decode("utf-8").replace('\n', '')
	if(developer_commits):
		return int(developer_commits.split('\t')[0])
	return 0


def developer_attributes(merge, repo):
	os.chdir(repo.workdir)

	developer_attributes = {}

	merge_time = datetime.fromtimestamp(merge.commit_time)
	six_months_ago_merge = merge_time - timedelta(days = 1*365/12)

	command_total_commits = "git shortlog -s -n --author=\"" + merge.author.name + "\" --since=\"" + str(six_months_ago_merge) + "\"" + " --until=\"" + str(merge_time) +"\""
	developer_attributes['commits_in_window_of_time'] = get_number_of_commits(command_total_commits)

	command_total_commits_hex = "git shortlog -s -n --author=\"" + merge.author.name +"\" " + merge.hex
	developer_attributes['commits_until_merge'] = get_number_of_commits(command_total_commits_hex)
	

	command_commits_no_merge = "git shortlog -s -n --no-merges --author=\"" + merge.author.name + "\" --since=\"" + str(six_months_ago_merge) + "\"" + " --until=\"" + str(merge_time) +"\""
	developer_attributes['no_merges_in_window_of_time'] = get_number_of_commits(command_commits_no_merge)

	command_commits_no_merge_hex = "git shortlog -s -n --no-merges --author=\"" + merge.author.name +"\" " + merge.hex
	developer_attributes['no_merges_until_merge'] = get_number_of_commits(command_commits_no_merge_hex)
	

	developer_attributes['merges_in_window_of_time'] = int(developer_attributes['commits_in_window_of_time']) - int(developer_attributes['no_merges_in_window_of_time'])
	developer_attributes['merges_until_merge'] = int(developer_attributes['commits_until_merge']) - int(developer_attributes['no_merges_until_merge'])

	return(developer_attributes)

def get_merge_type(merge, authors_branch1, authors_branch2):
	merge_branch = False
	if('merge' in merge.message.lower() and 'branch' in merge.message.lower()):
		merge_branch = True

	if(merge_branch or (len(authors_branch1)>1 and len(authors_branch2)>1)):
		return True

	return False


def diff_time(timestamp1, timestamp2):
	return timestamp2-timestamp1


def calculate_max_branch_time(first_commit_b1, first_commit_b2, last_commit_b1, last_commit_b2):
	timestamp1 = min(first_commit_b1.commit_time, first_commit_b2.commit_time)
	timestamp2 = max(last_commit_b1.commit_time, last_commit_b2.commit_time)

	max_branch_time = diff_time(timestamp1, timestamp2)
	return max_branch_time

def calculate_min_branch_time(first_commit_b1, first_commit_b2, last_commit_b1, last_commit_b2):
	timestamp1 = max(first_commit_b1.commit_time, first_commit_b2.commit_time)
	timestamp2 = min(last_commit_b1.commit_time, last_commit_b2.commit_time)
	
	min_branch_time = diff_time(timestamp1, timestamp2)
	return min_branch_time

def calculate_min_total_time(base, last_commit_b1, last_commit_b2):
	timestamp = min(last_commit_b1.commit_time, last_commit_b2.commit_time)

	min_total_time = diff_time(base.commit_time, timestamp)
	return min_total_time

def calculate_max_total_time(base, last_commit_b1, last_commit_b2):
	timestamp = max(last_commit_b1.commit_time, last_commit_b2.commit_time)

	max_total_time = diff_time(base.commit_time, timestamp)
	return max_total_time

def calculate_total_time(base, merge):
	total_time = diff_time(base.commit_time, merge.commit_time)
	return total_time

def authors_in_commits(commits):
	authors = set()
	for commit in commits:
		authors.add(commit.author.name)
	return authors

def committers_in_commits(commits):
	committers = set()
	for commit in commits:
		committers.add(commit.committer.name)

	return committers

def commits_between_commits(c0,cN, repo):
	commits = []

	for commit in repo.walk(cN.id, GIT_SORT_TOPOLOGICAL):
		if(c0 and commit.hex == c0.hex):
			break
		else:
			commits.append(commit)
	commits.reverse()
	return commits

def get_total_changed_lines(lines_attributes):
	return len(lines_attributes['add']) + len(lines_attributes['rm'])

def lines_attributes(diff_a_b):
	lines_attributes = {}

	add_lines = set()
	rm_lines = set()
	for d in diff_a_b:
		file_name = d.delta.new_file.path
		for h in d.hunks:
			for l in h.lines:
				if l.origin == "+":
					add_lines.add(file_name + l.content)
				else: 
					rm_lines.add(file_name + l.content)
	lines_attributes['add'] = add_lines
	lines_attributes['rm'] = rm_lines

	return lines_attributes

def file_exists(file_name):
	if (str(file_name.id) == "0000000000000000000000000000000000000000"):
		return False
	return True


def files_attributes(diff_a_b):
	files_edited = set()
	files_add = set()
	files_rm = set()

	files_attributes = {}

	for patch in diff_a_b:
		if(not file_exists(patch.delta.new_file)):
			files_rm.add(patch.delta.old_file.path)

		elif(not file_exists(patch.delta.old_file)):
			files_add.add(patch.delta.new_file.path)
		else:
			files_edited.add(patch.delta.new_file.path)

	files_attributes['edited'] = files_edited
	files_attributes['add'] = files_add
	files_attributes['rm'] = files_rm

	return files_attributes


def collect_attributes(diff_base_parent1, diff_base_parent2, base_version, parent1, parent2, repo, merge):
	files_branch1 = files_attributes(diff_base_parent1)
	files_branch2 = files_attributes(diff_base_parent2)

	changed_files_branch1 = files_branch1['edited'].union(files_branch1['add']).union(files_branch1['rm'])
	changed_files_branch2 = files_branch2['edited'].union(files_branch2['add']).union(files_branch2['rm'])

	lines_branch1 = lines_attributes(diff_base_parent1)
	lines_branch2 = lines_attributes(diff_base_parent2)

	changed_lines_branch1 = lines_branch1['add'].union(lines_branch1['rm'])
	changed_lines_branch2 = lines_branch2['add'].union(lines_branch2['rm'])

	commits_branch1 = commits_between_commits(base_version, parent1, repo)
	commits_branch2 = commits_between_commits(base_version, parent2, repo)

	authors_branch1 = authors_in_commits(commits_branch1)
	authors_branch2 = authors_in_commits(commits_branch2)

	committers_branch1 = committers_in_commits(commits_branch1)
	committers_branch2 = committers_in_commits(commits_branch2)


	time_total = calculate_total_time(base_version, merge)

	time_max_total = calculate_max_total_time(base_version, commits_branch1[-1], commits_branch2[-1])
	time_min_total = calculate_min_total_time(base_version, commits_branch1[-1], commits_branch2[-1])
	time_min_branch = calculate_min_branch_time(commits_branch1[0], commits_branch2[0], commits_branch1[-1], commits_branch2[-1])
	time_max_branch =  calculate_max_branch_time(commits_branch1[0], commits_branch2[0], commits_branch1[-1], commits_branch2[-1])

	developer = developer_attributes(merge, repo)

	conflict_attributes = redo_merge(repo,merge)

	if get_merge_type(merge, authors_branch1, authors_branch2):
		merge_type = "branch"

	else:
		merge_type = "workspace"

	attributes = {}

	attributes['files_edited_b1'] = len(files_branch1['edited'])
	attributes['files_edited_b2'] = len(files_branch2['edited'])
	attributes['files_edited_intersection'] = len(files_branch1['edited'].intersection(files_branch2['edited']))
	attributes['files_edited_union'] = len(files_branch1['edited'].union(files_branch2['edited']))

	attributes['files_add_b1'] = len(files_branch1['add'])
	attributes['files_add_b2'] = len(files_branch2['add'])
	attributes['files_add_intersection'] = len(files_branch1['add'].intersection(files_branch2['add']))
	attributes['files_add_union'] = len(files_branch1['add'].union(files_branch2['add']))

	attributes['files_rm_b1'] = len(files_branch1['rm'])
	attributes['files_rm_b2'] = len(files_branch2['rm'])
	attributes['files_rm_intersection'] = len(files_branch1['rm'].intersection(files_branch2['rm']))
	attributes['files_rm_union'] = len(files_branch1['rm'].union(files_branch2['rm']))

	attributes['files_changed_b1'] = len(changed_files_branch1)
	attributes['files_changed_b2'] = len(changed_files_branch2)
	attributes['files_changed_intersection'] = len(changed_files_branch1.intersection(changed_files_branch2))
	attributes['files_changed_union'] = len(changed_files_branch1.union(changed_files_branch2))

	attributes['lines_add_b1'] = len(lines_branch1['add'])
	attributes['lines_add_b2'] = len(lines_branch2['add'])
	attributes['lines_add_intersection'] = len(lines_branch1['add'].intersection(lines_branch2['add']))
	attributes['lines_add_union']= len(lines_branch1['add'].union(lines_branch2['add']))

	attributes['lines_rm_b1'] = len(lines_branch1['rm'])
	attributes['lines_rm_b2'] = len(lines_branch2['rm'])
	attributes['lines_rm_intersection'] = len(lines_branch1['rm'].intersection(lines_branch2['rm']))
	attributes['lines_rm_union'] = len(lines_branch1['rm'].union(lines_branch2['rm']))

	attributes['lines_changed_b1'] = len(changed_lines_branch1)
	attributes['lines_changed_b2'] = len(changed_lines_branch2)
	attributes['lines_changed_intersection'] = len(changed_lines_branch1.intersection(changed_lines_branch2))
	attributes['lines_changed_union'] = len(changed_lines_branch1.union(changed_lines_branch2))

	attributes['commits_b1'] = len(commits_branch1)
	attributes['commits_b2'] = len(commits_branch2)
	attributes['commits_total'] = len(commits_branch1) + len(commits_branch2)

	attributes['authors_b1'] = len(authors_branch1)
	attributes['authors_b2'] = len(authors_branch2)
	attributes['authors_intersection'] = len(authors_branch1.intersection(authors_branch2))
	attributes['authors_union'] = len(authors_branch1.union(authors_branch2))

	attributes['committers_b1'] = len(committers_branch1)
	attributes['committers_b2'] = len(committers_branch2)
	attributes['committers_intersection'] = len(committers_branch1.intersection(committers_branch2))
	attributes['committers_union'] = len(committers_branch1.union(committers_branch2))

	attributes['time_total'] = time_total
	attributes['time_min_total'] = time_min_total
	attributes['time_max_total'] = time_max_total
	attributes['time_min_branch'] = time_min_branch
	attributes['time_max_branch'] = time_max_branch

	attributes['merge_type'] = merge_type



	#attributes['has_conflict'] = conflict_attributes['conflict']
	#attributes['conflict_files'] = conflict_attributes['conflict_files']
	#attributes['conflict_chunks'] = conflict_attributes['conflict_chunks']

	attributes['project_commits'] = len(commits_between_commits(None, merge, repo))


	attributes['developer_commits_in_window_of_time'] = developer['commits_in_window_of_time']
	attributes['developer_commits_until_merge'] = developer['commits_until_merge']
	attributes['developer_no_merges_in_window_of_time'] = developer['no_merges_in_window_of_time']
	attributes['developer_no_merges_until_merge'] = developer['no_merges_until_merge']
	attributes['developer_merges_in_window_of_time'] = developer['merges_in_window_of_time']
	attributes['developer_merges_until_merge'] = developer['merges_until_merge']

	return attributes

def get_actions(diff_a_b):
	actions = Counter()
	for d in diff_a_b:
		file_name = d.delta.new_file.path
		for h in d.hunks:
			for l in h.lines:
				actions.update([file_name+l.origin+l.content])
	return actions

def clone(url):
	current_working_directory = os.getcwd()
	repo_path = current_working_directory + "/build/" + str(time.time())
	repo = clone_repository(url, repo_path) 

	return repo


def calculate_rework(parent1_actions, parent2_actions):
	rework_actions = parent1_actions & parent2_actions
	return (sum(rework_actions.values()))

def calculate_wasted_effort(parents_actions, merge_actions):
	wasted_actions = parents_actions - merge_actions

	return (sum(wasted_actions.values()))

def calculate_additional_effort(parents_actions, merge_actions):
	additional_actions = merge_actions - parents_actions
	return (sum(additional_actions.values()))


def analyse(commits, repo, normalized=False, collect=False):
	global ERROR
	commits_metrics = {}
	merge_commits_count = 0
	
	without_base_version = 0
	no_ff = 0

	#developer_attributes()

	try:
		for commit in commits:
			if (len(commit.parents)==2):
				merge_commits_count+=1
				parent1 = commit.parents[0]
				parent2 = commit.parents[1]
				base = repo.merge_base(parent1.hex, parent2.hex)
				if(base):
					if(parent1.hex != base.hex and parent2.hex != base.hex):
						
						base_version = repo.get(base)
							
						diff_base_final = repo.diff(base_version, commit, context_lines=0)
						diff_base_parent1 = repo.diff(base_version, parent1, context_lines=0)
						diff_base_parent2 = repo.diff(base_version, parent2, context_lines=0)
							
						merge_actions = get_actions(diff_base_final)
						parent1_actions = get_actions(diff_base_parent1)
						parent2_actions = get_actions(diff_base_parent2)

						metrics = calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized, merge_commits_count)
						if (collect):
							 metrics.update(collect_attributes(diff_base_parent1, diff_base_parent2, base_version, parent1, parent2, repo, commit))
							
						metrics['project'] = repo.workdir
						commits_metrics[commit.hex] = metrics


					else:
						logger.info(commit.hex + " - this is a no fast-forward merge")
						no_ff += 1
				else:
					logger.info(commit.hex + " - this merge doesn't have a base version")
					without_base_version += 1
	except:
		logger.error ("Unexpected error in commit: " + str(commit.hex))
		logger.error (traceback.format_exc())

		ERROR = True


	# so salvar quando nao tiver erro
	if(collect and not ERROR):
		save_attributes_in_csv(commits_metrics)

	logger.info("Total of merge commits: " + str(merge_commits_count))
	logger.info("Merges without base version: "+ str(without_base_version))
	logger.info("No fast forward merges: "+ str(no_ff))
	return commits_metrics  

def delete_repo_folder(folder):
		shutil.rmtree(folder)

def calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized, merge_commits_count):    
	metrics = {}
	
	parents_actions = parent1_actions + parent2_actions 

	if(normalized):
		metrics['rework'] = calculate_rework(parent1_actions, parent2_actions)/sum(parents_actions.values())
		metrics['wasted']  = calculate_wasted_effort(parents_actions, merge_actions)/sum(parents_actions.values())
		metrics['extra'] =calculate_additional_effort(parents_actions, merge_actions)/sum(merge_actions.values())

	else:
		metrics['branch1'] = len(parent1_actions)
		metrics['branch2'] = len(parent2_actions)
		metrics['merge'] = len(merge_actions)
		metrics['rework'] = calculate_rework(parent1_actions, parent2_actions)
		metrics['wasted']  = calculate_wasted_effort(parents_actions, merge_actions)
		metrics['extra'] = calculate_additional_effort(parents_actions, merge_actions)

	metrics['merge_commits_count'] = merge_commits_count 
		
	return metrics

def merge_commits(commits):
	""" Gets all reachable merge commits from a set of commits """
	visited = set()
	merges = set()

	while commits:
		commit = commits.pop()
		if commit.id not in visited:
			visited.add(commit.id)
			commits.update(commit.parents)
			if len(commit.parents) == 2:
				merges.add(commit)

	return merges
	

def init_analysis(commits, repo, normalized, collect, url):
	global ERROR

	logger.info("Starting project" + repo.workdir)
	commits_metrics = analyse(commits, repo, normalized, collect)
	print(commits_metrics)
	logger.info("Total of merge commits analyzed: " + str(len(commits_metrics)))
	if(ERROR):
		logger.error("Completed with error!")
	if url:
		delete_repo_folder(repo.workdir)

	logger.info(datetime.now() - startTime)
	logger.info("Finished project" + repo.workdir)


def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--url", help="set an url for a git repository")
	group.add_argument("--local", help="set the path of a local git repository")
	parser.add_argument("--commit", nargs='+', help="set the commit (or a list of commits separated by comma) to analyse. Default: all merge commits")
	parser.add_argument("--normalized",action='store_true', help="show metrics normalized")
	parser.add_argument("--collect",action='store_true', help="collect attributes")
	args = parser.parse_args()

	
	if args.url:
		repo_aux = clone(args.url) 
		#sem essa linha da erro depoois na hora de pegar os branches, porque?? 
		repo = Repository(repo_aux.workdir)

	elif args.local:
		repo = Repository(args.local)

	commits = []
	if args.commit:
		for commit in args.commit:
			commits.append(repo.get(commit))

	else:
		commits = list(merge_commits({repo.branches[branch_name].peel() for branch_name in repo.branches}))

	init_analysis(commits, repo, args.normalized, args.collect, args.url)



	
if __name__ == '__main__':
	main()  

