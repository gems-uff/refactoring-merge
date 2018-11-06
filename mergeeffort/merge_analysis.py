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


def diff_time(timestamp1, timestamp2):
	time1 = datetime.fromtimestamp(timestamp1)
	time2 = datetime.fromtimestamp(timestamp2)
	if(time1 > time2):
		diff_time = time1 - time2
	else:
		diff_time = time2 - time1
	return diff_time


def calculate_branches_time(first_commit_b1, first_commit_b2, last_commit_b1, last_commit_b2):
	timestamp1 = min(first_commit_b1.commit_time, first_commit_b2.commit_time)
	timestamp2 = max(last_commit_b1.commit_time, last_commit_b2.commit_time)

	branches_time = diff_time(timestamp1, timestamp2)
	return branches_time.total_seconds()

def calculate_parallelism_time(first_commit_b1, first_commit_b2, last_commit_b1, last_commit_b2):
	timestamp1 = max(first_commit_b1.commit_time, first_commit_b2.commit_time)
	timestamp2 = min(last_commit_b1.commit_time, last_commit_b2.commit_time)
	
	parallelism_time = diff_time(timestamp1, timestamp2)
	return parallelism_time.total_seconds()



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

	for commit in repo.walk(cN.id, GIT_SORT_TOPOLOGICAL ):
		if(commit.hex == c0.hex):
			break
		else:
			commits.append(commit)
	return commits

def get_total_changed_lines(lines_attributes):
	return len(lines_attributes['lines_add']) + len(lines_attributes['lines_rm'])

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
	lines_attributes['lines_add'] = add_lines
	lines_attributes['lines_rm'] = rm_lines

	return lines_attributes

def get_total_changed_files(files_attributes):
	return len(files_attributes['files_edited']) + len(files_attributes['files_add']) + len(files_attributes['files_rm'])


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

	files_attributes['files_edited'] = files_edited
	files_attributes['files_add'] = files_add
	files_attributes['files_rm'] = files_rm

	return files_attributes


def collect_attributes(diff_base_parent1, diff_base_parent2, base_version, parent1, parent2, repo):
	files_branch1 = files_attributes(diff_base_parent1)
	files_branch2 = files_attributes(diff_base_parent2)

	total_changed_files_b1 = get_total_changed_files(files_branch1)
	total_changed_files_b2 = get_total_changed_files(files_branch2)

	lines_branch1 = lines_attributes(diff_base_parent1)
	lines_branch2 = lines_attributes(diff_base_parent2)

	total_changed_lines_b1 = get_total_changed_lines(lines_branch1)
	total_changed_lines_b2 = get_total_changed_lines(lines_branch2)

	commits_branch1 = commits_between_commits(base_version, parent1, repo)
	commits_branch2 = commits_between_commits(base_version, parent2, repo)

	authors_branch1 = authors_in_commits(commits_branch1)
	authors_branch2 = authors_in_commits(commits_branch2)

	committers_branch1 = committers_in_commits(commits_branch1)
	committers_branch2 = committers_in_commits(commits_branch2)

	#time_total =
	time_parallelism = calculate_parallelism_time(commits_branch1[0], commits_branch2[0], commits_branch1[-1], commits_branch2[-1])
	#time_merge = 
	time_branches =  calculate_branches_time(commits_branch1[0], commits_branch2[0], commits_branch1[-1], commits_branch2[-1])

	attributes = {}

	attributes['files_edited_b1'] = len(files_branch1['files_edited'])
	attributes['files_edited_b2'] = len(files_branch2['files_edited'])
	attributes['files_edited_intersection'] = len(files_branch1['files_edited'].intersection(files_branch2['files_edited']))
	attributes['files_edited_union'] = len(files_branch1['files_edited'].union(files_branch2['files_edited']))
	attributes['files_add_b1'] = len(files_branch1['files_add'])
	attributes['files_add_b2'] = len(files_branch2['files_add'])
	attributes['files_add_intersection'] = len(files_branch1['files_add'].intersection(files_branch2['files_add']))
	attributes['files_add_union'] = len(files_branch1['files_add'].union(files_branch2['files_add']))
	attributes['files_rm_b1'] = len(files_branch1['files_rm'])
	attributes['files_rm_b2'] = len(files_branch2['files_rm'])
	attributes['files_rm_intersection'] = len(files_branch1['files_rm'].intersection(files_branch2['files_rm']))
	attributes['files_rm_union'] = len(files_branch1['files_rm'].union(files_branch2['files_rm']))
	attributes['files_changed_b1'] = total_changed_files_b1
	attributes['files_changed_b2'] = total_changed_files_b2
	attributes['files_changed_total'] = total_changed_files_b1 + total_changed_files_b2
	attributes['lines_add_b1'] = len(lines_branch1['lines_add'])
	attributes['lines_add_b2'] = len(lines_branch2['lines_add'])
	attributes['lines_add_intersection'] = len(lines_branch1['lines_add'].intersection(lines_branch2['lines_add']))
	attributes['lines_add_union']= len(lines_branch1['lines_add'].union(lines_branch2['lines_add']))
	attributes['lines_rm_b1'] = len(lines_branch1['lines_rm'])
	attributes['lines_rm_b2'] = len(lines_branch2['lines_rm'])
	attributes['lines_rm_intersection'] = len(lines_branch1['lines_rm'].intersection(lines_branch2['lines_rm']))
	attributes['lines_rm_union'] = len(lines_branch1['lines_rm'].union(lines_branch2['lines_rm']))
	attributes['lines_changed_b1'] = total_changed_lines_b1
	attributes['lines_changed_b2'] = total_changed_lines_b2
	attributes['lines_changed_total'] = total_changed_files_b1 + total_changed_lines_b2
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

	attributes['time_parallelism'] = time_parallelism
	attributes['time_branches'] = time_branches


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
	current_working_directory = os.getcwd()
	repo_path = current_working_directory + "/build/" + str(time.time())
	repo = clone_repository(repo_url, repo_path) 

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
	
	try:
		for commit in commits:
			if (len(commit.parents)==2):
				
				parent1 = commit.parents[0]
				parent2 = commit.parents[1]
				base = repo.merge_base(parent1.hex, parent2.hex)
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
						 metrics.update(collect_attributes(diff_base_parent1, diff_base_parent2, base_version, parent1, parent2, repo))
					
					commits_metrics[commit.hex] = metrics
				else:
					print(commit.hex + " - this merge doesn't have a base version")
	except:
		print ("Unexpected error")
		print (traceback.format_exc())

	if(collect):
		save_attributes_in_csv(commits_metrics)
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
		repo = Repository(args.local)

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

