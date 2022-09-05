from pygit2 import *
import os
import csv
import subprocess

INITIAL_DIR = os.getcwd()

def write_csv(row):
	global INITIAL_DIR
	with open(INITIAL_DIR + '/merges_count.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(row)

	csvFile.close()


def total_merges(repo):
	print("Counting merges of repo " + repo)
	os.chdir(repo)

	print(os.getcwd())
	git_command = "git rev-list --min-parents=2 --max-parents=2 --count --all"

	print(git_command)

	output = " "
	try:
		output = subprocess.check_output([git_command], stderr=subprocess.STDOUT,shell=True)
		output = output.decode("utf-8").replace('\n', '')
	
	except: 
		output = "error"
	
	print(output)
	write_csv([repo, output])

	return output

def get_repos_dir():
	global INITIAL_DIR

	repos_dir = []

	for i in os.listdir(INITIAL_DIR):
		if os.path.isdir(i):
			repo = INITIAL_DIR + "/" + i
			repos_dir.append(repo)

	return repos_dir



def main():
	repos_dir = get_repos_dir()
	print(repos_dir)

	for repo in repos_dir:
		total_merges(repo)



if __name__ == '__main__':
	main()  

