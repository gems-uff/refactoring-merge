import csv
import merge_analysis
import sys
import argparse

def select_repos(input_file):
	repos = []
	with open(input_file) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if(int(row[1])>500 and int(row[1])<28000): 
				line_count += 1
				repos.append(row[0])
				#run_script(path)

		print('Selected ' + str(line_count) + ' repos to analyze:', repos)
	return repos
			
def main():
	parser = argparse.ArgumentParser(description='Merge effort analysis over multiple projects')
	parser.add_argument("input", help="input CSV file containing the path and the number of merges of each repository")
	parser.add_argument("output", help="output CSV file to be generated, containing the collected metrics")
	args = parser.parse_args()

	selected_repos = select_repos(args.input)
	for repo in selected_repos:
		print(repo)
		merge_analysis.init_analysis(repo, args.output, False, True)

if __name__ == '__main__':
	main()