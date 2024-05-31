#!/usr/bin/python3
# -*- coding: utf-8 -*-

#switch python versions: sudo update-alternatives --config python3

# Dicas:https://pypi.org/project/PyMySQL/
# https://pymysql.readthedocs.io/en/latest/user/examples.html


from datetime import datetime
from datetime import date
import argparse
import logging
import pymysql
from collections import Counter
import json
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns;
import matplotlib.pyplot as plt
import seaborn as sns

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


def open_connection_db(database_name):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database=database_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection


def get_unprocessed_merge_effort_commits(connection_bd):
	name_projects_list = []
	valid_merge_commits_list = []
	sql = "SELECT name, number_valid_merge_commits from project"
	
	with connection_bd.cursor() as cursor:
		cursor.execute(sql)
		rows = cursor.fetchall()		
		for row in rows:			
			name_projects_list.append(row['name'])
			valid_merge_commits_list.append(row['number_valid_merge_commits'])
			
	return name_projects_list, valid_merge_commits_list


def generate_boxplot(df):
	#sns.set_theme(style = "whitegrid", font_scale= 1.1)
	cor = sns.color_palette("Greys", as_cmap=True)
	plt.figure(figsize=(9, 1.9))

	median = np.median(df['ValidsCommits'])
	upper_quartile = np.percentile(df['ValidsCommits'], 75)
	lower_quartile = np.percentile(df['ValidsCommits'], 25)

	iqr = upper_quartile - lower_quartile
	max = df['ValidsCommits'][df['ValidsCommits']<=upper_quartile+1.5*iqr].max()
	min = df['ValidsCommits'][df['ValidsCommits']>=lower_quartile-1.5*iqr].min()

	if(printlog):			
		logger.info('lower_quartile: ' + str(lower_quartile))
		logger.info('upper_quartile: ' + str(upper_quartile))
		logger.info('median: ' + str(median))
		logger.info('iqr: ' + str(iqr))
		logger.info('max: ' + str(max))
		logger.info('min: ' + str(min))
	
	#plt.text(-10, -0.43, lower_quartile, fontsize=7.5)
	#plt.text(4400, 0.35, max, fontsize=7.5)

	ax = sns.boxplot(x=df["ValidsCommits"],palette=sns.color_palette("Greys",n_colors=3))

	lower_quartile = int(lower_quartile)
	ax.text(320, 0.30, lower_quartile, rotation=90, va='center',fontsize=6)
	ax.text(4800, 0.1, max, rotation=90, va='center',fontsize=6)

	ax.set_xlabel('Number of valids commits')

	plt.savefig('boxplot.png')


def collect_projects_data(log=False, database_name="refactoring_merge"):	
	
	global printlog	
	printlog = log
	
	start_time = datetime.now()		
	
	try:
		connection_bd = open_connection_db(database_name)			
		if(printlog):			
			logger.info('Elapsed time:' + str(start_time))

		name_projects_list, valid_merge_commits_list = get_unprocessed_merge_effort_commits(connection_bd)
		data = {
        		'project':name_projects_list,
        		'ValidsCommits':valid_merge_commits_list
       	}
		
		df = pd.DataFrame(data)
		generate_boxplot(df)

							
	except TypeError as err:
		logger.exception("Type Error: " + str(err))
		connection_bd.rollback()
	except pymysql.Error as mySqlErr:
		logger.exception("Database Error: " + str(mySqlErr))
		connection_bd.rollback()	
	finally:					
		connection_bd.close()
		end_time = datetime.now()
		if(printlog):			
			logger.info('Elapsed time:' + str(end_time))			
		
printlog = False

def main():
	parser = argparse.ArgumentParser(description='Collect data from projects')	
	parser.add_argument("--log", action='store_true', help="print log")	
	parser.add_argument("--database", default='refactoring_merge', help="database name.")

	# ./generate_boxplot_repos_os.py --log --database banco_teste

	args = parser.parse_args()		

	collect_projects_data(args.log, args.database)


if __name__ == '__main__':
	main()