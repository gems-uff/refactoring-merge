#!/usr/bin/python3

from pickletools import TAKEN_FROM_ARGUMENT4U
from sre_constants import BRANCH
from typing import ItemsView
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
	
	with open(file_name, 'w') as csvfile:
		fc = csv.DictWriter(csvfile, fieldnames=csv_columns, )
		fc.writeheader()
		fc.writerows(list_dicts)


def open_connection_db(database_name):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database=database_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection


def analyse_branches(branch_list, merge_commit, id_branch, both_branches):
	total_commits_with_refac = 0
	total_refac_branch = 0
	
	for sha1 in branch_list:		
		#TODO: ARTIGO adicionei o "and (not cache_commit[sha1])" no IF abaixo
		# quando o script mining conseguir separar refacs específicas do merge, tirar esse "and"		
		if((sha1 in cache_commit_refactoring.keys()) and (not cache_commit[sha1])): 			
			total_commits_with_refac += 1
			for refact_type, qty in (cache_commit_refactoring[sha1]).items():				
				if both_branches:
					rt = refact_type+"_b"+id_branch				
				else:
					rt = refact_type
				merge_commit[rt] += qty
				total_refac_branch += qty

	return (total_commits_with_refac, total_refac_branch)		


def is_merge_commit(connection_bd, sha1):
	with connection_bd.cursor() as cursor:		
		cursor.execute("select c.id, mc.parent1, mc.parent2 FROM commit c, merge_commit mc where c.id = mc.id_commit and c.sha1=%s",str(sha1))
		row = cursor.fetchone()			
		if row:
			return row['id'], row['parent1'], row['parent2']
		else:
			return False, False, False


def get_common_ancestor(connection_bd, id_merge_commit) :
	with connection_bd.cursor() as cursor:		
		cursor.execute("select common_ancestor, common_ancestor_date_time FROM merge_commit where id_commit =%s",str(id_merge_commit))
		row = cursor.fetchone()		
		if row:
			return row['common_ancestor'], row['common_ancestor_date_time']
		else:
			return False, False

def get_commit_date_time(connection_bd, sha1) :
	with connection_bd.cursor() as cursor:		
		cursor.execute("select date_time FROM commit where sha1 =%s",str(sha1))
		row = cursor.fetchone()
		if row:
			return row['date_time']
		else:
			return False

def analyse_invalids_commits_in_branch(connection_bd, commits_list, external_merge_ca_date_time):
	for commit in commits_list:		
		#print(f'External merge CA date_time = {external_merge_ca_date_time}')
		datetime_commit = get_commit_date_time(connection_bd, commit)		
		#print(f'Commit {commit} date_time = {datetime_commit}')
		if (datetime_commit < external_merge_ca_date_time): #is not valid
			commits_list.remove(commit)
	return commits_list

