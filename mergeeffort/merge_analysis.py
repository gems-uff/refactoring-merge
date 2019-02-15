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

current_working_directory = os.getcwd()
REPO_PATH = current_working_directory + "/build/" + str(time.time())

def save_attributes_in_csv(commits_attributes):
	attributes = []
	if(commits_attributes):
		attributes.append('commit')
		for attr in list(commits_attributes.values())[0]:
			attributes.append(attr)

		with open('project.csv', 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=attributes)
			writer.writeheader()
			for commit, attribute in commits_attributes.items():
				attribute['commit'] = commit
				writer.writerow(attribute)

def redo_merge(repo, commit):
	index = repo.merge_commits(commit.parents[0], commit.parents[1])
	conflicted = False
	conflicted_files = 0
	if(index.conflicts):
		conflicted_files = len(list(index.conflicts))

		#conflicted_lines = 0
		# if index.conflicts else 0
		
		#if len(list(index.conflicts)) > 0:
		conflicted = True

		"""diff = repo.diff(commit, commit.parents[0])
		for d in diff:
			diff_full = d.patch.split("\n")

			inicio = False
			for line in diff_full:
				if "=======" in line:
					inicio = True
				elif ">>>>>>> " in line:
					inicio = False
				elif inicio:
					conflicted_lines += 1

		#print(conflicted_lines)"""

	conflict = {}

	conflict["has_conflict"] = conflicted
	conflict["files"] = conflicted_files
	return conflict

def developer_attributes():
	os.chdir(REPO_PATH)
	output = subprocess.check_output(["git shortlog -s -n --all"], stderr=subprocess.STDOUT,shell=True)

	developers_commits = output.decode("utf-8").split('\n')

	devs_commits = {}
	for i in developers_commits:
		if(i is not ''):
			commits = i.split('\t')[0]
			dev = i.split('\t')[-1]
			devs_commits[dev] = int(commits)

	print(devs_commits)

	output = subprocess.check_output(["git shortlog -s -n --all --no-merges"], stderr=subprocess.STDOUT,shell=True)
	developers_no_merge_commits = output.decode("utf-8").split('\n')

	devs_no_merge_commits = {}
	for i in developers_no_merge_commits:
		if(i is not ''):
			commits = i.split('\t')[0]
			dev = i.split('\t')[-1]
			devs_no_merge_commits[dev] =  int(commits)
	print(devs_no_merge_commits)

	devs_merge_commits = {}
	for dev, commits in devs_commits.items():
		devs_merge_commits[dev] = commits - devs_no_merge_commits[dev]

	print(devs_merge_commits)

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

	attributes['has_conflict'] = redo_merge(repo, merge)['has_conflict']
	attributes['conflict_files'] = redo_merge(repo, merge)['files']

	attributes['project_commits'] = len(commits_between_commits(None, merge, repo))


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
	repo_url = url
	#current_working_directory = os.getcwd()
	#repo_path = current_working_directory + "/build/" + str(time.time())
	repo = clone_repository(repo_url, REPO_PATH) 

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
	commits_metrics = {}
	
	without_base_version = 0
	no_ff = 0

	developer_attributes()

	try:
		for commit in commits:
			if (len(commit.parents)==2):
				parent1 = commit.parents[0]
				parent2 = commit.parents[1]
				base = repo.merge_base(parent1.hex, parent2.hex)
				if(parent1.hex != base.hex and parent2.hex != base.hex):
					if(base): 
						base_version = repo.get(base)
						
						diff_base_final = repo.diff(base_version, commit, context_lines=0)
						diff_base_parent1 = repo.diff(base_version, parent1, context_lines=0)
						diff_base_parent2 = repo.diff(base_version, parent2, context_lines=0)
						
						merge_actions = get_actions(diff_base_final)
						parent1_actions = get_actions(diff_base_parent1)
						parent2_actions = get_actions(diff_base_parent2)

						metrics = calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized)
						if (collect):
							 metrics.update(collect_attributes(diff_base_parent1, diff_base_parent2, base_version, parent1, parent2, repo, commit))
						
						commits_metrics[commit.hex] = metrics
					else:
						print(commit.hex + " - this merge doesn't have a base version")
						without_base_version += 1
				else:
					print(commit.hex + " - this is a no fast-forward merge")
					no_ff += 1
	except:
		print ("Unexpected error")
		print (traceback.format_exc())

	if(collect):
		save_attributes_in_csv(commits_metrics)

	print("Merges without base version: "+ str(without_base_version))
	print("No fast forward merges: "+ str(no_ff))
	return commits_metrics	

def delete_repo_folder(folder):
		shutil.rmtree(folder)

def calculate_metrics(merge_actions, parent1_actions, parent2_actions, normalized):	
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
		
	return metrics

			
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
		repo = clone(args.url) 

	elif args.local:
		global REPO_PATH
		repo = Repository(args.local)
		REPO_PATH = args.local

	commits = []
	if args.commit:
		for commit in args.commit:
			commits.append(repo.get(commit))

	else:
		commits = repo.walk(repo.head.target, GIT_SORT_TIME | GIT_SORT_REVERSE)

	commits_metrics = analyse(commits, repo, args.normalized, args.collect)
	print(commits_metrics)
	print("Total of merge commits: " + str(len(commits_metrics)))
	if args.url:
		delete_repo_folder(repo.workdir)

	print(datetime.now() - startTime)

	
if __name__ == '__main__':
	main()	

