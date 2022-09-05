#!/usr/bin/python3

from datetime import datetime
import logging
import pymysql
import pandas as pd

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

def open_connection_db():
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='refactoring_merge',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection



def get_list_refactorings_by_type():
	connection_bd = open_connection_db()	
	with connection_bd.cursor() as cursor:
		cursor.execute("select type, count(*) as qty from refactoring group by type order by qty desc")
		rows = cursor.fetchall()	
	df = pd.DataFrame(rows)
	df.to_excel('../output/countRefactoringsByType.xlsx',index=False)

def main():		
	get_list_refactorings_by_type()
	
if __name__ == '__main__':
	main()