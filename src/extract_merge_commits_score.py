#!/usr/bin/python3

import pygit2
from datetime import datetime
from datetime import date
import argparse
import logging
import json
import pymysql
import csv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = logging.FileHandler(r'extract_merge_commits_score.log')

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s : %(message)s')
fh.setFormatter(formatter)
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)

output = {}
cache_commit = {}
cache_commit_refactoring = {}
cache_refactoring = {}

def read_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as f:
        return json.load(f)

def write_json(data,file_name):			
	with open(file_name, 'w', encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)

def write_csv(data,file_name):	
	
	values_view = data.values()
	value_iterator = iter(values_view)
	first_value = next(value_iterator)
	csv_columns = first_value.keys()
	
	list_dicts = list(data.values())
	#print(list_dicts)
	with open(file_name, 'w') as csvfile:
		fc = csv.DictWriter(csvfile, fieldnames=csv_columns, )
		fc.writeheader()
		fc.writerows(list_dicts)


def open_connection_db():
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='refactoring_merge',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_total_refactoring_b1_b2(sha1, id_branch, refac_type_list):
	refac_b1 = {key:val for key, val in output[sha1].items() if key.endswith('_b1')}
	refac_b2 = {key:val for key, val in output[sha1].items() if key.endswith('_b2')}	
	total_refac_branch = 0	
	total_refacs_b = {}
	for type_refac1, qty_b1 in refac_b1.items():		
		type_base = str(type_refac1)					
		type_base = type_base[:-3]
		if type_base in refac_type_list:			
			type_b2 = type_base + "_b2"			
			sum_refac_b1_b2 = qty_b1 + refac_b2[type_b2]
			#print(f"SOMA = {sum_refac_b1_b2}")
			data = {type_base+"_b"+id_branch: sum_refac_b1_b2}
			total_refac_branch += sum_refac_b1_b2			
			total_refacs_b.update(data)		
	return (total_refacs_b, total_refac_branch)

def analyse_branches(merge_commit,id_branch,refac_type_list, both_branches):
	#print(f"############   Commit de merge {merge_commit['sha1']} sendo avaliado para o branch {id_branch}")
	total_commits_with_refac = len(merge_commit['branch'+id_branch+'_list'])
	total_refac_branch = 0
	for sha1 in merge_commit['branch'+id_branch+'_list']:		
		if(sha1 in cache_commit_refactoring.keys()): #ADDED 28/12/2021			
			for refact_type, qty in (cache_commit_refactoring[sha1]).items():					
				if both_branches:
					rt = refact_type+"_b"+id_branch				
				else:
					rt = refact_type
				merge_commit[rt] += qty
				total_refac_branch += qty
							
		if sha1 in cache_commit.keys():  #ADDED 28/12/2021
			if cache_commit[sha1]: #It is a merge_commit ==> complement the list of commits in the branch
				#print("###### ACHOU MERGE ########")
				if both_branches:
					(list_refacs_branch_i, total_refac_branch_i) = get_total_refactoring_b1_b2(sha1,id_branch,refac_type_list)		
					total_refac_branch += total_refac_branch_i
					total_commits_with_refac += len(output[sha1]['branch1_list']) + len(output[sha1]['branch2_list'])
					#print(f"commit avaliado = {sha1} - qtd_refac_bi = {total_refac_branch_i} - total commits com refac = {len(output[sha1]['branch1_list']) + len(output[sha1]['branch2_list'])}")
					#print(list_refacs_branch_i)
					#print(total_refac_branch)
					#input("...")
					for refact_type, qty in list_refacs_branch_i.items():
						if refact_type not in merge_commit.keys():						
							data = {refact_type: qty}
							merge_commit.update(data)
						else:		
							merge_commit[refact_type] += qty
				else:
					for refact_type in refac_type_list:
						merge_commit[refact_type] += output[sha1][refact_type]
						total_refac_branch += output[sha1][refact_type] #ADDED 28/12/2021

	return (total_commits_with_refac, total_refac_branch)		

def join_refactoring_score(refac_type_list, both_branches):	
	for sha1, merge_commit in output.items():		
		qty_commits_with_refac_b1, qty_refac_b1 = analyse_branches(merge_commit,'1',refac_type_list, both_branches)
		qty_commits_with_refac_b2, qty_refac_b2 = analyse_branches(merge_commit,'2',refac_type_list, both_branches)
		qty_refactorings = qty_refac_b1 + qty_refac_b2
		qty_commits_with_refac = qty_commits_with_refac_b1 + qty_commits_with_refac_b2
		
		score = {
					'qty_commits_with_refac': qty_commits_with_refac,
					'qty_commits_with_refac_b1': qty_commits_with_refac_b1,
					'qty_commits_with_refac_b2': qty_commits_with_refac_b2,
					'qty_refactorings': qty_refactorings,
					'qty_refac_b1': qty_refac_b1,
					'qty_refac_b2': qty_refac_b2
				}
		merge_commit.update(score)

	for sha1, merge_commit in output.items():
		del merge_commit['branch1_list']
		del merge_commit['branch2_list']
		del merge_commit['commit_seq']
		#del merge_commit['sha1']
		#del merge_commit['project_name']
		del merge_commit['date_time']
		del merge_commit['is_ff_merge']