def get_list_of_commit_in_branch(connection_bd, merge_commit_sha1, merge_commit_seq, id_branch, merge_commit_evaluated, ca_list):
	
	#print("")
	#print(f"--------------------- ANALISE DO RAMO {id_branch} do MERGE {merge_commit_sha1}---------------------")
	#print("")
	list_commit_branch = list()	
	rows = {}
	with connection_bd.cursor() as cursor:
		parameters = [merge_commit_seq, id_branch]
		cursor.execute("select c.sha1 FROM commit c, merge_branch mb where c.id = mb.id_commit and mb.id_merge_commit=%s and mb.type_branch = %s order by c.date_time",parameters)
		rows = cursor.fetchall()			
		for row in rows:
			if(row['sha1'] not in list_commit_branch):
				list_commit_branch.append(row['sha1'])
	#complement branch list with commits from merge commit branches	
	common_ancestor, common_ancestor_date_time = get_common_ancestor(connection_bd, merge_commit_seq)	
	#include common ancestor in common ancestors list	
	ca_list.append(common_ancestor)	
	#print(f'MERGE COMMIT: {merge_commit_sha1} - Common ancestor = {common_ancestor} - {common_ancestor_date_time}')
	#print(f'Lista Original do commits do branch {id_branch} = {list_commit_branch}')
	list_commit_branch_original = list_commit_branch.copy()

	for commit in list_commit_branch_original:
		#print(f'====> MC = {merge_commit_sha1} - COMMIT: {commit}')
		if(commit in cache_commit):						
			#print(f'====> CACHE_COMMIT: {cache_commit[str(commit)]}')
			if((cache_commit[str(commit)]) and (commit not in merge_commit_evaluated)): #is a merge commit		
				merge_commit_id, parent1, parent2 = is_merge_commit(connection_bd, commit)								
				#print("")
				#print(f"MC {merge_commit_sha1} HAS MERGE COMMIT INTERNO =>{commit}")
				#print(f'parent1 MC interno = {parent1}')
				#print(f'parent2 MC interno= {parent2}')
				#print(f'CA LIST = {ca_list}')
				if(parent1 in ca_list and parent2 not in ca_list):							
					#print("Pega do ramo 2") #caso semelhante projeto refactoring_toy - commit de merge 3bfbc107eac92f388de9f8b87682c3a0baf74981					
					list_b2 = get_list_of_commit_in_branch(connection_bd, commit, merge_commit_id, 2, merge_commit_evaluated, ca_list)					
					#print(f'Ramo 2 = {list_b2}')
					for c2 in list_b2:
						if c2 not in list_commit_branch:
							list_commit_branch.append(c2)
				elif (parent2 in ca_list and parent1 not in ca_list): #essa situação parece mais rara					
					#print("Pega do ramo 1")
					list_b1 = get_list_of_commit_in_branch(connection_bd, commit, merge_commit_id, 1, merge_commit_evaluated, ca_list)					
					#print(f'Ramo 1 antes do filtro = {list_b1}')
					list_b1_filtred = analyse_invalids_commits_in_branch(connection_bd, list_b1, common_ancestor_date_time)					
					#print(f'Ramo 1 depois do filtro = {list_b1_filtred}')
					for c1 in list_b1_filtred:
						if c1 not in list_commit_branch:
							list_commit_branch.append(c1)					
				elif (parent1 not in ca_list and parent2 not in ca_list): 					
					#print("Pega dos dois ramos")				
					list_b1 = get_list_of_commit_in_branch(connection_bd, commit, merge_commit_id, 1, merge_commit_evaluated, ca_list)					
					#print(f'Ramo 1 antes do filtro = {list_b1}')
					list_b1_filtred = analyse_invalids_commits_in_branch(connection_bd, list_b1, common_ancestor_date_time)					
					#print(f'Ramo 1 depois do filtro = {list_b1_filtred}')
					for c1 in list_b1_filtred:
						if c1 not in list_commit_branch:
							list_commit_branch.append(c1)
					list_b2 = get_list_of_commit_in_branch(connection_bd, commit, merge_commit_id, 2, merge_commit_evaluated, ca_list)					
					#print(f'Ramo 2 = {list_b2}')
					for c2 in list_b2:
						if c2 not in list_commit_branch:
							list_commit_branch.append(c2)					

				merge_commit_evaluated.add(commit)
	
	return list_commit_branch

			
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

