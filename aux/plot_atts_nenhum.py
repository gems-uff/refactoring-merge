# libraries
import numpy as np
import matplotlib.pyplot as plt
# Load the Pandas libraries with alias 'pd' 
import pandas as pd 


def get_quantity(attribute):
	attribute_interval = \
	{'branch1': 6, \
	'branch2': 6, \
	'merge': 6, \
	'files_changed_b1': 6, \
	'files_changed_b2': 6, \
	'files_changed_intersection': 4, \
	'files_changed_union': 6, \
	'files_edited_b1': 6, \
	'files_edited_b2': 6, \
	'files_edited_intersection': 6, \
	'files_edited_union': 6, \
	'files_add_b1': 6, \
	'files_add_b2': 6, \
	'files_add_intersection': 6, \
	'files_add_union': 6, \
	'files_rm_b1': 6, \
	'files_rm_b2': 4, \
	'files_rm_intersection': 4, \
	'files_rm_union': 6, \
	'commits_b1': 5, \
	'commits_b2': 5, \
	'commits_total': 5, \
	'authors_b1': 3, \
	'authors_b2': 3, \
	'authors_intersection': 4, \
	'authors_union': 3, \
	'committers_b1': 3, \
	'committers_b2': 3, \
	'committers_intersection': 4, \
	'committers_union': 3, \
	'lines_changed_b1': 6, \
	'lines_changed_b2': 6, \
	'lines_changed_intersection': 4, \
	'lines_changed_union': 6, \
	'lines_add_b1': 6, \
	'lines_add_b2': 6, \
	'lines_add_intersection': 4, \
	'lines_add_union': 6, \
	'lines_rm_b1': 6, \
	'lines_rm_b2': 6, \
	'lines_rm_intersection': 4, \
	'lines_rm_union': 6, \
	'rework': 4, \
	'wasted': 4, \
	'extra': 4, \
	'project_commits': 5, \
	'merge_commits_count': 5, \
	'developer_commits_until_merge': 6, \
	'developer_merges_until_merge': 6, \
	'developer_commits_in_window_of_time': 6, \
	'developer_merges_in_window_of_time': 6, \
	'time_total_y': 8, \
	'time_min_total_y': 8, \
	'time_max_total_y': 8, \
	'time_min_branch_y':15, \
	'time_max_branch_y':8, \
	'conflict_chunks': 4, \
	'conflict_files': 4, \
	'has_conflict': 2, \
	'merge_type': 1, \
	'gap': 2, \
	'X': 0}  

	return attribute_interval[attribute]

class Rule:
	def __init__(self, lhs, rhs, lift):
		self.lhs = lhs
		self.rhs = rhs
		self.lift = lift

def zeros_instead_of_none(rhs_list):
	rhs_list = [0 if v is None else v for v in rhs_list]

	return rhs_list
 
def get_right_hand_side(rhs_value, attribute_values, quantity):
	if(quantity == 6):
		get_positions = {'nenhum':0, 'pouco':1, 'muitopouco':2,'médio':3, 'muito':4, 'bastante':5}
	elif(quantity == 5):
		get_positions = {'pouco':0, 'muitopouco':1,'médio':2, 'muito':3, 'bastante':4}
	elif(quantity == 4):
		get_positions = {'nenhum':0, 'pouco':1, 'médio':2, 'muito':3}
	elif(quantity == 3):
		get_positions = {'pouco':0, 'médio':1, 'muito':2}
	elif(quantity == 8):
		get_positions = {"nenhum":0, "atéumminuto":1, "atémeiahora":2,"atéumahora":3,"atéumdia":4, "atéumasemana":5, "atéummes":6, "maisdeummes":7}
	
	elif(quantity == 15):
		get_positions = {"gap-maisdeummes" :0,"gap - até um mes":1,"gap - até uma semana":2,"gap - até um dia":3, "gap - até uma hora":4,"gap - até meia hora":5,"até um minuto":6, "nenhum":7, "até um minuto":8, "até meia hora":9,"até uma hora":10,"até um dia":11, "até uma semana":12, "até um mes":13, "mais de um mes":14}

	elif(quantity == 1):
		get_positions = {'workspace':0, 'branch':1}
	elif(quantity == 2):
		get_positions = {'True':0, 'False':1}
	else:
		print("Não implementado")

	rhs = []
	if(quantity != 1):
		rhs = [None] * quantity
	else:
		rhs = [None] * 2
	for rule in attribute_values:
		if(rule.rhs ==  rhs_value):
			rhs[get_positions[rule.lhs]] = rule.lift

	return rhs




def get_handside_value(rule_handside):
	return rule_handside.split('=')[1].replace('}','').replace(' ', '')


def get_rule(row):

	#print(row)
	lhs = row['rules'].split('=>')[0]
	rhs = row['rules'].split('=>')[1]
	lhs_value = get_handside_value(lhs)
	rhs_value = get_handside_value(rhs)

	return Rule(lhs_value, rhs_value, row['lift'])


