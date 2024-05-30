#!/usr/bin/python3

from datetime import datetime
import argparse
import logging
import json
import csv
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

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

def trans_format(text):
	return text.split(",")

def run_apriori():
	df = pd.read_csv('../input/merge_refactoring_DB_B_simp.csv',sep=',')
	df = df.iloc[:500,:]
	del df['wasted']
	del df['rework']
	print(df.describe)
	list_transactions = []
	# creating a list of dataframe columns
	columns = list(df)
	for i in range(0,len(df)):
  		data = ""  
  		for col_name in columns:
			  data += col_name + '=' + str(df[col_name][i]) + ','
  		if data:
			  data = data[:-1]
			  list_transactions.append(data)
	df_apriori = pd.DataFrame(list_transactions,columns=['Transaction'])

	#Preparar registros para o Apriori
	df_apriori['Transaction_list'] = df_apriori['Transaction'].apply(trans_format)
	te = TransactionEncoder()
	te_ary = te.fit(df_apriori['Transaction_list']).transform(df_apriori['Transaction_list'])
	te_ary
	#Formatando como DataFrame
	df_apriori_rules = pd.DataFrame(te_ary, columns=te.columns_)
	print(df_apriori_rules)
	#Rodar o apriori
	association_rules = apriori(df_apriori_rules, min_support=0.7, use_colnames=True)
	output = pd.DataFrame(association_rules)
	print(output)
	# min_confidence=0.2, min_lift=3, min_length=2

def main():		
	run_apriori()
	
if __name__ == '__main__':
	main()