def mount_branches_and_calculate_final_score(connection_bd, refac_type_list, both_branches):	
	
	with connection_bd.cursor() as cursor:
		
		#TESTE - TALPCO - ANTIGO
		#cursor.execute("select c.id, c.sha1, p.name, p.url, c.date_time, mc.has_base_version , mc.is_fast_forward_merge, mc.merge_effort_calculated, mc.merge_effort_calc_timeout, mc.extra_effort, mc.wasted_effort, mc.rework_effort, mc.branch1_actions, mc.branch2_actions, mc.common_ancestor, mc.parent1, mc.parent2 FROM project p, commit c, merge_commit mc where p.id = c.id_project and p.selected_experiments = 'True' and c.id = mc.id_commit and (c.sha1='72efba636c0fcb3f46ac13a1fe071d1a5e8d2a31' or c.sha1='d8cbcf3a08614e4d907d711f595ce1be7084eab9' or c.sha1 = 'f0b84096a26f5522001529e873f4e313f7dd87ed') order by c.date_time")
		#TESTE - TALPCO - NOVO 1
		#cursor.execute("select c.id, c.sha1, p.name, p.url, c.date_time, mc.has_base_version , mc.is_fast_forward_merge, mc.merge_effort_calculated, mc.merge_effort_calc_timeout, mc.extra_effort, mc.wasted_effort, mc.rework_effort, mc.branch1_actions, mc.branch2_actions, mc.common_ancestor, mc.parent1, mc.parent2 FROM project p, commit c, merge_commit mc where p.id = c.id_project and p.selected_experiments = 'True' and c.id = mc.id_commit and (c.sha1='55c5ee0a7224eae04dbdb414e7282ab65dc14c61' or c.sha1='a75ed3eae266d63e0870ee37afb7ec1d2d1cc000' or c.sha1 = '49d243afd36d33115b09ee1959cba617455ddd7a' or c.sha1 = 'f838ce33bac11e9a4d5b969dfc97bc11ab721401' or c.sha1 = '8284ed82b683a7a62f0fda313645c9a68f5e2e44' or c.sha1 = '88f611094bfac737bf40dad3aae37d852d9823a2') order by c.date_time")
		#TESTE - TALPCO - NOVO 2
		#cursor.execute("select c.id, c.sha1, p.name, p.url, c.date_time, mc.has_base_version , mc.is_fast_forward_merge, mc.merge_effort_calculated, mc.merge_effort_calc_timeout, mc.extra_effort, mc.wasted_effort, mc.rework_effort, mc.branch1_actions, mc.branch2_actions, mc.common_ancestor, mc.parent1, mc.parent2 FROM project p, commit c, merge_commit mc where p.id = c.id_project and p.selected_experiments = 'True' and c.id = mc.id_commit and (c.sha1='ebc66aa864f8736918d7c94969ed3ca3e9bc7cc0' or c.sha1='b984a3d19f5a77c7afd5b3339d5338fdfc8e794d' or c.sha1 = 'd5c37271a6bc0115b321f427481d8be3e1090c8f' or c.sha1 = 'a468b6b78317e802fed7bfdc571482c9e2061c59' or c.sha1 = '9f1908d3515f59a87d3cda36ae7483a4913eee94' or c.sha1 = 'a0c53de7084282e845b131a86235f6b397048fcb' or c.sha1 = 'd387199a4959f5be76fcb1a8a08c41c7ea6f1f0c' or c.sha1 = '2794d45245717971b46f22b32516a4f2357b8fd6' or c.sha1 = '9f61517024ecb9177d9bd4614d7f7468e9b8995e') order by c.date_time")

		#TESTE - THINGSBOARD
		#cursor.execute("select c.id, c.sha1, p.name, p.url, c.date_time, mc.has_base_version , mc.is_fast_forward_merge, mc.merge_effort_calculated, mc.merge_effort_calc_timeout, mc.extra_effort, mc.wasted_effort, mc.rework_effort, mc.branch1_actions, mc.branch2_actions, mc.common_ancestor, mc.parent1, mc.parent2 FROM project p, commit c, merge_commit mc where p.id = c.id_project and p.selected_experiments = 'True' and c.id = mc.id_commit and (c.sha1='fe30a23ef5596546842f59c6a62e80c5d54f680e' or c.sha1='5f7c4748379e2d9d21d87c9177ae8141cfe74f42') order by c.date_time")
		
		#OFFICIAL
		cursor.execute("select c.id, c.sha1, p.name, p.url, c.date_time, mc.has_base_version , mc.is_fast_forward_merge, mc.merge_effort_calculated, mc.merge_effort_calc_timeout, mc.extra_effort, mc.wasted_effort, mc.rework_effort, mc.branch1_actions, mc.branch2_actions, mc.common_ancestor, mc.parent1, mc.parent2 FROM project p, commit c, merge_commit mc where p.id = c.id_project and p.selected_experiments = 'True' and c.id = mc.id_commit order by c.date_time")
		list_merge_commits = cursor.fetchall()		
	
	qt = len(list_merge_commits)
	logger.info('Quantidade de Commits de Merge:' + str(len(list_merge_commits)))
	
		
	for merge_commit in list_merge_commits:								

		output[merge_commit['sha1']] = {
											'sha1': merge_commit['sha1'],
											'id': merge_commit['id'],
											'project_name': merge_commit['name'],													
											'project_url': merge_commit['url'],
											'date_time': merge_commit['date_time'],											
											'is_ff_merge': merge_commit['is_fast_forward_merge'],
											'has_base_version': merge_commit['has_base_version'],
											'merge_effort_calculated': merge_commit['merge_effort_calculated'],
											'merge_commit_calc_timeout': merge_commit['merge_effort_calc_timeout'],
											'extra': merge_commit['extra_effort'],
											'wasted': merge_commit['wasted_effort'],
											'rework': merge_commit['rework_effort'],
											'branch1_actions': merge_commit['branch1_actions'],
											'branch2_actions': merge_commit['branch2_actions'],												
											'common_ancestor': merge_commit['common_ancestor'],
											'parent1': merge_commit['parent1'],
											'parent2': merge_commit['parent2'],
											'qty_commits_with_refac': 0,
											'qty_commits_with_refac_b1': 0,
											'qty_commits_with_refac_b2': 0,
											'qty_refactorings': 0,
											'qty_refac_b1': 0,
											'qty_refac_b2': 0
										}
					
		
			
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
			
		#All merge commit should be considered to collect refactorings
						
		#if str(merge_commit['sha1']) not in cache_commit.keys():
		cache_commit[str(merge_commit['sha1'])] = True #set True if is a merge commit
		
	merge_commit_evaluated_b1 = set()
	merge_commit_evaluated_b2 = set()
	list_commits_b1 = list()
	list_commits_b2 = list()

	for sha1, merge_commit in output.items():
		logger.info('Pending: ' + str(qt))	
		print("################################################################################################################")
		print(f'MERGE COMMIT AVALIADO = {sha1} - {merge_commit["date_time"]} - PROJECT: {merge_commit["project_name"]}')
		print("################################################################################################################")
		print("")
		#COMENTAR COMANDO ABAIXO - QUANDO FOR SEM TRACE
		common_ancestor_mc, common_ancestor_date_time_mc = get_common_ancestor(connection_bd, merge_commit['id'])			
		print(f'COMMON ANCESTOR: {common_ancestor_mc} - {common_ancestor_date_time_mc}')
		print("")

		ca_list = list()
		ca_list.clear()
		list_commits_b1.clear()
		merge_commit_evaluated_b1.clear()			
		list_commits_b1 = get_list_of_commit_in_branch(connection_bd, sha1, merge_commit['id'], '1', merge_commit_evaluated_b1, ca_list)		
		qty_commits_with_refac_b1, qty_refac_b1 = analyse_branches(list_commits_b1, merge_commit,'1', both_branches)			
		print("")
		print(f'Lista FINAL de commits no ramo 1 = {list_commits_b1}')
		print("")
		list_commits_b2.clear()
		merge_commit_evaluated_b2.clear()
		ca_list.clear()
		list_commits_b2 = get_list_of_commit_in_branch(connection_bd, sha1, merge_commit['id'], '2', merge_commit_evaluated_b2, ca_list)			
		print("")
		print(f'Lista FINAL de commits no ramo 2 = {list_commits_b2}')
		print("")
		qty_commits_with_refac_b2, qty_refac_b2 = analyse_branches(list_commits_b2, merge_commit,'2', both_branches)

		qty_refactorings = qty_refac_b1 + qty_refac_b2
		qty_commits_with_refac = qty_commits_with_refac_b1 + qty_commits_with_refac_b2

		output[sha1]['qty_commits_with_refac_b1'] = qty_commits_with_refac_b1
		output[sha1]['qty_commits_with_refac_b2'] = qty_commits_with_refac_b2
		output[sha1]['qty_commits_with_refac'] = qty_commits_with_refac
		output[sha1]['qty_refac_b1'] = qty_refac_b1
		output[sha1]['qty_refac_b2'] = qty_refac_b2
		output[sha1]['qty_refactorings'] = qty_refactorings
				
		del merge_commit['id']
		

		qt -=1
				
	