def generate_graph(attribute, rhs_nenhum, rhs_pouco, rhs_medio, rhs_muito, quantity):
	# set width of bar
	barWidth = 0.20
	 
	# Set position of bar on X axis
	r0 = np.arange(len(rhs_nenhum))
	r1 = [x + barWidth for x in r0]
	r2 = [x + barWidth for x in r1]
	r3 = [x + barWidth for x in r2]
	 
	# Make the plot
	plt.bar(r0, rhs_nenhum, color='#708090', width=barWidth, edgecolor='white', label='none')
	plt.bar(r1, rhs_pouco, color='#DCDCDC', width=barWidth, edgecolor='white', label='low')
	plt.bar(r2, rhs_medio, color='#C0C0C0', width=barWidth, edgecolor='white', label='medium')
	plt.bar(r3, rhs_muito, color='#808080', width=barWidth, edgecolor='white', label='high')
	 
	# Add xticks on the middle of the group bars
	plt.xlabel(attribute, fontweight='bold')
	if(quantity == 3):
		graph_values = ['some', 'medium', 'many']
	elif(quantity == 4):
		graph_values = ['none','some', 'medium', 'many']
	elif(quantity == 5):
		graph_values = ['little','some', 'medium', 'many', 'too much']
	elif(quantity == 6):
		graph_values = ['none','little','some', 'medium', 'many', 'too much']
	elif(quantity == 8):
		graph_values = ['none','< 1 min','< 1/2 hour', '< 1 hour', '< 1 day', '< 1 week', '< 1 month', '> 1 month']
	#			get_positions = {"nenhum":0, "atéumminuto":1, "atémeiahora":2,"atéumahora":3,"atéumdia":4, "atéumasemana":5, "atéummes":6, "maisdeummes":7}
	elif(quantity == 1):
		graph_values = ['workspace', 'branch']
	elif(quantity == 2):
		graph_values = ['True', 'False']

	plt.xticks([r + barWidth for r in range(len(rhs_nenhum))], graph_values)
	
	plt.tight_layout()
	# Create legend & Show graphic
	plt.legend()

	#plt.show()
	plt.savefig('graphs/' +attribute+'.png')
	plt.clf()
	plt.close()




def check_lists(rhs_nenhum, rhs_pouco, rhs_medio, rhs_muito):
	if(None in rhs_nenhum or None in rhs_pouco or None in rhs_medio or None in rhs_muito):
		return False
	return True


data = pd.read_csv("~/Documents/git/merge-effort-mining/result/rules_extra_sup00001_conf_00001_nenhum.csv") 

#print(data.head())

atributes_values = {}

for index, row in data.iterrows():
	attribute = row['rules'].split('=')[0].replace("{","")  
	if("{}" not in row['rules']):
		if(attribute in atributes_values):
			atributes_values[attribute].append(get_rule(row))
			#if(attribute == 'files_edited_intersection'):
			#	print(attribute)
			#	print(row)

		else:
			atributes_values[attribute] = [get_rule(row)]
			#if(attribute == 'files_edited_intersection'):
			#	print(attribute)
			#	print(row)
			
			#   print('it is')
			#   aux = get_rule(row)
			#   print(aux.lhs)
			#   print(aux.rhs)
			#   print(aux.lift)
	#else:
	#   print(row)


#print(atributes_values)


attribute_none_values = []
attributes_not_in_range = []


for attribute in atributes_values:
	print(attribute)
	#quantity = 4

	#conflict_chunks
	#extra_nenhum = [1.04, 0.68, 0.49, 0.299]    
	#extra_pouco = [0.25, 9.78, 11.13, 6.60]
	#extra_medio = [0.236, 6.29, 12.23, 14.09]
	#extra_muito = [0.234, 4.04, 8.39, 23.49]

	quantity = get_quantity(attribute)
	print(quantity)

		#conflict_chunks example

	if(quantity in range(1,9)):

		rhs_nenhum = get_right_hand_side('nenhum', atributes_values[attribute], quantity)
		print(rhs_nenhum)
		rhs_pouco = get_right_hand_side('pouco', atributes_values[attribute], quantity)
		print(rhs_pouco)
		rhs_medio = get_right_hand_side('médio', atributes_values[attribute], quantity)
		print(rhs_medio)
		rhs_muito = get_right_hand_side('muito', atributes_values[attribute], quantity)
		print(rhs_muito)

		has_none_values = True
		if check_lists(rhs_nenhum, rhs_pouco, rhs_medio, rhs_muito):
			has_none_values = False
			#generate_graph(attribute, rhs_nenhum, rhs_pouco, rhs_medio, rhs_muito, quantity, has_none)
			pass
		else:
			attribute_none_values.append(attribute)
			#print(attribute + ' has none values')
			rhs_nenhum = zeros_instead_of_none(rhs_nenhum)
			#print(rhs_nenhum)
			rhs_pouco = zeros_instead_of_none(rhs_pouco)
			#print(rhs_pouco)
			rhs_medio = zeros_instead_of_none(rhs_medio)
			#print(rhs_medio)
			rhs_muito = zeros_instead_of_none(rhs_muito)
			#print(rhs_muito)
		generate_graph(attribute, rhs_nenhum, rhs_pouco, rhs_medio, rhs_muito, quantity)
			
	else:
		attributes_not_in_range.append(attribute)
		#print('else: ' + attribute)

print("Has none values:" + str(len(attribute_none_values)))
print(attribute_none_values)
print("Not in range:" + str(len(attributes_not_in_range)))
print(attributes_not_in_range )
