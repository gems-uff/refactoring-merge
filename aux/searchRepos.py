#Linguagens> Python, Javascript, Ruby, C++
#
#
#
#
# https://api.github.com/repos/CodeAmend/portfolio/commits?per_page=5
# https://api.github.com/search/repositories?q=stars:%3E=20000&sort=stars&per_page=10

#freeCodeCamp/freeCodeCamp
#/repos/:owner/:repo/stats/contributors

#https://api.github.com/repos/masnun/torrent-tweeter/stats/contributors

#https://api.github.com/repos/masnun/torrent-tweeter/commits

#https://api.github.com/repos/freeCodeCamp/freeCodeCamp/commits


#https://api.github.com/search/commits?q=repo:octocat/Spoon-Knife+css

#ps: stats recebe 202 com o body em branco e depois 200, aí sim terá conteúdo

#If the data hasn’t been cached when you query a repository’s statistics, you’ll receive a 202 response; a background job is also fired to start compiling these statistics. Give the job a few moments to complete, and then submit the request again. If the job has completed, that request will receive a 200 response with the statistics in the response body.




#https://api.github.com/repos/freeCodeCamp/freeCodeCamp/contributors
#To improve performance, only the first 500 author email addresses in the repository link to GitHub users. 
#The rest will appear as anonymous contributors without associated GitHub user information.
#
#
import csv

from github import Github
#g = Github("username","password")


def save_attributes_in_csv(repo_attributes):
	attributes = []
	if(repo_attributes):
		attributes.append('full_name')
		for attr in list(repo_attributes.values())[0]:
			attributes.append(attr)

		with open('projects_list.csv', 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=attributes)
			writer.writeheader()
			for repo, attribute in repo_attributes.items():
				attribute['full_name'] = repo
				writer.writerow(attribute)

#add token
g = Github("")


#query = 'topic:cmake language:cpp'

query = 'stars:>10000'

results = g.search_repositories(query, sort='stars')

repos = {}

for repo in results:
	repo_metrics = {}
	r = g.get_repo(repo.full_name)

	repo_metrics['html_url'] = repo.html_url
	repo_metrics['stars'] = repo.stargazers_count
	repo_metrics['description'] = repo.description
	repo_metrics['language'] = repo.language
	repo_metrics['total_commits'] = r.get_commits().totalCount

	#Quando há muitos contribuidores o código quebra pois o github retorna um 403 
	try:
		repo_metrics['total_contributors'] = r.get_contributors().totalCount
	except:
		repo_metrics['total_contributors'] = -1
	
	repos[repo.full_name] = repo_metrics


	#print(repo.merges_url)
save_attributes_in_csv(repos)
print(repos)