def init_analysis(both_branches=False, selected_refactorings=False,database='refactoring_merge',dataset_path_name='output/merge_refactoring_ds.csv'):
	start_time = datetime.now()	
	print(database)
	
	logger.info("Starting evaluation")	
	connection_bd = open_connection_db(database)
	refac_type_list = get_list_of_distinct_refactoring(connection_bd, selected_refactorings)	
	
	calculate_qty_refactoring_each_commit_per_type(connection_bd, refac_type_list)	
	
	mount_branches_and_calculate_final_score(connection_bd, refac_type_list, both_branches)	
	
	write_csv(output,dataset_path_name)
		
	connection_bd.close()
		
	logger.info("Finished evaluation")
	logger.info('Elapsed time:' + str(datetime.now() - start_time))

def main():	
	parser = argparse.ArgumentParser(description='Extract Merge-Refactoring')	
	parser.add_argument("--branches", action='store_true', help="boolean that indicate to split refactoring attributes in two branches")
	parser.add_argument("--selected_refactorings", action='store_true', help="boolean that indicate to compute only selected refactorings -table: refac_accept_type")
	parser.add_argument("--database", default='refactoring_merge', help="database name.")
	parser.add_argument("--dataset_path_name", default='output/merge_refactoring_ds.csv', help="output dataset file name.")
	args = parser.parse_args()
	init_analysis(args.branches, args.selected_refactorings,args.database, args.dataset_path_name)
	# ./extract_merge_commits_score.py --branches --selected_refactorings --database db_refac_merge_serpro --dataset_path_name /mnt/c/Users/xxx/experimentos_serpro_new.csv
if __name__ == '__main__':
	main()
