import csv
import merge_analysis
import sys

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
	if len(sys.argv) != 3:
		print('Syntax: python3 run_repos.py <input file> <output file>')
	else:
		input_file = sys.argv[1]
		output_file = sys.argv[2]
		selected_repos = select_repos(input_file)
		for repo in selected_repos:
			print(repo)
			merge_analysis.init_analysis(repo, output_file, False, True)
	
if __name__ == '__main__':
	main()