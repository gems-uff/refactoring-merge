
import csv
import merge_analysis

def select_repos():
	repos = []
	with open('merges_count2.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if(int(row[1])>500 and int(row[1])<28000): 
				line_count += 1
				repos.append(row[0])
				#run_script(path)

		print('Processed ' + str(line_count) + ' repos')
	return repos
			
def main():
	selected_repos = select_repos()
	for repo in selected_repos:
		print(repo)
		merge_analysis.init_analysis(repo, False, True)
	
if __name__ == '__main__':
	main()	