def get_list_of_commit_in_branch(connection_bd, merge_commit, id_branch):
	list_commit = []
	rows = {}
	with connection_bd.cursor() as cursor:
		parameters = [merge_commit['id'], id_branch]
		cursor.execute("select c.sha1 FROM commit c, merge_branch mb where c.id = mb.id_commit and mb.id_merge_commit=%s and mb.type_branch = %s",parameters)
		rows = cursor.fetchall()			
		for row in rows:
			list_commit.append(row['sha1'])
	return list_commit
			
def calculate_qty_refactoring_each_commit_per_type(connection_bd, refac_type_list):		
	for refactoring in refac_type_list:			
		with connection_bd.cursor() as cursor:
			cursor.execute("select c.sha1, r.type, count(*) as qty from commit c, refactoring r where c.id = r.id_commit and r.type = %s group by sha1", refactoring.replace("_"," "))
			list_commits_refactoring = cursor.fetchall()

		for commit in list_commits_refactoring:
			refactoring_type = {str(commit['type']).replace(" ","_"): commit['qty']}
			if str(commit['sha1']) not in cache_commit_refactoring.keys():
				cache_commit[str(commit['sha1'])] = False #inicialized with not is merge commit 
				cache_commit_refactoring[str(commit['sha1'])] = refactoring_type								
			else:								
				cache_commit_refactoring[commit['sha1']].update(refactoring_type)					


def get_list_of_distinct_refactoring(connection_bd, selected_refactorings):
	refactoring_list = []
	if not selected_refactorings:
		with connection_bd.cursor() as cursor:
			cursor.execute("select distinct type from refactoring")
			rows = cursor.fetchall()
		for row in rows:
			refactoring_list.append(str(row['type']).replace(" ","_"))
	else: # get from table refac_accept_type (a subset of more accept refactorings)
		with connection_bd.cursor() as cursor:
			cursor.execute("select distinct type from refac_accept_type")
			rows = cursor.fetchall()
		for row in rows:
			refactoring_list.append(str(row['type']).replace(" ","_"))
	
	return refactoring_list

def get_list_merge_commits(connection_bd, refac_type_list, both_branches):	
	with connection_bd.cursor() as cursor:
		cursor.execute("select c.id, c.sha1, p.name, c.date_time, mc.is_fast_forward_merge, mc.extra_effort, mc.wasted_effort, mc.rework_effort FROM project p, commit c, merge_commit mc where p.id=c.id_project and c.id = mc.id_commit and mc.is_fast_forward_merge='False' and mc.has_base_version='True' order by c.date_time")
		list_merge_commits = cursor.fetchall()		
		qt = 0
		logger.info('Quantidade de Commits de Merge:' + str(len(list_merge_commits)))
		for merge_commit in list_merge_commits:
			output[merge_commit['sha1']] = {
												'sha1': merge_commit['sha1'],
												'project_name': merge_commit['name'],
												'date_time': merge_commit['date_time'],
												'commit_seq': merge_commit['id'],
												'is_ff_merge': merge_commit['is_fast_forward_merge'],
												'extra': merge_commit['extra_effort'],
												'wasted': merge_commit['wasted_effort'],
												'rework': merge_commit['rework_effort'],
												'branch1_list': get_list_of_commit_in_branch(connection_bd, merge_commit, '1'),
												'branch2_list': get_list_of_commit_in_branch(connection_bd, merge_commit, '2')
											}
			
			if str(merge_commit['sha1']) in cache_commit.keys():				
				cache_commit[str(merge_commit['sha1'])] = True #set True if is a merge commit
			
			#include refactoring types in the output (branch_b1 and branch_b2 / or no branch)			
			for refac in refac_type_list:
				if both_branches:
					refactoring_type_b1 = {refac+"_b1": 0}
					output[merge_commit['sha1']].update(refactoring_type_b1)
					refactoring_type_b2 = {refac+"_b2": 0}
					output[merge_commit['sha1']].update(refactoring_type_b2)
				else:
					refactoring_type = {refac: 0}
					output[merge_commit['sha1']].update(refactoring_type)				
	
def init_analysis(both_branches=False, selected_refactorings=False):	
	start_time = datetime.now()	
	logger.info("Starting evaluation")	
	connection_bd = open_connection_db()
	refac_type_list = get_list_of_distinct_refactoring(connection_bd, selected_refactorings)	
	calculate_qty_refactoring_each_commit_per_type(connection_bd, refac_type_list)	
	get_list_merge_commits(connection_bd, refac_type_list, both_branches)		
	#print(output)
	join_refactoring_score(refac_type_list, both_branches)				
	print(len(output))
	write_csv(output,"../output/merge_refactoring_db.csv")
		
	connection_bd.close()
		
	logger.info("Finished evaluation")
	logger.info('Elapsed time:' + str(datetime.now() - start_time))

def main():	
	parser = argparse.ArgumentParser(description='Extract Merge-Refactoring')	
	parser.add_argument("--branches", action='store_true', help="boolean that indicate to split refactoring attributes in two branches")
	parser.add_argument("--selected_refactorings", action='store_true', help="boolean that indicate to compute only selected refactorings -table: refac_accept_type")
	args = parser.parse_args()
	init_analysis(args.branches, args.selected_refactorings)
	
if __name__ == '__main__':
	main()